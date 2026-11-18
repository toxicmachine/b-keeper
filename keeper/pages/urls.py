from django.conf import settings
from django.urls import path
from django.shortcuts import redirect
from . import views


urlpatterns = [
    path('', views.KeeperMainPage.as_view(), name='main'),
    path('get_keeper_object/', views.get_keeper_object, name='get_keeper_object'),
    path('editor/', views.KeeperEditorPage.as_view(), name='editor'),
    path('editor/check_is_folder_exist/', views.check_is_folder_exist, name='check_is_folder_exist'),
    path('editor/add_object_in_keeper/', views.add_object_in_keeper, name='add_object_in_keeper'),
    path('type-objects/', views.KeeperTypePage.as_view(), name='type-objects'),
]