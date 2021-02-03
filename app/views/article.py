from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
# Create your views here.

class ViewAddArticle(LoginRequiredMixin, View):
    template = 'pages/article/platform_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Article'})
    
class ViewListArticle(LoginRequiredMixin, View):
    template = 'pages/article/platform_list.html'
    def get(self, request):
        data_ref = db.collection('Article-Web')
        data_platform = data_ref.stream()
        list_platform = []
        for platform in data_platform:
            dict_member = platform.to_dict()
            dict_member['id'] = platform.id
            list_platform.append(dict_member)
        return render(request, self.template, {'title': 'List Article', 'data':list_platform})
    
class ViewUpdateArticle(LoginRequiredMixin, View):
    template = 'pages/article/platform_form.html'
    def get(self, request, id_article):
        ref_platform= db.collection('Article-Web').document(id_article)
        collection = ref_platform.get()
        return render(request, self.template, {'title':'Update Platform','data':collection.to_dict(),'id':id_article})

class DeleteArticle(LoginRequiredMixin, View):
    def get(self, request, id_article):
        ref_platform = db.collection('Article-Web')
        doc_platform = ref_platform.stream()
        for platform in doc_platform:
            if platform.id == id_article:
                platform.reference.delete()
        return redirect('article:list')
    
    
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

class PostAddArticle(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Article-Web').document().set(getData(request))
        return redirect('article:list')
    
class PostUpdateArticle(LoginRequiredMixin, View):
    def post(self, request, id_platform):
        ref = db.collection('Article-Web').document(id_platform)
        ref.update(getData(request))
        return redirect('article:list')
    

