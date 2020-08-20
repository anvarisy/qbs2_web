from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
# Create your views here.

class ViewAddMission(View):
    template = 'pages/mission_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Mission'})
    
class ViewListMission(View):
    template = 'pages/mission_list.html'
    def get(self, request):
        data_ref = db.collection('Missions')
        data_mission = data_ref.stream()
        list_mission = []
        
        for mission in data_mission:
            dict_member = mission.to_dict()
            dict_member['id'] = mission.id
            dict_member['t'] = "{:,.2f}".format(float(dict_member['mission_target']))
            # print(dict_member['t'])
            list_money = []
            for item in dict_member['mission_collected']:
                list_money.append(float(item))
            dict_member['total'] = "{:,.2f}".format(sum(list_money))#Rp di awal jika mau pake rp
            # print(dict_member['total'])
            list_mission.append(dict_member)
        return render(request, self.template, {'title': 'List Mission', 'data':list_mission})
    
class ViewUpdateFormMission(View):
    template = 'pages/mission_update_form.html'
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions').document(id_mission)
        collection = ref_mission.get()
        return render(request, self.template, {'title':'Update Mission','data':collection.to_dict(),'id':id_mission})

class ViewUpdateImageMission(View):
    template = 'pages/mission_update_image.html'
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions').document(id_mission)
        collection = ref_mission.get()
        data_mission = collection.to_dict()
        list_image = []
        list_image.append({'link':data_mission['mission_title'], 'type':'Title'})
        for item in data_mission['mission_photo']:
            list_image.append({'link':item, 'type':'Collection'})
        
        return render(request, self.template,{'title':'Update Image','data':list_image,'id':id_mission})

class DeleteMission(View):
    def get(self, request, id_mission):
        ref_mission = db.collection('Missions')
        doc_mission= ref_mission.stream()
        for mission in doc_mission:
            if mission.id == id_mission:
                mission.reference.delete()
        return redirect('mission:list')
  
class PostAddMission(View):
    def post(self, request):
        mission_name = request.POST['mission_name']
        mission_start = request.POST['mission_start']
        mission_end = request.POST['mission_end']
        mission_target = request.POST['mission_target']
        mission_title = request.POST['mission_title']
        mission_type = request.POST.get('mission_type')
        mission_detail = request.POST['mission_detail']
        mission_photo = request.POST['mission_photo']
        mission_photo = mission_photo.split(",")
        while("" in mission_photo) : 
            mission_photo.remove("") 
        data = {
        'mission_name':mission_name,
        'mission_start': mission_start,
        'mission_end': mission_end,
        'mission_target':mission_target,
        'mission_title':mission_title,
        'mission_type':mission_type,
        'mission_detail': mission_detail,
        'mission_photo':mission_photo,
        'mission_collected':[0]
        
    }
        db.collection('Missions').document().set(data)
        return redirect('mission:list')
    
class PostUpdateFormMission(View):
    
    def post(self, request, id_mission):
        mission_name = request.POST['mission_name']
        mission_start = request.POST['mission_start']
        mission_end = request.POST['mission_end']
        mission_target = request.POST['mission_target']
        mission_type = request.POST.get('mission_type')
        mission_detail = request.POST['mission_detail']
        # for item in mission_photo:
        #     if len(item) < 10 :
        #         mission_photo.remove(item)
        data = {
        'mission_name':mission_name,
        'mission_start': mission_start,
        'mission_end': mission_end,
        'mission_target':mission_target,
        'mission_type':mission_type,
        'mission_detail': mission_detail,
        
    }
        ref = db.collection('Missions').document(id_mission)
        ref.update(data)
        return redirect('mission:list')

class DeleteImageCollection(View):
    
    def post(self, request):
        id_mission = request.POST.get('id')
        link_photo = request.POST.get('path')
        ref = db.collection('Missions').document(id_mission)
        ref.update({"mission_photo": ArrayRemove([link_photo])})
        return HttpResponse('OK')
        #return redirect('mission:update-image', id_mission = id_mission)

class UpdateImageTitle(View):
    def post(self, request):
        id_mission = request.POST['id']
        link_photo = request.POST['path']
        ref = db.collection('Missions').document(id_mission)
        ref.update({'mission_title':link_photo})
        return HttpResponse('OK')

class UpdateImageCollection(View):
    def post(self, request):
        id_mission = request.POST['id']
        link_photo = request.POST['path']
        link_photo = link_photo.split(',')
        ref = db.collection('Missions').document(id_mission)
        ref.update({"mission_photo": ArrayUnion(link_photo)})
        return HttpResponse('OK')