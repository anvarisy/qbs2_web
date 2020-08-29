from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin


class ViewAddDonation(LoginRequiredMixin, View):
    template = 'pages/donation_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Donation'})
    
class ViewListDonation(LoginRequiredMixin, View):
    template = 'pages/donation_list.html'
    def get(self, request):
        data_ref = db.collection('Donation')
        data_donation = data_ref.stream()
        list_donation = []
        for donation in data_donation:
            dict_member = donation.to_dict()
            dict_member['id'] = donation.id
            list_donation.append(dict_member)
        return render(request, self.template, {'title': 'List Donation', 'data':list_donation})
    
class ViewUpdateDonation(LoginRequiredMixin, View):
    template = 'pages/donation_form.html'
    def get(self, request, id_donation):
        ref_donation = db.collection('Donation').document(id_donation)
        collection = ref_donation.get()
        return render(request, self.template, {'title':'Update Donation','data':collection.to_dict(), 'id':id_donation,})

class DeleteDonation(LoginRequiredMixin, View):
    def get(self, request, id_donation):
        donation_ref = db.collection('Donation')
        donation_doc = donation_ref.stream()
        for donation in donation_doc:
            if donation.id == id_donation:
                donation.reference.delete()
        return redirect('donation:list')
    
def getData(request):
    date = request.POST['date']
    donatur = request.POST['donatur']
    mission = request.POST['mission']
    value = request.POST['value']
    ref_user = db.collection('User').document(donatur)
    donatur_name = ref_user.get().to_dict()['full_name']
    ref_mission = db.collection('Missions').document(mission)
    mission_name = ref_mission.get().to_dict()['mission_name']
    data = {
        'date':date,
        'donatur': donatur,
        'mission_id':mission,
        'mission_name':mission_name,
        'donatur_name':donatur_name,
        'value':value
        
    }
    return data   

class PostAddDonation(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Donation').document().set(getData(request))
        return redirect('donation:list')

class PostUpdateDonation(LoginRequiredMixin, View):
    def post(self, request, id_donation):
        ref = db.collection('Donation').document(id_donation)
        ref.update(getData(request))
        return redirect('donation:list')

