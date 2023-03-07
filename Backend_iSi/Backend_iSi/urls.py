from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from chat.views import CreateThread, ThredsListByUser, CreateReadMessage, MarkReadMassages

router = routers.DefaultRouter()
router.register('thread', CreateThread, basename='create_delite')
router.register('all-Threds', ThredsListByUser, basename='all_threads')
router.register('messages', CreateReadMessage, basename='read_write_messsage')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mark-read/', MarkReadMassages.as_view(), name='mark_read_messsage')
]
