from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class ViewProfil(LoginRequiredMixin, View):
    template = 'pages/profil_form.html'
    def get(self, request):
        profil_ref = db.collection('Profil')
        data_profil = profil_ref.stream()
        list_ = []
        for profil in data_profil:
           list_.append({'teks':profil.to_dict()['profil_vision'], 'type':'Visi'})
           list_.append({'teks':profil.to_dict()['profil_detail'], 'type':'Detail'})
           for misi in  profil.to_dict()['profil_mission'] :
               list_.append({'teks':misi,'type':'Misi'})
        return render(request, self.template, {'data': list_, 'id':profil.id})
    
class UpdateVisi(LoginRequiredMixin, View):
    def post(self, request):
        visi = request.POST['visi']
        id_profil = request.POST['id']
        data_ref = db.collection('Profil').document(id_profil)
        data_ref.update({'profil_vision':visi})
        return HttpResponse('OK')

class UpdateDetail(LoginRequiredMixin, View):
    def post(self, request):
        detail = request.POST['detail']
        id_profil = request.POST['id']
        data_ref = db.collection('Profil').document(id_profil)
        data_ref.update({'profil_detail':detail})
        return HttpResponse('OK')
        
class AddMisi(LoginRequiredMixin, View):
    def post(self, request):
        misi = request.POST['misi']
        id_profil = request.POST['id']
        data_ref = db.collection('Profil').document(id_profil)
        data_ref.update({'profil_mission': ArrayUnion([misi])})
        return HttpResponse('OK')

class DeleteMisi(LoginRequiredMixin, View):
    def post(self, request):
        misi = request.POST['misi']
        print(misi)
        id_profil = request.POST['id']
        data_ref = db.collection('Profil').document(id_profil)
        data_ref.update({'profil_mission': ArrayRemove([misi])})
        return HttpResponse('OK')

class ViewProfilImage(LoginRequiredMixin, View):
    template = 'pages/update_profil_image.html'
    def get(self, request):
        profil_ref = db.collection('Profil')
        data_profil = profil_ref.stream()
        list_ = []
        for profil in data_profil:
           for url in  profil.to_dict()['photo_collection'] :
               list_.append({'url':url})
        return render(request, self.template, {'data': list_, 'id':profil.id})

class DeleteProfilImage(LoginRequiredMixin, View):
    def post(self, request):
        id_profil = request.POST.get('id')
        link_photo = request.POST.get('path')
        ref = db.collection('Profil').document(id_profil)
        ref.update({"photo_collection": ArrayRemove([link_photo])})
        return HttpResponse('OK')
    
class AddCollection(LoginRequiredMixin, View):
    def post(self, request):
        path = request.POST['path']
        id_profil = request.POST['id']
        path = path.split(',')
        data_ref = db.collection('Profil').document(id_profil)
        data_ref.update({'photo_collection': ArrayUnion(path)})
        return HttpResponse('OK')