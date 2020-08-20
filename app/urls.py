from django.urls import path, include
from app.views.carousel import *
from app.views.contact import *
from app.views.donation import *
from app.views.mission import *
from app.views.platform import *
from app.views.json import *
from app.views.visimisi import *

urlpatterns = [
    path('', ViewHomePage.as_view(), name='home'),
    path('get-json', GetJsonSecurity.as_view(), name='get-json'),
    path('get-json-user', GetJsonUser.as_view(), name='get-json-user'),
    path('get-json-mission', GetJsonMission.as_view(), name='get-json-mission'),
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
       
        path('update-image/<str:id_mission>', ViewUpdateImageMission.as_view(), name='update-image'),
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
         path('post-del', DeleteProfilImage.as_view(), name='post-del'),
         path('add-col', AddCollection.as_view(), name='add-col')
     ],'visimisi')))
  
    
]