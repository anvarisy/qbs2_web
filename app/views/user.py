from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from django.http import HttpResponse
from firebase_admin import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class ViewUser(View):
    template = 'pages/user_list.html'
    def get(self, request):
        list_ = []
        for user in auth.list_users().iterate_all():
            list_.append({'uid':user.uid,'email':user.email, 'status':user.disabled})
        print(list_)
        return render(request, self.template,{'title':'List User', 'data':list_})

class ViewLogin(LoginView):
    template_name = 'pages/page-signin.html'
    success_url = reverse_lazy('home')

class PostLogin(View):
    status = ''
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            status = 'OK'
        else:
            status = 'FAIL'
        return HttpResponse(status)

class PostLogout(View):
    def get(self, request):
        logout(request)
        return redirect('home')