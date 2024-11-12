import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .services import FriendService
from .models import *
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async



class OnlineFriendsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[1]
        validated_token = JWTAuthentication().get_validated_token(token)
        self.user = await sync_to_async(JWTAuthentication().get_user)(validated_token)

        if self.user.is_authenticated:
            self.user_data = await sync_to_async(UserData.objects.get)(user=self.user)

            # Aceitar a conexão primeiro
            await self.accept()

            # Marcar o usuário como online
            await self.update_online_status(True)

            # Pegar amigos online
            online_friends = await self.get_online_friends()

            # Enviar a lista de amigos online para o cliente
            await self.send(text_data=json.dumps({'online_friends': online_friends}))

            # Adicionar o usuário ao grupo
            self.group_name = f'user_{self.user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            friends = await sync_to_async(FriendService.get_friends)(self.user.id)
            for friend in friends:
                valid_friend_group_name = f"user_{friend['user_tag'].replace('@', '').replace('#', '')}"
                await self.channel_layer.group_add(
                valid_friend_group_name,
                self.channel_name
            )
                
            await self.channel_layer.group_send(
                    valid_friend_group_name,
                    {
                        'type': 'online_friends_update',
                        'online_friends': online_friends
                    }
                )

        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user'):
            # Marcar o usuário como offline
            await self.update_online_status(False)

            # Remover o usuário do grupo
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

            # Enviar a lista atualizada de amigos online para todos os clientes
            online_friends = await self.get_online_friends()
            friends = await sync_to_async(FriendService.get_friends)(self.user.id)
            if friends:  # Verificar se o usuário tem amigos antes de enviar atualização
                    for friend in friends:
                        valid_friend_group_name = f"user_{friend['user_tag'].replace('@', '').replace('#', '')}"
                        await self.channel_layer.group_send(
                            valid_friend_group_name,
                            {
                                'type': 'online_friends_update',
                                'online_friends': online_friends
                            }
                        )

    async def receive(self, text_data):
        pass

    async def online_friends_update(self, event):
        online_friends = event['online_friends']
        print("Enviando lista atualizada de amigos online:", online_friends)  # Adicione esse log
        await self.send(text_data=json.dumps({'online_friends': online_friends}))

    @sync_to_async
    def update_online_status(self, is_online):
        self.user_data.is_online = is_online    
        self.user_data.save()

    @sync_to_async
    def get_online_friends(self):
        return FriendService.get_online_friends(self.user.id)
    



from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Adicionar o usuário ao grupo da sala
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        
        # Enviar a mensagem para o grupo WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',  # Chama o método send_message
                'message': data,
            }
        )

       
        

    async def send_message(self, event):
        data = event['message']
        print(f"Enviando mensagem recebida do frontend para o grupo: {data}")
        res_data = await self.create_message(data=data)

        if res_data:
            # Serializa a mensagem criada
            serialized_data = await database_sync_to_async(lambda: MessageSerializer(res_data).data)()
            print('Enviando para o frontend:', serialized_data)
            await self.send(text_data=json.dumps({'message': serialized_data}))
        #else:
            # print("Erro: Mensagem não foi criada corretamente.")

        


    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_room(self, room_name):
        return Room.objects.get(name=room_name)

    @database_sync_to_async
    def create_message(self, data):
        room, created = Room.objects.get_or_create(name=data['room_name'])
        if not Message.objects.filter(content=data['message'], room=room).exists():
            sender = User.objects.get(id=data['sender'])  
            new_message = Message.objects.create(room=room, sender=sender, content=data['message'])
            return new_message
