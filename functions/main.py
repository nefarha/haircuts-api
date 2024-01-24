# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import datetime
import json
import urllib.parse as parser

import requests
from firebase_admin import firestore, initialize_app
from firebase_functions import https_fn, options

initialize_app()
options.set_global_options(max_instances=1)


@https_fn.on_request()
def accept_payment(req: https_fn.Request) -> https_fn.Response:
    token = "$2y$13$4DYobXThUcBgG9E8hNZjq.5zZRhiRx0KkQJKONi1.dDL3vIrOipRG"
    db = firestore.client()
    current_time = datetime.datetime.now()
    milliseconds_since_epoch = int(current_time.timestamp() * 1000)

    if req.method == "POST":
        try:
            formDataBytes = req.get_data()
            getDataFromBytes = formDataBytes.decode('utf-8')

            parsedFormData = parser.parse_qs(getDataFromBytes)

            jsonFromParsedData = json.dumps({key: value[0] for key, value in parsedFormData.items()})

            jsonDecodeFromDumps = json.loads(jsonFromParsedData)

            if jsonDecodeFromDumps['token'] == token:
                payloadDataFromJson = json.loads(jsonDecodeFromDumps['data'])

                
                doc_id = str(payloadDataFromJson['bill_link_id'])
                doc_new_status = payloadDataFromJson['status']

                # Get Payment Model
                doc_ref = db.collection("payment").document(doc_id)
                doc_item = doc_ref.get().to_dict()
                # Update It
                doc_ref.update({"status": doc_new_status})

                # Get Model from Cart
                orderItem = doc_item['bookingModel']
                print(orderItem['id'])

                if  payloadDataFromJson['status'] == "SUCCESSFUL":
                    if orderItem is not None:
                            doc_ref = db.collection("booking").document(str(orderItem['id']))
                            doc_ref.set(orderItem)

                return https_fn.Response("CALLBACK SUKSES")
                
            else:
                return https_fn.Response("INVALID TOKEN")
        except Exception as error:
            return https_fn.Response(f"terjadi error di {error}")
    else:
        return https_fn.Response("ini halaman get")

@https_fn.on_request()
def disbursment(req: https_fn.Request) -> https_fn.Response:
    token = "$2y$13$4DYobXThUcBgG9E8hNZjq.5zZRhiRx0KkQJKONi1.dDL3vIrOipRG"
    db = firestore.client()
    current_time = datetime.datetime.now()

    if req.method == "POST":
        try:
            formDataBytes = req.get_data()
            getDataFromBytes = formDataBytes.decode('utf-8')

            parsedFormData = parser.parse_qs(getDataFromBytes)

            jsonFromParsedData = json.dumps({key: value[0] for key, value in parsedFormData.items()})

            jsonDecodeFromDumps = json.loads(jsonFromParsedData)

            if jsonDecodeFromDumps['token'] == token:
                payloadDataFromJson = json.loads(jsonDecodeFromDumps['data'])

                
                doc_id = str(payloadDataFromJson['id'])
                doc_new_status = payloadDataFromJson['status']

                # Get Payment Model
                doc_ref = db.collection("withdraw").document(doc_id)
                doc_item = doc_ref.get().to_dict()
                # Update It
                doc_ref.update({"status": doc_new_status})

                # Get Book from Cart
                orderItem = doc_item['orderModel']
                print(orderItem['id'])

                if  payloadDataFromJson['status'] == "SUCCESSFUL":
                    
                    doc_ref = db.collection("orderStore").document(str(orderItem['id']))
                    doc_ref.set(orderItem)
                return https_fn.Response("CALLBACK SUKSES")
                
            else:
                return https_fn.Response("INVALID TOKEN")
        except Exception as error:
            return https_fn.Response(f"{error}")
    else:
        return https_fn.Response("ini halaman get")
