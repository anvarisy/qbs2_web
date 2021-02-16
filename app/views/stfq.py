from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class StfqDetail(View):
    template = 'pages/stfq_detail.html'
    def get(self, request):
        datas = db.collection('stfq').document('page').get()
        val = datas.to_dict()
        return render(request, self.template,{'detail':val['detail']})
    
    def post(self, request):
        detail = request.POST['detail']
        ref = db.collection('stfq').document('page')
        ref.update({
            'detail':detail
        })
        return redirect('stfq:detail')

class StfqContent(View):
    template = 'pages/stfq_content.html'
    def get(self, request):
        try:
            data = db.collection('stfq').document('page').get()
            data_video = db.collection('stfq').document('page').collection('video').stream()
            videos = []
            images = data.to_dict()['image']
            for item in data_video:
                member = item.to_dict()
                member['id'] = item.id
                videos.append(member)
            return render(request, self.template,{'images':images,'videos':videos})
        except :
            print('empty')
            return render(request, self.template,{})
    
    def post(self, request):
        if request.POST['type']=='P':
            photos = request.POST['path']
            photos = photos.split(',')
            ref = db.collection('stfq').document('page')
            ref.update({"image": ArrayUnion(photos)})
        elif request.POST['type']=='V':
            video = request.POST['path']
            title = request.POST['title']
            data = {
                'link':video,
                'title':title,
                'status':True
            }
            ref = db.collection('stfq').document('page').collection('video').document()
            ref.set(data)
        return HttpResponse('OK')

class StfqDelete(View):
    def post(self, request):
        if request.POST['type']=='P':
            link_photo = request.POST.get('path')
            ref = db.collection('stfq').document('page')
            ref.update({"image": ArrayRemove([link_photo])})
        elif request.POST['type']=='V':
            video_id = request.POST['id']
            ref = db.collection('stfq').document('page').collection('video').stream()
            for item in ref:
                if item.id == video_id:
                    item.reference.delete()
        return HttpResponse('OK')

class StfqCarousel(View):
    template = 'pages/stfq_carousel.html'
    def get(self, request):
        data_carousel = db.collection('stfq').document('page').collection('carousel').stream()
        carousels = []
        for item in data_carousel:
            carousel = item.to_dict()
            carousel['id'] = item.id
            carousels.append(carousel)
        return render(request, self.template,{'c':carousels})
    def post (self, request):
        type_p = ''
        try:
            type_p = request.POST['type']
        except :
            type_p = 'insert'
        if type_p == 'insert':
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
            db.collection('stfq').document('page').collection('carousel').document().set(data)
            return redirect('stfq:carousel')
        else:
            c_id = request.POST['id']
            ref = db.collection('stfq').document('page').collection('carousel').stream()
            for item in ref:
                if item.id == c_id:
                    item.reference.delete()
            return HttpResponse('OK')
