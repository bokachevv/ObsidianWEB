from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.i18n import set_language
from django.contrib.auth import views as auth_views
from . import views
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Главная страница
    path('hello/', views.hello_world, name='hello_world'),  # Приветствие
    path('obsidian/<str:filename>/', views.markdown_view, name='markdown_view'),  # Просмотр файла
    path('set-language/', set_language, name='set_language'),  # Установка языка
    path('goals/', views.goals_page, name='goals_page'),  # Страница целей
    path('login/', views.login_page, name='login_page'),  # Страница логина
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('api/', include(router.urls)),
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('create_note/', views.create_note, name='create_note'),
    path('api/notes/', views.NoteListView.as_view(), name='note-list'),  # Заметь, что путь заканчивается на "/"

]