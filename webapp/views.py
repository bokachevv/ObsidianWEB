from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .models import Note
from django.http import JsonResponse
from django.shortcuts import render
from .models import Note
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .forms import NoteForm
from django.http import JsonResponse
from rest_framework import generics
from .serializers import NoteSerializer
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
import markdown2
import re
import os

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NoteList(APIView):
    def get(self, request, format=None):
        notes = Note.objects.all()  # Получаем все заметки из базы данных
        serializer = NoteSerializer(notes, many=True)  # Сериализуем их
        return Response(serializer.data)  # Возвращаем сериализованные данные

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)  # Принимаем данные из запроса
        if serializer.is_valid():  # Проверяем их на валидность
            serializer.save()  # Сохраняем данные в базе
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Возвращаем созданный объект
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteListView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

def hello_world(request):
    return HttpResponse("Hello, world!")

def note_list(request):
    response = requests.get("http://127.0.0.1:8000/api/notes/")
    notes = response.json()  # Получаем данные о заметках в формате JSON
    return render(request, "note_list.html", {"notes": notes})


def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return JsonResponse({'error': 'Title and content are required!'}, status=400)

        # Создаем заметку
        note = Note(title=title, content=content)
        note.save()

        return JsonResponse({'message': 'Note created successfully!'})

    return render(request, 'create_note.html')

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

def note_edit(request, pk):
    note = Note.objects.get(pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_form.html', {'form': form})

def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    return redirect('note_list')

def homepage(request):
    return render(request, 'homepage.html')

def goals_page(request):
    return render(request, 'goals.html')

def login_page(request):
    # Если пользователь уже залогинен, перенаправляем на главную страницу
    if request.user.is_authenticated:
        return redirect('homepage')

    # Основная логика авторизации
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Если remember_me есть, сохраняем сессию на SESSION_COOKIE_AGE
            if remember_me == 'on':  # Чекбокс вернет 'on', если отмечен
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            response = redirect('homepage')
            response.set_cookie('login', username)  # Устанавливаем куки с логином

            return response
        else:
            messages.error(request, "Wrong username or password.")

    return render(request, 'login_page.html')


def convert_obsidian_links(content):
    link_pattern = r'\[\[([^\]]+)\]\]'

    def replace_link(match):
        filename = match.group(1).replace(' ', '_')
        return f'<a href="/obsidian/{filename}/">{match.group(1)}</a>'

    return re.sub(link_pattern, replace_link, content)

@login_required
def markdown_view(request, filename):
    md_dir = os.path.join('/Users/bokachev/djangoweb/webapp/Markdown')
    file_path = os.path.join(md_dir, f'{filename}.md')

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()

        html_content = markdown2.markdown(content)
        html_content = convert_obsidian_links(html_content)

        return render(request, 'markdown.html', {'content': html_content})

    return render(request, '404.html')

from django.utils import translation
from django.shortcuts import redirect


def my_view(request):
    message = _("Привет мир!")
    return HttpResponse(message)
