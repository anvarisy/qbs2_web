from django.urls import path, include
from app.views.carousel import *
from app.views.contact import *
from app.views.donation import *
from app.views.mission import *
from app.views.platform import *
from app.views.json import *
from app.views.visimisi import *
from app.views.user import *
from app.views.walkthrough import *
from app.views.payment import *
from app.views.proposal import *

urlpatterns = [
    path('', ViewHomePage.as_view(), name='home'),
    path('get-json', GetJsonSecurity.as_view(), name='get-json'),
    path('get-json-user', GetJsonUser.as_view(), name='get-json-user'),
    path('get-json-auth', GetJsonAuth.as_view(), name='get-json-auth'),
    path('get-json-mission', GetJsonMission.as_view(), name='get-json-mission'),
    path('login', ViewLogin.as_view(), name='login'),
    path('post-login', PostLogin.as_view(), name='post-login'),
    path('logout', PostLogout.as_view(), name='logout'),
    # path('payment/<str:uid>/<str:mission>/<int:total>',ViwePaymentPage.as_view(), name='payment'),
    path('charge',ViewPaymentPage.as_view(),name='charge'),
    # path('payment', include(([
    #      path('',ViewPaymentPage.as_view(), name='payment'),
    #       path('/charge',GetChargeView.as_view(), name='charge'),
    # ],'payment'))),
    
    path('carousel',include(([
        path('add', ViewAddCarousel.as_view(), name='add'),
        path('list', ViewListCarousel.as_view(), name='list'),
        path('update/<str:id_carousel>', ViewUpdateCarousel.as_view(), name='update'),
        path('delete/<str:id_carousel>', DeleteCarousel.as_view(), name='delete'),
        path('post-add', PostAddCarousel.as_view(), name='post-add'),
        path('post-update/<str:id_carousel>', PostUpdateCarousel.as_view(), name='post-update')
        
    ],'carousel'))),
    path('contact', include(([
        path('add', ViewAddContact.as_view(), name='add'),
        path('list', ViewListContact.as_view(), name='list'),
        path('update/<str:id_contact>', ViewUpdateContact.as_view(), name='update'),
        path('delete/<str:id_contact>', DeleteContact.as_view(), name='delete'),
        path('post-add', PostAddContact.as_view(), name='post-add'),
        path('post-update/<str:id_contact>', PostUpdateContact.as_view(), name='post-update')
    ],'contact'))),
    path('donation', include(([
        path('add', ViewAddDonation.as_view(), name='add'),
        path('list', ViewListDonation.as_view(), name='list'),
        path('update/<str:id_donation>', ViewUpdateDonation.as_view(), name='update'),
        path('delete/<str:id_donation>', DeleteDonation.as_view(), name='delete'),
        path('post-add', PostAddDonation.as_view(), name='post-add'),
        path('post-update/<str:id_donation>', PostUpdateDonation.as_view(), name='post-update')
    ],'donation'))),
    path('platform', include(([
        path('add', ViewAddPlatform.as_view(), name='add'),
        path('list', ViewListPlatform.as_view(), name='list'),
        path('update/<str:id_platform>', ViewUpdatePlatform.as_view(), name='update'),
        path('delete/<str:id_platform>', DeletePlatform.as_view(), name='delete'),
        path('post-add', PostAddPlatform.as_view(), name='post-add'),
        path('post-update/<str:id_platform>', PostUpdatePlatform.as_view(), name='post-update')
    ],'platform'))),
     path('mission', include(([
        path('add', ViewAddMission.as_view(), name='add'),
        path('list', ViewListMission.as_view(), name='list'),
        path('update/<str:id_mission>', ViewUpdateFormMission.as_view(), name='update'),
        path('detail/<str:id_mission>', ViewDetailMission.as_view(), name='detail'),
        path('update-image/<str:id_mission>', ViewUpdateImageMission.as_view(), name='update-image'),
        path('update-report/<str:id_mission>',ViewUpdateReport.as_view(), name='update-report'),
         path('post-update-report',PostUpdateReport.as_view(), name='post-update-report'),
        #  path('delete-collection/<str:id_mission>/?P<path>', DeleteImageCollection.as_view(), name='delete-collection'),
        path('update-image-title', UpdateImageTitle.as_view(), name='update-image-title'),
        path('update-image-col', UpdateImageCollection.as_view(), name='update-image-col'),
        path('delete-collection', DeleteImageCollection.as_view(), name='delete-collection'),
        path('delete/<str:id_mission>', DeleteMission.as_view(), name='delete'),
        path('post-add', PostAddMission.as_view(), name='post-add'),
        path('post-update/<str:id_mission>', PostUpdateFormMission.as_view(), name='post-update')
    ],'mission'))),
     path('visimisi', include(([
         path('view', ViewProfil.as_view(), name='view'),
         path('viewcol', ViewProfilImage.as_view(), name='viewcol'),
         path('add-misi', AddMisi.as_view(), name='add-misi'),
         path('del-misi', DeleteMisi.as_view(), name='del-misi'),
         path('update-visi', UpdateVisi.as_view(), name='update-visi'),
         path('update-detail', UpdateDetail.as_view(), name='update-detail'),
         path('post-del', DeleteProfilImage.as_view(), name='post-del'),
         path('add-col', AddCollection.as_view(), name='add-col')
     ],'visimisi'))),
     path('user', include(([
         path('',ViewUser.as_view(), name='list')
     ],'user'))),
     path('walk', include(([
         path('post-add', PostAddWalk.as_view(), name='post-add'),
         path('post-update/<str:id_walk>', PostUpdateWalk.as_view(), name='post-update'),
         path('add', ViewAddWalkthrough.as_view(), name='add'),
         path('list', ViewListWalk.as_view(), name='list'),
         path('update/<str:id_walk>', ViewUpdateWalkthrough.as_view(), name='update'),
         path('delete/<str:id_walk>', DeleteWalk.as_view(), name='delete')
         
     ],'walk'))),
     path('proposal', include(([
        path('list', ViewProposal.as_view(),name='list'),
        path('list-ii', ViewTransaction.as_view(),name='list-ii')    
     ],'proposal')))
  
    
]