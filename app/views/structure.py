from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin

class ViewAddSctucture(LoginRequiredMixin, View):
    template = 'pages/struktur_form.html'
    def get(self, request):
        return render(request, self.template)

class ViewUpadateStructure(LoginRequiredMixin, View):
    template = 'pages/struktur_form.html'
    def get(self, request, id_structure):
        data = db.collection('Team').document(id_structure).get()
        return render(request, self.template,{'title':'Organisasi','data':data.to_dict(),'id':id_structure})
    
class ViewListStructure(LoginRequiredMixin, View):
    template = 'pages/struktur_list.html'
    def get(self, request):
        data = db.collection('Team').stream()
        list_ = []
        for item in data:
            dict_ = item.to_dict()
            dict_['id']= item.id
            list_.append(dict_)
        return render(request, self.template, {'title': 'List Team','data':list_})

class PostAddStructure(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Team').document().set(data(request))
        return redirect('structure:list')

class PostUpdateStructure(LoginRequiredMixin, View):
    def post(self, request, id_structure):
        db.collection('Team').document(id_structure).update(data(request))
        return redirect('structure:list')

class DeleteStructure(LoginRequiredMixin, View):
    def get(self, request, id_structure):
        ref_carousel = db.collection('Team')
        doc_carousel= ref_carousel.stream()
        for carousel in doc_carousel:
            if carousel.id == id_structure:
                carousel.reference.delete()
        return redirect('structure:list')

def data(request):
    name = request.POST['name']
    position = request.POST['position']
    wa = request.POST['wa']
    fb = request.POST['fb']
    ig = request.POST['ig']
    photo = request.POST['photo']
    pos = request.POST['pos']
    member = {
        'name':name,
        'wa':wa,
        'position':position,
        'fb':fb,
        'ig':ig,
        'photo':photo,
        'pos':pos
    }
    return member