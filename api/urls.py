from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrashLocationViewSet, RewardViewSet, UserViewSet, LoginView

router = DefaultRouter()
router.register(r'trash-locations', TrashLocationViewSet, basename='trash-location')
router.register(r'rewards', RewardViewSet)
router.register(r'users', UserViewSet)  # Add User resource

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

]
