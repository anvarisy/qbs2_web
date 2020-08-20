from django.views import  View
import json
from django.http import JsonResponse
from app.__firebase__ import db


class GetJsonSecurity(View):
    def get(self, request):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return JsonResponse(data)

class GetJsonUser(View):
    def get(self, request):
        ref_user = db.collection('User')
        data_user = ref_user.stream();
        list_user=[]
        for user in data_user:
            dict_member = user.to_dict()
            dict_member['id'] = user.id
            list_user.append(dict_member)
        return JsonResponse(list_user, safe=False)

class GetJsonMission(View):
    def get(self, request):
        ref_mission = db.collection('Missions')
        data_mission =  ref_mission.stream();
        list_mission=[]
        for mission in data_mission:
            dict_member = mission.to_dict()
            dict_member['id'] = mission.id
            list_mission.append(dict_member)
        return JsonResponse(list_mission, safe=False)