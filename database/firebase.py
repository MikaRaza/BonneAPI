
import firebase_admin

from firebase_admin import credentials

from configs.firebase_config_example import firebaseConfig

import pyrebase

 

if not firebase_admin._apps:

    cred = credentials.Certificate("configs\myapi-af622-firebase-adminsdk-w2zkl-e450a79af9.json")
    firebase_admin.initialize_app(cred)

   

#cred = credentials.Certificate("path/to/serviceAccountKey.json")

#firebase_admin.initialize_app(cred)

 

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()