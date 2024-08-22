
import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate("app/auth/secret.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_todo_collection():
    return db.collection('todos')
