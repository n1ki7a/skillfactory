from django.urls import path

from . import views
from .views import ProfileDetail, ProfileEdit

urlpatterns = [
    path('profile/', ProfileDetail.as_view(), name='profile_view'),
    path('profile/edit/', ProfileEdit.as_view(), name='profile_edit'),
    path('upgrade/', views.upgrade_me, name='upgrade'),
]