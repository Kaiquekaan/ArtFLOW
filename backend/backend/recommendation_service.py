import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import pickle
from api.models import Interaction, Post, UserData
from django.core.cache import cache
import re
from django.db.models import Q
import unicodedata
from collections import Counter

INTERACTION_SCORES = {
    'like': 1,
    'comment': 2,
    'favorite': 3,
    'view': 0.5  
}

def save_model(algo, filename='svd_model.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(algo, f)

def load_model(filename='svd_model.pkl'):
    """
    Carrega o modelo SVD salvo de um arquivo.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def get_cached_svd_model(filename='svd_model.pkl'):
    """
    Retorna o modelo SVD carregado do cache, ou o carrega do arquivo e armazena no cache.
    """
    model = cache.get('svd_model')
    if model is None:
        print("Modelo não encontrado no cache. Carregando do arquivo...")
        model = load_model(filename)
        cache.set('svd_model', model, timeout=60*60)  # Armazena no cache por 1 hora
    else:
        print("Modelo carregado do cache.")
    return model

def build_user_item_matrix():
    """
    Constrói uma matriz de interações usuário-item a partir do banco de dados.
    """

    interactions = Interaction.objects.values('user_id', 'post_id', 'interaction_type')  # Ajuste o campo 'score'
    df = pd.DataFrame(interactions)
    df['score'] = df['interaction_type'].map(INTERACTION_SCORES)
    user_item_matrix = df.pivot_table(index='user_id', columns='post_id', values='score', fill_value=0)
    return user_item_matrix

def train_svd_model(user_item_matrix):
    """
    Treina um modelo SVD usando a biblioteca Surprise.
    """
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(user_item_matrix.stack().reset_index(), reader)
    algo = SVD()

    # Avaliação cruzada para ver a precisão do modelo
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    
    # Treina o modelo em todos os dados
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    
    return algo

user_item_matrix = build_user_item_matrix()
svd_model = get_cached_svd_model()




def get_top_n_recommendations(user_id, user_item_matrix, svd_model, n=10):
    """
    Retorna as top N postagens recomendadas para um usuário específico, excluindo as próprias.
    """
    # Obter todas as postagens
    all_post_ids = user_item_matrix.columns

    if user_id not in user_item_matrix.index:
        # Para novos usuários, exibir posts populares ou recentes
        return Post.objects.order_by('-created_at')[:n].values_list('id', flat=True)
    else:
        # Excluir as interações próprias e postagens do próprio usuário
        already_interacted = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index

        # Fazer previsões para postagens não interagidas, e que não sejam do próprio usuário
        predictions = [
            svd_model.predict(user_id, post_id) 
            for post_id in all_post_ids 
            if post_id not in already_interacted and not Post.objects.filter(id=post_id, user_id=user_id).exists()
        ]

        # Classificar por classificação prevista
        top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]

        # Retornar IDs das postagens recomendadas
        return [pred.iid for pred in top_n]


def build_tfidf_matrix():
    """
    Constrói uma matriz TF-IDF para as legendas das postagens.
    """
    posts = Post.objects.values('id', 'caption')
    df_posts = pd.DataFrame(posts)

    # Vetorização das legendas das postagens
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_posts['caption'].fillna(''))
    
    return df_posts, tfidf_matrix

df_posts, tfidf_matrix = build_tfidf_matrix()

def get_similar_posts(post_id, df_posts, tfidf_matrix, n=10):
    """
    Retorna as postagens mais similares a uma postagem específica.
    """
    # Verifica se o post_id existe no DataFrame
    if post_id in df_posts['id'].values:
        post_index = df_posts[df_posts['id'] == post_id].index[0]
        cosine_similarities = cosine_similarity(tfidf_matrix[post_index], tfidf_matrix).flatten()

        # Obter índices das postagens mais similares
        similar_indices = cosine_similarities.argsort()[:-n-1:-1]

        # Retornar IDs das postagens mais similares
        similar_posts = df_posts.iloc[similar_indices]['id']
        return similar_posts.tolist()
    else:
        # Caso o post_id não seja encontrado, retornar uma lista vazia ou posts populares
        return Post.objects.order_by('-created_at')[:n].values_list('id', flat=True)
    

def normalize_text(text):
    # Remove acentos e normaliza o texto
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def extract_hashtags(caption):
    # Extrai hashtags da legenda
    hashtags = re.findall(r'#\w+', caption)
    # Normaliza as hashtags para remover acentos
    return {normalize_text(tag) for tag in hashtags}


def hashtag_based_recommendation(user, limit=10):
    # Obtém as hashtags das interações do usuário no modelo Interaction
    user_interactions = Interaction.objects.filter(user=user).select_related('post')
    user_hashtags = set()

    for interaction in user_interactions:
        post_caption = interaction.post.caption
        if post_caption:
            # Extrai e normaliza hashtags, removendo acentos
            user_hashtags.update(extract_hashtags(post_caption))

    # Log para verificar as hashtags extraídas
    print("Hashtags do usuário:", user_hashtags)

    

    # Se não houver hashtags, retorna posts populares
    if not user_hashtags:
        return Post.objects.filter(is_private=False, is_sensitive=False).order_by('-created_at')[:limit]

    # Construção da query normalizada
    hashtag_query = Q()
    for hashtag in user_hashtags:
        hashtag_query |= Q(caption__icontains=normalize_text(hashtag.replace('#', '')))

    # Log para verificar a query construída
    print("Query de hashtag:", hashtag_query)

    # Buscar postagens que contenham as hashtags normalizadas
    recommended_posts = Post.objects.filter(
        hashtag_query,
        is_private=False,
        is_sensitive=False
    ).exclude(user=user).order_by('-created_at')[:limit]

    # Log para verificar o resultado da busca
    print("Postagens recomendadas:", recommended_posts)

    return recommended_posts

def get_trending_hashtags():
    # Define o período de tempo, como as últimas 24 horas
    time_threshold = timezone.now() - timedelta(days=100)
    recent_posts = Post.objects.filter(
        created_at__gte=time_threshold,
        is_private=False, is_sensitive=False
    )

    # Contador para hashtags
    hashtags_count = Counter()
    for post in recent_posts:
        # Extrai hashtags da legenda do post
        hashtags = re.findall(r'#\w+', post.caption or '')
        hashtags_count.update(hashtags)  # Atualiza o contador com todas as hashtags do post

    # Obtém as 10 hashtags mais comuns
    top_5_hashtags = hashtags_count.most_common(5)

    print("Top 5 Hashtags:", top_5_hashtags) 
    
    return top_5_hashtags 

def search_posts(query, limit=10):
    # Normaliza o termo de pesquisa para evitar problemas com acentos
    normalized_query = normalize_text(query.lstrip('#'))
    search_results = Post.objects.filter(
        Q(caption__icontains=normalized_query),
        is_private=False,
        is_sensitive=False
    ).order_by('-created_at')[:limit]

    print("Resultados da busca:", search_results)

    return search_results

def hybrid_recommendation(user_id, post_id, user_item_matrix, svd_model, df_posts, tfidf_matrix, excluded_user_ids=None, n=10):
    """
    Combina recomendações colaborativas e baseadas em conteúdo.
    """
    # Obter recomendações colaborativas
    cf_recommendations = list(get_top_n_recommendations(user_id, user_item_matrix, svd_model, n))

    # Gerar recomendações baseadas em conteúdo
    if post_id:
        content_recommendations = list(get_similar_posts(post_id, df_posts, tfidf_matrix, n))
    else:
        content_recommendations = []

    # Combinar ambas as recomendações
    hybrid_recommendations = list(set(cf_recommendations + content_recommendations))

    # Filtrar as postagens próprias
    hybrid_recommendations = [
        post_id for post_id in hybrid_recommendations
        if not Post.objects.filter(id=post_id, user_id=user_id).exists() and 
           (excluded_user_ids is None or not Post.objects.filter(id=post_id, user_id__in=excluded_user_ids).exists())
    ]
    
    return hybrid_recommendations


def main():
    # Carrega o modelo salvo
    svd_model = load_model('svd_model.pkl')

    # Constrói a matriz de interações usuário-item
    user_item_matrix = build_user_item_matrix()

    # Obter as top 10 recomendações para um usuário específico (Exemplo com user_id=1)
    user_id = 1
    top_recommendations = get_top_n_recommendations(user_id, user_item_matrix, svd_model, n=10)

    # Exibe as recomendações
    print("Top 10 recomendações para o usuário", user_id, ":", top_recommendations)

# Chama a função principal
if __name__ == '__main__':
    main()