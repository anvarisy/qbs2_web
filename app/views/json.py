from django.views import  View
import json
from django.http import JsonResponse
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin
from firebase_admin import auth

class GetJsonSecurity(LoginRequiredMixin, View):
    def get(self, request):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return JsonResponse(data)

class GetJsonUser(LoginRequiredMixin, View):
    def get(self, request):
        ref_user = db.collection('User')
        data_user = ref_user.stream();
        list_user=[]
        for user in data_user:
            dict_member = user.to_dict()
            dict_member['id'] = user.id
            list_user.append(dict_member)
        return JsonResponse(list_user, safe=False)

class GetJsonAuth(View):
    def get(self, request):
        list_ = []
        for user in auth.list_users().iterate_all():
            list_.append({'uid':user.uid,'email':user.email, 'status':user.disabled})
        return JsonResponse(list_, safe=False)

class GetJsonMission(LoginRequiredMixin, View):
    def get(self, request):
        ref_mission = db.collection('Missions')
        data_mission =  ref_mission.stream();
        list_mission=[]
        for mission in data_mission:
            dict_member = mission.to_dict()
            dict_member['id'] = mission.id
            list_mission.append(dict_member)
        return JsonResponse(list_mission, safe=False)