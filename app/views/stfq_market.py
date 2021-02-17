from django.shortcuts import render, redirect
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import http.client
import json
from app.models import City
# conn = http.client.HTTPSConnection("api.rajaongkir.com")

# headers = { 'key': "783e41549002c1dde506303407d1fc6b" }

# conn.request("GET", "/starter/city", headers=headers)

# res = conn.getresponse()
# data = res.read()
# # a = data.decode("utf-8")
# json_data = json.loads(data)
# result = json_data['rajaongkir']
# for item in result['results']:
#     City.objects.create(**item)
# print("Type:", type(json_data))
# for item in json_data:
#     print(item['result'])
# print(data.decode("utf-8"))

class ViewMarket(View):
    template = 'pages/stfq_market.html'
    def get(self, request):
        ref = db.collection('stfq-market').document('Tenants').collection('items').stream()
        tenants = []
        categories = []
        stuffes = []
        cities = City.objects.filter(province__contains='Jawa')
        for item in ref:
            tenant = item.to_dict()
            tenant['id'] = item.id
            tenants.append(tenant)
        
        ref_categories = db.collection('stfq-market').document('Categories').collection('items').stream()
        for item in ref_categories:
            category = item.to_dict()
            category['id'] = item.id
            categories.append(category)

        ref_stuffes = db.collection('stfq-market').document('Products').collection('items').stream()
        for item in ref_stuffes:
            stuff = item.to_dict()
            stuff['id'] = item.id
            stuffes.append(stuff)
        return render(request, self.template,{'title':'Market','tenants':tenants,'cities':cities, 'categories':categories,'stuffes':stuffes})

    def post(self, request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        status = ''
        try:
            status = request.POST['type']
        except:
            status = 'insert'
        if status == 'insert':
            tenant= request.POST.dict()
            ref = db.collection('stfq-market').document('Tenants').collection('items').document().set(tenant)
            return redirect('stfq:market')
        elif status =='delete':
            t_id = request.POST['id']
            ref = db.collection('stfq-market').document('Tenants').collection('items').stream()
            for item in ref:
                if item.id == t_id:
                    item.reference.delete()
            return HttpResponse('OK')
       
class PostCategory(View):
    def post(self, request):
        status = ''
        try:
            status = request.POST['type']
        except:
            status = 'insert'
        if status == 'insert':
            category= request.POST.dict()
            ref = db.collection('stfq-market').document('Categories').collection('items').document().set(category)
            return redirect('stfq:market')
        elif status == 'delete':
            c_id = request.POST['id']
            ref = db.collection('stfq-market').document('Categories').collection('items').stream()
            for item in ref:
                if item.id == c_id:
                    item.reference.delete()
            return HttpResponse('OK')

class PostStuff(View):
    def post(self, request):
        status = ''
        try:
            status = request.POST['type']
        except:
            status = 'insert'
        if status == 'insert':
            arrs = []
            temp = ''
            product_name = request.POST['product_name']
            for i in product_name:
                temp+=i
                arrs.append(temp)
            
            product_price = request.POST['product_price']
            product_weight = request.POST['product_weight']
            product_date = request.POST['product_date']
            product_image = request.POST['product_image']
            
            categories = request.POST['categories']
            a_categories = categories.split(',')
            f_categories = []
            for item in a_categories:
                ref = db.collection('stfq-market').document('Categories').collection('items').document(item).get()
                print(ref.to_dict())
                data = {
                    'category_id':ref.id,
                    'category_name':ref.to_dict()['category_name']
                }
                f_categories.append(data)
            tenant_id = request.POST['tenant_id']
            image_collections = request.POST['image_collections']
            image_collections = image_collections.split(',')
            data = {
                 'product_name':product_name,
                    'product_price':product_price,
                    'product_weight':product_weight,
                    'product_date':product_date,
                    'product_image':product_image,
                    'categories':f_categories,
                    'tenant_id':tenant_id,
                    'product_query': arrs,
                    'image_collections':image_collections
            }
            print(data)
            ref = db.collection('stfq-market').document('Products').collection('items').document().set(data)
            return HttpResponse('OK')
        elif status == 'delete':
            c_id = request.POST['id']
            ref = db.collection('stfq-market').document('Products').collection('items').stream()
            for item in ref:
                if item.id == c_id:
                    item.reference.delete()
            return HttpResponse('OK')