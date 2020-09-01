from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class ViewAddMission(LoginRequiredMixin, View):
    template = 'pages/mission_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Mission'})
    
class ViewDetailMission(LoginRequiredMixin, View):
    template = 'pages/donation_detail.html'
    def get(self, request, id_mission):
        datas = db.collection('Donations').where('mis_id', '==', id_mission).stream()
        list_donation = []
        list_amount = []
        for donation in datas:
            dict_member = donation.to_dict()
            dict_member['id'] = donation.id
            list_donation.append(dict_member)
            list_amount.append(donation.to_dict()['amount'])
        return render(request, self.template, {'data':list_donation, 'title':'Detail', 'total':"{:,.2f}".format(sum(list_amount))})
    
class ViewListMission(LoginRequiredMixin, View):
    template = 'pages/mission_list.html'
    def get(self, request):
        data_ref = db.collection('Missions')
        data_mission = data_ref.stream()
        list_mission = []
        
        for mission in data_mission:
            dict_member = mission.to_dict()
            dict_member['id'] = mission.id
            dict_member['t'] = "{:,.2f}".format(float(dict_member['target']))
            # print(dict_member['t'])
            list_money = []
            for item in dict_member['collected']:
                list_money.append(float(item))
            dict_member['total'] = "{:,.2f}".format(sum(list_money))#Rp di awal jika mau pake rp
            # print(dict_member['total'])
            list_mission.append(dict_member)
        return render(request, self.template, {'title': 'List Mission', 'data':list_mission})
    
class ViewUpdateFormMission(LoginRequiredMixin, View):
    template = 'pages/mission_update_form.html'
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions').document(id_mission)
        collection = ref_mission.get()
        return render(request, self.template, {'title':'Update Mission','data':collection.to_dict(),'id':id_mission})

class ViewUpdateImageMission(LoginRequiredMixin, View):
    template = 'pages/mission_update_image.html'
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions').document(id_mission)
        collection = ref_mission.get()
        data_mission = collection.to_dict()
        list_image = []
        list_image.append({'link':data_mission['photo'], 'type':'Title'})
        for item in data_mission['photos']:
            list_image.append({'link':item, 'type':'Collection'})
        
        return render(request, self.template,{'title':'Update Image','data':list_image,'id':id_mission})

class ViewUpdateReport(LoginRequiredMixin, View):
    template = 'pages/mission_report.html'
    def get(self, request, id_mission):
        ref =  db.collection('Missions').document(id_mission)
        collection = ref.get()
        list_ = []
        list_.append({'report':collection.to_dict()['report']})  
        print(list_)    
        return render(request, self.template,{'title':'Update Report','data':list_, 'id':id_mission})
        
class PostUpdateReport(LoginRequiredMixin, View):
    def post(self, request):
        report = request.POST['report']
        id = request.POST['id']
        ref = db.collection('Missions').document(id)
        ref.update({'report':report})
        return HttpResponse('OK')

class DeleteMission(LoginRequiredMixin, View):
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions')
        doc_mission= ref_mission.stream()
        for mission in doc_mission:
            if mission.id == id_mission:
                mission.reference.delete()
        return redirect('mission:list')
  
class PostAddMission(LoginRequiredMixin, View):
    def post(self, request):
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
        target = request.POST['target']
        photo = request.POST['photo']
        kind = request.POST.get('type')
        detail = request.POST['detail']
        photos = request.POST['photos']
        photos = photos.split(",")
        while("" in photos) : 
            photos.remove("") 
        data = {
        'title':title,
        'start': start,
        'end': end,
        'target':target,
        'photo':photo,
        'type':kind,
        'detail': detail,
        'photos':photos,
        'report':'-',
        'collected':['0']
        
    }
        db.collection('Missions').document().set(data)
        return redirect('mission:list')
    
class PostUpdateFormMission(LoginRequiredMixin, View):
    
    def post(self, request, id_mission):
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
        target = request.POST['target']
        kind = request.POST.get('type')
        detail = request.POST['detail']
        # for item in photos:
        #     if len(item) < 10 :
        #         photos.remove(item)
        data = {
        'title':title,
        'start': start,
        'end': end,
        'target':target,
        'type':kind,
        'detail': detail,
        
    }
        ref = db.collection('Missions').document(id_mission)
        ref.update(data)
        return redirect('mission:list')

class DeleteImageCollection(LoginRequiredMixin, View):
    
    def post(self, request):
        id_mission = request.POST.get('id')
        link_photo = request.POST.get('path')
        ref = db.collection('Missions').document(id_mission)
        ref.update({"photos": ArrayRemove([link_photo])})
        return HttpResponse('OK')
        #return redirect('mission:update-image', id_mission = id_mission)

class UpdateImageTitle(LoginRequiredMixin, View):
    def post(self, request):
        id_mission = request.POST['id']
        link_photo = request.POST['path']
        ref = db.collection('Missions').document(id_mission)
        ref.update({'photo':link_photo})
        return HttpResponse('OK')

class UpdateImageCollection(LoginRequiredMixin, View):
    def post(self, request):
        id_mission = request.POST['id']
        link_photo = request.POST['path']
        link_photo = link_photo.split(',')
        ref = db.collection('Missions').document(id_mission)
        ref.update({"photos": ArrayUnion(link_photo)})
        return HttpResponse('OK')