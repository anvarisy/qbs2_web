import midtransclient
from time import gmtime, strftime
from django.shortcuts import render, redirect
from django.views import View
from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json



@method_decorator(csrf_exempt, name='dispatch')
class ViewPaymentPage(View):
    def post(self, request):
        # time = strftime("%Y%m%d%H%M%S", gmtime())
        # is_production=False,
        # server_key='SB-Mid-server-PV66D9pq57gAf01tpRcdM2e7',
        # client_key='SB-Mid-client-CvCBexmp05svFhIE'
        # core = midtransclient.CoreApi(
        # is_production=True,
        # server_key='Mid-server-QeAV3hB7JRhAaU4GOTY_nxCN',
        # client_key='Mid-client-WrMb-HVBxMZrefnq'
        # )
        snap = midtransclient.Snap(
        is_production=True,
        server_key='Mid-server-QeAV3hB7JRhAaU4GOTY_nxCN',
        client_key='Mid-client-WrMb-HVBxMZrefnq'
        )
        # param = {"customer_details":{},"custom_field1":"ANYCUSTOMFIELD","item_details":[{"id":"5c18ea1256f67560cb6a00cdde3c3c7a81026c29","name":"USB FlashDisk","price":7500.0,"quantity":1}],"transaction_details":{"currency":"IDR","gross_amount":7500.0,"order_id":"1598503263668"},"user_id":"e77c77b7-cb75-47d0-984b-0429a15997d2"}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        # transaction = core.charge(param)
        transaction = snap.create_transaction(body)
        return JsonResponse(transaction, safe=False)
# @method_decorator(csrf_exempt, name='dispatch')
# class ViewPaymentPage(View):
#     # template = 'payment.html'
#     # snap = midtransclient.Snap(
#     #     is_production=True,
#     #     server_key='Mid-server-QeAV3hB7JRhAaU4GOTY_nxCN',
#     #     client_key='Mid-client-WrMb-HVBxMZrefnq'
#     # )
#     # time = strftime("%Y%m%d%H%M%S", gmtime())
    
#     def get(self, request):
#         # body_unicode = request.body.decode('utf-8')
#         # body = json.loads(body_unicode)
#         # print(body)
#         # param = {
#         #     "transaction_details": {
#         #         "order_id": self.time,
#         #         "gross_amount": 7500
#         #     }, "credit_card": {
#         #         "secure": True
#         #     },
#         # }
#         # transaction = self.snap.create_transaction(param)

#         # transaction_token = transaction['token']
#         return HttpResponse('')


# @method_decorator(csrf_exempt, name='dispatch') 
# class GetChargeView(View):
#     core = midtransclient.CoreApi(
#         is_production=True,
#         server_key='Mid-server-QeAV3hB7JRhAaU4GOTY_nxCN',
#         client_key='Mid-client-WrMb-HVBxMZrefnq')
#     time = strftime("%Y%m%d%H%M%S", gmtime())
#     def post(self, request):
#          param = {
#             "transaction_details": {
#                 "order_id": self.time,
#                 "gross_amount": 7500
#             }, "credit_card": {
#                 "secure": True
#             },
#         }
#         charge_response = self.core.charge(param)
#         return JsonResponse(charge_response, False)