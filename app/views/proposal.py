from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class ViewProposal(LoginRequiredMixin, View):
    template = 'pages/proposal_list.html'
    def get(self, request):
        ref = db.collection('Proposal')
        data = ref.stream()
        list_proposal = []
        for item in data :
            dict_ = item.to_dict()
            dict_['id'] = item.id
            list_proposal.append(dict_)
        return render(request, self.template, {'title':'Proposal','data':list_proposal})

class ViewTransaction(LoginRequiredMixin, View):
    template = 'pages/transaction_list.html'
    def get(self, request):
        ref = db.collection('s-transactions').where('mis_id','==','12345678')
        data = ref.stream()
        list_ = []
        for item in data:
            dict_ = item.to_dict()
            dict_ ['id']= item.id
            data = db.collection('User').document(item.to_dict()['p_uid']).get().to_dict()
            dict_['name'] = data['full_name']
            dict_['email'] = data['email']
            dict_['phone'] = data['phone']
            list_.append(dict_)
        print(list_)
        return render(request,self.template,{'title':'List Transaction', 'data':list_})

class ViewPengaduan(LoginRequiredMixin, View):
    template = 'pages/delation_list.html'
    def get(self, request):
        data = db.collection('Pengaduan').stream()
        list_ = []
        for item in data:
            dict_ = item.to_dict()
            dict_['id'] = item.id
            list_.append(dict_)
        return render(request, self.template, {'title':'Pengaduan', 'data':list_})