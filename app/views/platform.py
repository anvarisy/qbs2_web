from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db

# Create your views here.

class ViewAddPlatform(View):
    template = 'pages/platform_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Platform'})
    
class ViewListPlatform(View):
    template = 'pages/platform_list.html'
    def get(self, request):
        data_ref = db.collection('Platform')
        data_platform = data_ref.stream()
        list_platform = []
        for platform in data_platform:
            dict_member = platform.to_dict()
            dict_member['id'] = platform.id
            list_platform.append(dict_member)
        return render(request, self.template, {'title': 'List Platform', 'data':list_platform})
    
class ViewUpdatePlatform(View):
    template = 'pages/platform_form.html'
    def get(self, request, id_platform):
        ref_platform= db.collection('Platform').document(id_platform)
        collection = ref_platform.get()
        return render(request, self.template, {'title':'Update Platform','data':collection.to_dict(),'id':id_platform})

class DeletePlatform(View):
    def get(self, request, id_platform):
        ref_platform = db.collection('Platform')
        doc_platform = ref_platform.stream()
        for platform in doc_platform:
            if platform.id == id_platform:
                platform.reference.delete()
        return redirect('platform:list')
    
    
def getData(request):
    platform_name = request.POST['platform_name']
    platform_detail= request.POST['platform_detail']
    platform_icon = request.POST['platform_icon']
    data = {
        'platform_name':platform_name,
        'platform_icon':platform_icon,
        'platform_detail':platform_detail
    }
    return data

class PostAddPlatform(View):
    def post(self, request):
        db.collection('Platform').document().set(getData(request))
        return redirect('platform:list')
    
class PostUpdatePlatform(View):
    def post(self, request, id_platform):
        ref = db.collection('Platform').document(id_platform)
        ref.update(getData(request))
        return redirect('platform:list')
    

