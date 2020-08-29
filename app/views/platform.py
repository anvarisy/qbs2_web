from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
# Create your views here.

class ViewAddPlatform(LoginRequiredMixin, View):
    template = 'pages/platform_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Platform'})
    
class ViewListPlatform(LoginRequiredMixin, View):
    template = 'pages/platform_list.html'
    def get(self, request):
        data_ref = db.collection('Article')
        data_platform = data_ref.stream()
        list_platform = []
        for platform in data_platform:
            dict_member = platform.to_dict()
            dict_member['id'] = platform.id
            list_platform.append(dict_member)
        return render(request, self.template, {'title': 'List Platform', 'data':list_platform})
    
class ViewUpdatePlatform(LoginRequiredMixin, View):
    template = 'pages/platform_form.html'
    def get(self, request, id_platform):
        ref_platform= db.collection('Article').document(id_platform)
        collection = ref_platform.get()
        return render(request, self.template, {'title':'Update Platform','data':collection.to_dict(),'id':id_platform})

class DeletePlatform(LoginRequiredMixin, View):
    def get(self, request, id_platform):
        ref_platform = db.collection('Article')
        doc_platform = ref_platform.stream()
        for platform in doc_platform:
            if platform.id == id_platform:
                platform.reference.delete()
        return redirect('platform:list')
    
    
def getData(request):
    platform_name = request.POST['title']
    platform_detail= request.POST['detail']
    platform_icon = request.POST['image']
    data = {
        'title':platform_name,
        'date':date.today().strftime("%m-%d-%Y"),
        'image':platform_icon,
        'detail':platform_detail
    }
    return data

class PostAddPlatform(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Article').document().set(getData(request))
        return redirect('platform:list')
    
class PostUpdatePlatform(LoginRequiredMixin, View):
    def post(self, request, id_platform):
        ref = db.collection('Article').document(id_platform)
        ref.update(getData(request))
        return redirect('platform:list')
    

