from django.urls import path, re_path
from .views import ListUsers,UsersDetail,ListUserProfile,DetailUserProfile, hello_api, profiles_list, profiles_detail

app_name = 'profiles_api'

urlpatterns = [
    path('',hello_api,name='hello'),
    path('profiles-list/',profiles_list,name='profiles-list'),
    path('profiles-detail/<int:pk>/',profiles_detail,name='profiles-detail'),
    path('profiles/',ListUsers.as_view(), name='profiles'),
    path('profiles/<int:pk>/',UsersDetail.as_view(), name='profiles-detail'),
    path('userprofiles/',ListUserProfile.as_view(),name='user-profiles'),
    path('userprofiles/<int:pk>/',DetailUserProfile.as_view(),name='user-profiles-detail'),
]