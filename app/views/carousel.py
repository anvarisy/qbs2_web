from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ViewHomePage(LoginRequiredMixin, View):
    template = 'pages/home.html'
    # login_url = '/login'
    def get(self, request):
        return render(request, self.template, {'title':'Home',})

class ViewAddCarousel(LoginRequiredMixin, View):
    template = 'pages/carousel_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Carousel'})
    
class ViewListCarousel(LoginRequiredMixin, View):
    template = 'pages/carousel_list.html'
    def get(self, request):
     
        data_ref = db.collection('Carousel')
        data_carousel = data_ref.stream()
        list_carousel = []
        for carousel in data_carousel:
            dict_member = carousel.to_dict()
            dict_member['id'] = carousel.id
            list_carousel.append(dict_member)
        return render(request, self.template, {'title': 'List Carousel', 'data':list_carousel})
    
class ViewUpdateCarousel(LoginRequiredMixin, View):
    template = 'pages/carousel_form.html'
    def get(self, request, id_carousel):
        ref_carousel = db.collection('Carousel').document(id_carousel)
        collection = ref_carousel.get()
        return render(request, self.template, {'title':'Update Carousel','id':id_carousel,'data':collection.to_dict(), })

class DeleteCarousel(LoginRequiredMixin, View):
    def get(self, request, id_carousel):
        ref_carousel = db.collection('Carousel')
        doc_carousel= ref_carousel.stream()
        for carousel in doc_carousel:
            if carousel.id == id_carousel:
                carousel.reference.delete()
        return redirect('carousel:list')

def getData(request):
    title = request.POST['title']
    subtitle = request.POST['subtitle']
    link = request.POST['link']
    position = request.POST['position']
    image = request.POST['carousel_image']
    data = {
        'title':title,
        'subtitle':subtitle,
        'link':link,
        'position':position,
        'image':image
    }
    return data

class PostAddCarousel(LoginRequiredMixin, View):
    def post(self, request):
        db.collection('Carousel').document().set(getData(request))
        return redirect('carousel:list')

class PostUpdateCarousel(LoginRequiredMixin, View):
    def post(self, request, id_carousel):
        ref = db.collection('Carousel').document(id_carousel)
        ref.update(getData(request))
        return redirect('carousel:list')
