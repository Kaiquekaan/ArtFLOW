import pandas as pd
from api.models import Interaction, Post, UserData
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
from django.db.models import Count
import pickle


def train_and_save_model():
    # Constrói a matriz de interações usuário-item
    user_item_matrix = build_user_item_matrix()

    # Treina o modelo SVD
    svd_model = train_svd_model(user_item_matrix)

    # Salva o modelo treinado
    save_model(svd_model, 'svd_model.pkl')


def build_user_item_matrix():
    """
    Constrói uma matriz de interações usuário-item a partir do banco de dados.
    """
    interactions = Interaction.objects.values('user_id', 'post_id', 'interaction_type')
    df = pd.DataFrame(interactions)

    INTERACTION_SCORES = {
        'like': 1,
        'comment': 2,
        'favorite': 3,
        'view': 0.5
    }
    
    # Mapeia interaction_type para valores numéricos
    df['score'] = df['interaction_type'].map(INTERACTION_SCORES)
    
    # Cria a matriz user-item (preenche valores ausentes com 0)
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

def save_model(algo, filename='svd_model.pkl'):
    """
    Salva o modelo treinado em um arquivo.
    """
    with open(filename, 'wb') as f:
        pickle.dump(algo, f)


if __name__ == "__main__":
    train_and_save_model()