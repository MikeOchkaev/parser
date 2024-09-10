import csv
import json
import copy
import io
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

input_path = os.getenv('INPUT_PATH')
output_path = os.getenv('OUTPUT_PATH')
api_url = os.getenv('API_URL')
ldap = os.getenv('LDAP')
email = os.getenv('EMAIL')
bu_id = os.getenv('BU_ID')
loc_id = os.getenv('LOC_ID')
role = os.getenv('ROLE')

# Templates
transport_request_json: dict = {
    "deliveryAppointmentIdentifier": "",
    "transportRequestFlowTypeIdentifier": 2,                        # always 2
    "transportRequestEarlyPickupDate": "2024-09-14T07:00:00.000Z",  # always 2024-09-14T07:00:00.000Z
    "shippingLocationIdentifier": "",
    "deliveryLocationIdentifier": "",
    "transportRequestFlowSubtype": None,    # always null
    "requestOrderBindings": []
}
order_binding_json: dict = {
    "orderIdentifier": "11111456",
    "orderUnloadingType": "back",
    "orderPhytoCert": False,                # always false
    "orderRollsPresence": False,            # always false
    "orderTemperatureMode": None,           # always null
    "slices": [
        {
            "sliceTotalReferenceUnit": 0.0,
            "sliceGrossWeight": 0.0,
            "slicePallets": 0
        }
    ]
}


def create_request(row, identifier):
    json_object = copy.deepcopy(transport_request_json)

    json_object["deliveryAppointmentIdentifier"] = identifier
    json_object["shippingLocationIdentifier"] = row["shippingLocationIdentifier"]
    json_object["deliveryLocationIdentifier"] = row["deliveryLocationIdentifier"]
    json_object["transportRequestFlowSubtype"] = row["transportRequestFlowSubtype"] if row["transportRequestFlowSubtype"] != 'NULL' else None

    return json_object


def create_order_binding(row):
    json_object = copy.deepcopy(order_binding_json)

    json_object["orderIdentifier"] = row["orderIdentifier"]
    json_object["orderUnloadingType"] = row["orderUnloadingType"]
    json_object["orderPhytoCert"] = row["orderPhytoCert"]
    json_object["orderRollsPresence"] = row["orderRollsPresence"]
    json_object["slices"][0]["sliceTotalReferenceUnit"] = float(row["sliceTotalReferenceUnit"])
    json_object["slices"][0]["sliceGrossWeight"] = float(row["sliceGrossWeigh"])
    json_object["slices"][0]["slicePallets"] = int(row["slicePallets"])

    return json_object


def add_order_to_request(json_object, row):
    order_binding = create_order_binding(row)
    json_object["requestOrderBindings"].append(order_binding)


def create_curl_command(request_body: str) -> str:
    curl_command = io.StringIO()

    curl_command.write("curl -v -X 'POST' \\\n")
    curl_command.write(f"  '{api_url}' \\\n")
    curl_command.write(f"  -H 'x-lmru-ldap: {ldap}' \\\n")
    curl_command.write(f"  -H 'x-lmru-email: {email}' \\\n")
    curl_command.write(f"  -H 'x-lmru-bu-id: {bu_id}' \\\n")
    curl_command.write(f"  -H 'x-lmru-location-id: {loc_id}' \\\n")
    curl_command.write(f"  -H 'x-lmru-role: {role}' \\\n")
    curl_command.write("  -H 'Content-Type: application/json' \\\n")
    curl_command.write(f"  -d '{request_body}'\n")

    return curl_command.getvalue()


def csv_to_curl():
    request_by_id: Dict[str, Any] = {}

    with open(input_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')

        for row in csv_reader:
            identifier = row["deliveryAppointmentIdentifier"]

            if identifier in request_by_id:
                json_object = request_by_id[identifier]
            else:
                json_object = create_request(row, identifier)
                request_by_id[identifier] = json_object

            add_order_to_request(json_object, row)

    with open(output_path, 'w', encoding='utf-8') as outputfile:
        for request in request_by_id.values():
            json_request = json.dumps([request], ensure_ascii=False, indent=4)

            curl = create_curl_command(json_request)

            outputfile.write(curl + '\n\n')
