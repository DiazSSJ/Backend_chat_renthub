from django.shortcuts import render
from django.db.models import OuterRef, Subquery     
from django.db.models import Q, Max, F, Min
from rest_framework import generics
from microservice_chat.models import User, Profile, ChatMessage
from rest_framework.permissions import AllowAny
from microservice_chat.serializer import RegisterSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
import requests


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class DeleteMessages(generics.DestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['reciever_id']

        sender_user = User.objects.filter(id_origin=sender_id).first()
        receiver_user = User.objects.filter(id_origin=receiver_id).first()

        # Verifica si los usuarios existen antes de borrar mensajes
        if sender_user and receiver_user:
            messages_to_delete = ChatMessage.objects.filter(
                sender__in=[sender_user.id, receiver_user.id],
                receiver__in=[sender_user.id, receiver_user.id]
            )

            # Borra los mensajes encontrados
            messages_to_delete.delete()

            return Response({"message": "Mensajes eliminados correctamente"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Puedes manejar el caso donde uno o ambos usuarios no existen
            return Response({"error": "Uno o ambos usuarios no existen"}, status=status.HTTP_404_NOT_FOUND)

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get('user_id')
        #user_id = self.kwargs['user_id']

        # Obtener el usuario actual
        user = User.objects.filter(id_origin=user_id).first()

        if user:
            # Obtener los últimos mensajes para cada conversación
            messages = ChatMessage.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).order_by('-id').values('sender', 'receiver','id').annotate(last_message= Max('id'))

            # Obtener los mensajes correspondientes a esas fechas
            chat_ids = set()
            unique_messages = []
            
            for message in messages:
                chat_id = tuple(sorted([message['sender'], message['receiver']]))
                
                if chat_id not in chat_ids:
                    chat_ids.add(chat_id)
                    unique_messages.append(message['last_message'])
            
            # Obtener los mensajes finales
            messages = ChatMessage.objects.filter(id__in=unique_messages).order_by("-id")

            res = []

            for menssage in messages:
                print(menssage)
                data = {
                    'id':menssage.id,
                    'texto': menssage.message,
                    'date': menssage.date,
                    'is_read':menssage.is_read,

                    'id_sender': menssage.sender.id,
                    'name_sender': menssage.sender.name,
                    'last_name_sender': menssage.sender.last_name,

                    'id_receiver': menssage.receiver.id,
                    'name_receiver': menssage.receiver.name,
                    'last_name_receiver': menssage.receiver.last_name,
                }
                
                res.append(data)


            return Response( {'mensajes': res}, status=status.HTTP_200_OK)

        return Response( {'mensajes': []}, status=status.HTTP_404_NOT_FOUND)
    

class filterMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def post(self, request):
  
        user_id = request.data.get('user_id')
        search_text = request.data.get('filter') 

        # Obtener el usuario actual
        user = User.objects.filter(id_origin=user_id).first()

        if user:
            # Obtener los últimos mensajes para cada conversación
            messages = ChatMessage.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).order_by('-id').values('sender', 'receiver','id').annotate(last_message= Max('id'))

            # Obtener los mensajes correspondientes a esas fechas
            chat_ids = set()
            unique_messages = []
            
            for message in messages:
                chat_id = tuple(sorted([message['sender'], message['receiver']]))
                
                if chat_id not in chat_ids:
                    chat_ids.add(chat_id)
                    unique_messages.append(message['last_message'])

            filter_id = User.objects.filter(~Q(id_origin=user_id), Q(name__icontains=search_text) ) 
            
            
            # Obtener los mensajes finales
            messages = ChatMessage.objects.filter(Q(id__in=unique_messages), Q(sender__in=filter_id)| Q(receiver__in=filter_id)).order_by("-id")

            res = []

            for menssage in messages:
                print(menssage)
                data = {
                    'id':menssage.id,
                    'texto': menssage.message,
                    'date': menssage.date,
                    'is_read':menssage.is_read,

                    'id_sender': menssage.sender.id,
                    'name_sender': menssage.sender.name,
                    'last_name_sender': menssage.sender.last_name,

                    'id_receiver': menssage.receiver.id,
                    'name_receiver': menssage.receiver.name,
                    'last_name_receiver': menssage.receiver.last_name,
                }
                
                res.append(data)


            return Response( {'mensajes': res}, status=status.HTTP_200_OK)


        return Response( {'mensajes': []}, status=status.HTTP_404_NOT_FOUND)
    

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']

        senderUser = User.objects.filter(id_origin = sender_id).first()
        recieverUser = User.objects.filter(id_origin = reciever_id).first()

        # Verifica si los usuarios existen antes de buscar mensajes
        if senderUser and recieverUser:
            messages = ChatMessage.objects.filter(
                sender__in=[senderUser.id, recieverUser.id],
                receiver__in=[senderUser.id, recieverUser.id]
            )
            return messages
        else:
            # Puedes manejar el caso donde uno o ambos usuarios no existen
            return ChatMessage.objects.none()


class SendMessages(generics.CreateAPIView):
    """
    Esta vista permite registrar un nuevo mensaje a un usuario 
    Atributos:
        - permission_classes: Lista de permisos requeridos para acceder a la vista.
    Métodos:
        - post: Maneja la solicitud POST para crear un nuevo mensaje.
    """

    permission_classes = (AllowAny,)

    def post(self, request):

        id_user = request.data.get('user')
        id_sender = request.data.get('sender')
        id_receiver = request.data.get('receiver')

        message = request.data.get('message')

        
        ##Si user no esta creado
        if not User.objects.filter(id_origin = id_user).exists():
            ##se debe crear el usuario en los modelos y luego si crear el mensaje 
            info_user = get_user_api(id_user)
            print(info_user)
            if info_user != None:
                crear_usuario(id_user, info_user['nombre'], info_user['apellido'])
            else:
                return Response({'message': 'No se encuentra el usuario'}, status=status.HTTP_404_NOT_FOUND)
            
        ##Si receiver no esta creado
        if not User.objects.filter(id_origin = id_receiver).exists():
            ##se debe crear el usuario en los modelos y luego si crear el mensaje 
            info_receiver = get_user_api(id_receiver)
            print(info_receiver)
            if info_receiver != None:
                crear_usuario(id_receiver, info_receiver['nombre'], info_receiver['apellido'])
            else:
                return Response({'message': 'No se encuentra el usuario'}, status=status.HTTP_404_NOT_FOUND)

        
        #buscar el usuario que envia el mensaje y el que recibe el mensaje 
        user =  User.objects.get(id_origin = id_user)
        sender =  User.objects.get(id_origin = id_sender)
        receiver =  User.objects.get(id_origin = id_receiver)


        object_message = ChatMessage(
            user = user,
            sender = sender, 
            receiver = receiver,
            message = message,
        
        )

        object_message.save()

        # Verificar que el objeto se haya creado correctamente
        if object_message.id:
            return Response({'message': 'Mensaje creado exitosamente.'}, status=status.HTTP_201_CREATED)
        else: 
            #Algo salio mal al crear el objeto 
            return Response({'message': 'Error al crear el mensaje.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



#para probar
class get_id_receiver(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        id = request.data.get('id')
        message = ChatMessage.objects.get(id = id)
        return Response({'nombre':  message.user.name })

def get_user_api(id):
    url = 'https://django-render-renthub-app.onrender.com/login/obtener-usuario/'+str(id)+'/'  # Reemplaza con la URL real del otro microservicio y el endpoint que deseas acceder
    respuesta = requests.get(url)

    if respuesta.status_code == 200:  # Verifica si la respuesta fue exitosa (código de estado 200)
        datos = respuesta.json()  # Si el contenido es JSON, puedes usar .json() para obtener los datos como un diccionario de Python
        return datos
    else:
        # Si la respuesta no fue exitosa, puedes manejar el error aquí
        print(f'Error al obtener datos del otro microservicio. Código de estado: {respuesta.status_code}')
        return None

def crear_usuario(id_origin, name, last_name):
    # Crear una instancia del serializador con los datos proporcionados
    username = f'user_{id_origin}'
    serializer = RegisterSerializer(data={'id_origin': id_origin, 'name': name, 'last_name': last_name, 'username': username})

    # Verificar si los datos son válidos
    if serializer.is_valid():
        # Crear el usuario utilizando el método `create` del serializador
        usuario_creado = serializer.save()
        return usuario_creado
    else:
        # Si los datos no son válidos, puedes manejar el error aquí
        # Por ejemplo, puedes imprimir los errores de validación
        print(serializer.errors)
        return None

