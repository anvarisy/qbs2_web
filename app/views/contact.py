from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ViewAddContact(LoginRequiredMixin, View):
    template = 'pages/contact_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Contact'})
    
class ViewListContact(LoginRequiredMixin, View):
    template = 'pages/contact_list.html'
    def get(self, request):
        data_ref = db.collection('Contact')
        data_contact = data_ref.stream()
        list_contact = []
        for contact in data_contact:
            dict_member = contact.to_dict()
            dict_member['id'] = contact.id
            list_contact.append(dict_member)
        return render(request, self.template, {'title': 'List Contact', 'data':list_contact})
    
class ViewUpdateContact(LoginRequiredMixin, View):
    template = 'pages/contact_form.html'
    def get(self, request, id_contact):
        ref_contact = db.collection('Contact').document(id_contact)
        collection = ref_contact.get()
        return render(request, self.template, {'title':'Update Contact','data':collection.to_dict(),'id':id_contact})

class DeleteContact(LoginRequiredMixin, View):
    def get(self, request, id_contact):
        contact_ref = db.collection('Contact')
        contact_doc = contact_ref.stream()
        for contact in contact_doc:
            if contact.id == id_contact:
                contact.reference.delete()
        return redirect('contact:list')

def getData(request):
    contact_icon = request.POST['contact_icon']
    contact_link = request.POST['contact_link']
    contact_type = request.POST['contact_type']
    data = {
        'contact_icon':contact_icon,
        'contact_link':contact_link,
        'contact_type':contact_type
        
    }
    return data

class PostAddContact(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Contact').document().set(getData(request))
        return redirect('contact:list')
    
class PostUpdateContact(LoginRequiredMixin, View):
    def post(self, request, id_contact):
        ref = db.collection('Contact').document(id_contact)
        ref.update(getData(request))
        return redirect('contact:list')
