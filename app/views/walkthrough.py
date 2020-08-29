from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin


class ViewAddWalkthrough(View):
    template = 'pages/walkthrough_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Walkthrough'})

class ViewUpdateWalkthrough(View):
    template = 'pages/walkthrough_form.html'
    def get(self, request, id_walk):
        ref_walk = db.collection('Walk').document(id_walk)
        collection = ref_walk.get()
        return render(request, self.template, {'title':'Update Walkthrough', 'data':collection.to_dict(), 'id':id_walk})

class PostAddWalk(View):
    def post(self, request):
        db.collection('Walk').document().set(getData(request))
        return redirect('walk:list')
    
class PostUpdateWalk(View):
    def post(self, request, id_walk):
        ref = db.collection('Walk').document(id_walk)
        ref.update(getData(request))
        return redirect('walk:list')
 
class DeleteWalk(View):
    def get(self, request, id_walk):
        ref_walk = db.collection('Walk')
        doc_walk= ref_walk.stream()
        for walk in doc_walk:
            if walk.id == id_walk:
                walk.reference.delete()
        return redirect('walk:list')
    
class ViewListWalk(View):
    template = 'pages/walkthrough_list.html'
    def get(self, request):
        data_ref = db.collection('Walk')
        data_walk = data_ref.stream()
        list_walk = []
        for walk in data_walk:
            dict_member = walk.to_dict()
            dict_member['id'] = walk.id
            list_walk.append(dict_member)
        return render(request, self.template, {'title':'List Walkthrough', 'data':list_walk})
    
def getData(request):
    title = request.POST['title']
    position = request.POST['position']
    detail = request.POST['detail']
    image = request.POST['image']
    data = {
        'title':title,
        'position':position,
        'detail':detail,
        'image':image
    }
    return data
    