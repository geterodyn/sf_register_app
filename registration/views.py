import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import RegisterForm
from .models import User


USERFILE='users.txt'

def load_from_file(filename):
    all_users = {}
    try:
        with open(filename) as file:
            all_users = json.loads(file.read())
    except:
        pass
    return all_users

class RegisterToFile(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        warn_message = ''
        if form.is_valid():
            cd = form.cleaned_data
            all_users = load_from_file(USERFILE)
            if cd['login'] in all_users:
                warn_message = 'Такой пользователь уже существует!'
            else:
                user_dict = {cd['login']: cd['password']}
                all_users.update(user_dict)
                with open(USERFILE, 'w') as file:
                    json.dump(all_users, file)
                return HttpResponse('<h1>User registered</h1><br/><a href="/">Home</a>')
        return render(request, 'registration/start.html', {'form': form, 'message': warn_message})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'registration/start.html', {'form': form})

class RegisterToDb(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        warn_message = ''
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(login=cd['login']):
                warn_message = 'Такой пользователь уже существует!'
            else:
                user = User(**cd)
                user.save()
                return HttpResponse('<h1>User registered</h1><br/><a href="/todb">Home</a>')
        return render(request, 'registration/start.html', {'form': form, 'message': warn_message})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'registration/start.html', {'form': form})