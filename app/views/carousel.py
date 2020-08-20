from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db

# Create your views here.
class ViewHomePage(View):
    template = 'pages/home.html'
    
    def get(self, request):
        return render(request, self.template, {'title':'Home',})

class ViewAddCarousel(View):
    template = 'pages/carousel_form.html'
    def get(self, request):
        return render(request, self.template, {'title':'Add Carousel'})
    
class ViewListCarousel(View):
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
    
class ViewUpdateCarousel(View):
    template = 'pages/carousel_form.html'
    def get(self, request, id_carousel):
        ref_carousel = db.collection('Carousel').document(id_carousel)
        collection = ref_carousel.get()
        return render(request, self.template, {'title':'Update Carousel','id':id_carousel,'data':collection.to_dict(), })

class DeleteCarousel(View):
    def get(self, request, id_carousel):
        ref_carousel = db.collection('Carousel')
        doc_carousel= ref_carousel.stream()
        for carousel in doc_carousel:
            if carousel.id == id_carousel:
                carousel.reference.delete()
        return redirect('carousel:list')

def getData(request):
    carousel_title = request.POST['carousel_title']
    carousel_link = request.POST['carousel_link']
    carousel_image = request.POST['carousel_image']
    data = {
        'carousel_title':carousel_title,
        'carousel_link':carousel_link,
        'carousel_image':carousel_image
    }
    return data

class PostAddCarousel(View):
    def post(self, request):
        db.collection('Carousel').document().set(getData(request))
        return redirect('carousel:list')

class PostUpdateCarousel(View):
    def post(self, request, id_carousel):
        ref = db.collection('Carousel').document(id_carousel)
        ref.update(getData(request))
        return redirect('carousel:list')
