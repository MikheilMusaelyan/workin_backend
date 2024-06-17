from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.models import CustomUser, Message
from base.serializers import MessageSerializer, CustomUserSerializer

from datetime import datetime
from django.db.models import Q
from datetime import datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# import math

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        # now = datetime.now()
        # year = now.year
        # month = str(now.month).zfill(2)
        
        # events = Event.objects.filter(date__year=year, date__month=month, userId=user.id)
        # eventSerializer = EventSerializer(events, many=True)
        
        # dateObject = {}

        # for event in eventSerializer.data:
            
        #     dayObject = datetime.strptime(event['date'], '%Y-%m-%d')
        #     formatted_date = dayObject.strftime("%B %d, %Y")
        #     day = dayObject.day

        #     if f'd{day}' not in dateObject:
        #         dateObject[f'd{day}'] = []
            
        #     event['color'] = {
        #         'name' : event['color'],
        #         'pastel': True
        #     }
        #     event['date'] = formatted_date
            
        #     dateObject[f'd{day}'].append(event)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            # 'events': dateObject,
        }, status=status.HTTP_200_OK)

class SingupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.create_user(email=email, password=password, **kwargs,)
        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class MessageView(APIView):
    def get(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
            messageSerializer = MessageSerializer(message)
            response_data = messageSerializer.data
            
            # checking if replied to something
            replyTo = message.replyTo
            replySerializer = None
            if replyTo is not None:
                Message.objects.get(id=replyTo.id)
                replySerializer = MessageSerializer(replyTo)
                response_data['replyTo'] = replySerializer.data

            # not serializing because only returned email so i included other fields too as a string
            author = CustomUser.objects.get(id=messageSerializer.data['author'])

            response_data['author'] = {
                "id": author.id,
                "email": author.email,
                "is_staff": author.is_staff
            }
            
            return Response(
                response_data,
                status=status.HTTP_200_OK
            )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        