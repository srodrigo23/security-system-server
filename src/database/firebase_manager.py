import firebase_admin
from firebase_admin import db, credentials, messaging


class FirebaseManager():
    
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('./database/private-key.json')
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://surveillance-database-default-rtdb.firebaseio.com/'
        })

    def send_push(self, title, msg, registration_token, data_object=None):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=msg
            ),
            data=data_object,
            tokens=registration_token
        )
        # Send a messageto the device corresponding to the provided registration token
        response = messaging.send_multicast(message)
        # response is a message ID String
        print("Succesfully sent message", response)

    def record_event(self, date, type, description):
        ref = db.reference('Registros')
        ref.push({
            "fecha":date,
            "tipo":type,
            "desc":description
        })