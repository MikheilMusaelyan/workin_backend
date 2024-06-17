from django.urls import path
from rest_framework_simplejwt import views
from base.views import MessageView;

urlpatterns = [
    # path('login/', LoginView.as_view(), name='token_obtain_pair'),
    # path('signup/', SingupView.as_view(), name='signup'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('message/<pk>/', MessageView.as_view(), name='message'),
    
    # path('search/<date>/<start>/<name>/', SearchEvents.as_view(), name='s'),
]