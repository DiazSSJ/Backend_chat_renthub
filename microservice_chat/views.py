from django.shortcuts import render
from rest_framework import generics
from microservice_chat.models import User, Profile, ChatMessage
from rest_framework.permissions import AllowAny
from microservice_chat.serializer import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
import requests


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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
            if info_user != None:
                crear_usuario(id_user, info_user.name, info_user.last_name)
            
        ##Si receiver no esta creado
        if not User.objects.filter(id_origin = id_receiver).exists():
            ##se debe crear el usuario en los modelos y luego si crear el mensaje 
            info_receiver = get_user_api(id_user)
            if info_receiver != None:
                crear_usuario(info_receiver, info_receiver.name, info_receiver.last_name)
        
        #buscar el usuario que envia el mensaje y el que recibe el mensaje 
        user =  User.objects.get(id_origin = id_user)
        sender =  User.objects.get(id_origin = id_sender)
        receiver =  User.objects.get(id_origin = id_receiver)


        object_message = ChatMessage(
            user = user,
            sender = sender, 
            receiver = receiver,
            message = message
        )

        object_message.save()

        # Verificar que el objeto se haya creado correctamente
        if object_message.id:
            return Response({'message': 'Mensaje creado exitosamente.'}, status=status.HTTP_201_CREATED)
        else: 
            #Algo salio mal al crear el objeto 
            return Response({'message': 'Error al crear el mensaje.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_user_api(id):
    url = 'http://url_del_otro_microservicio/endpoint/'+str(id)  # Reemplaza con la URL real del otro microservicio y el endpoint que deseas acceder
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
    serializer = RegisterSerializer(data={'id_origin': id_origin, 'name': name, 'last_name': last_name})

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
        
     
"""
from .serializers import RegisterSerializer

def crear_usuario(id_origin, name, last_name):
    # Crear una instancia del serializador con los datos proporcionados
    serializer = RegisterSerializer(data={'id_origin': id_origin, 'name': name, 'last_name': last_name})

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

crear_usuario(id_origin=1, name='John', last_name='Doe')

pip install requests


import requests

def obtener_informacion_de_otros_microservicio():
    url = 'http://url_del_otro_microservicio/endpoint/'  # Reemplaza con la URL real del otro microservicio y el endpoint que deseas acceder
    respuesta = requests.get(url)

    if respuesta.status_code == 200:  # Verifica si la respuesta fue exitosa (código de estado 200)
        datos = respuesta.json()  # Si el contenido es JSON, puedes usar .json() para obtener los datos como un diccionario de Python
        return datos
    else:
        # Si la respuesta no fue exitosa, puedes manejar el error aquí
        print(f'Error al obtener datos del otro microservicio. Código de estado: {respuesta.status_code}')
        return None



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class ObtenerInformacionView(APIView):
    def post(self, request):
        # Obtén los datos que necesitas para hacer la solicitud al otro microservicio
        id = request.data.get('id')  # Por ejemplo, si necesitas un ID para obtener información específica
        
        # Realiza la solicitud al otro microservicio
        url = 'http://url_del_otro_microservicio/endpoint/'  # Reemplaza con la URL real del otro microservicio y el endpoint que deseas acceder
        respuesta = requests.get(url, params={'id': id})

        if respuesta.status_code == 200:
            datos = respuesta.json()
            return Response(datos, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error al obtener datos del otro microservicio.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
path('obtener_informacion/', ObtenerInformacionView.as_view(), name='obtener_informacion')

"""