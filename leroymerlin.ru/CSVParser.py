import csv
import json
from typing import Dict, Any

# Shared template JSON
transport_request_json = {
    "deliveryAppointmentIdentifier": "",
    "transportRequestFlowTypeIdentifier": 2,
    "transportRequestEarlyPickupDate": "2024-09-14T07:00:00.000Z",
    "shippingLocationIdentifier": "",
    "deliveryLocationIdentifier": "",
    "transportRequestFlowSubtype": None,
    "requestOrderBindings": []
}


def create_json_object(row, identifier):
    json_object = transport_request_json.copy()

    json_object["deliveryAppointmentIdentifier"] = identifier
    json_object["shippingLocationIdentifier"] = row["shippingLocationIdentifier"]
    json_object["deliveryLocationIdentifier"] = row["deliveryLocationIdentifier"]
    json_object["transportRequestFlowSubtype"] = row["transportRequestFlowSubtype"] if row["transportRequestFlowSubtype"] != 'NULL' else None

    return json_object


def csv_to_json(input_path, output_path):
    json_by_id: Dict[str, Any] = {}

    with open(input_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')

        for row in csv_reader:
            identifier = row["deliveryAppointmentIdentifier"]

            if identifier in json_by_id:
                json_object = json_by_id[identifier]
            else:
                json_object = create_json_object(row, identifier)
                json_by_id[identifier] = json_object

            # Create requestOrderBinding for each row
            order_binding = {
                "orderIdentifier": row["orderIdentifier"],
                "orderUnloadingType": row["orderUnloadingType"],
                "orderPhytoCert": row["orderPhytoCert"].lower() == 'true',
                "orderRollsPresence": row["orderRollsPresence"].lower() == 'true',
                "orderTemperatureMode": row["orderTemperatureMode"] if row["orderTemperatureMode"] != 'NULL' else None,
                "slices": [
                    {
                        "sliceTotalReferenceUnit": float(row["sliceTotalReferenceUnit"]),
                        "sliceGrossWeight": float(row["sliceGrossWeigh"]),
                        "slicePallets": int(row["slicePallets"])
                    }
                ]
            }

            # Add every order_binding to requestOrderBindings
            json_object["requestOrderBindings"].append(order_binding)

    # Convert result to list
    result = list(json_by_id.values())

    # Write to JSON file
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(result, jsonfile, indent=4, ensure_ascii=False)
