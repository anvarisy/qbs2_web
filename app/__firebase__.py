import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os
from qbs2_web.settings import BASE_DIR
# Use a service account

loc = os.path.join(BASE_DIR, 'config.json')
cred = credentials.Certificate(loc)
firebase_admin.initialize_app(cred,{
     'storageBucket': 'pondok-f2805.appspot.com'
})

db = firestore.client()
bkt = storage.bucket()