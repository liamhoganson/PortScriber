import json
import re
from pydantic import BaseModel, field_validator
from typing import List, Dict

# TODO: Remove this to work with webhooks later
mock_data = """{
  "id": "daafb100-06ce-422a-b523-110ebc0fa08e:main",
  "trigger_id": "1d7283a7-f27b-41fa-8550-e989adc4745b",
  "date": "2024-08-26T21:02:04.820Z",
  "payload": {
    "id": "86a4pp7hh",
    "custom_id": "INFRA-4441",
    "custom_item_id": 0,
    "name": "power survey",
    "text_content": "",
    "description": "",
    "status": {
      "id": "p90090223948_Clc4PiJ5",
      "status": "to do",
      "color": "#87909e",
      "orderindex": 0,
      "type": "open"
    },
    "orderindex": "119431925.00000000000000000000000000000000",
    "date_created": "1724706122123",
    "date_updated": "1724706122573",
    "date_closed": null,
    "date_done": null,
    "archived": false,
    "creator": {
      "id": 63111425,
      "username": "Liam Hoganson",
      "color": "#388d3c",
      "email": "lhoganson@utahbroadband.com",
      "profilePicture": null
    },
    "assignees": [],
    "group_assignees": [],
    "watchers": [
      {
        "id": 63111425,
        "username": "Liam Hoganson",
        "color": "#388d3c",
        "initials": "LH",
        "email": "lhoganson@utahbroadband.com",
        "profilePicture": null
      }
    ],
    "checklists": [],
    "tags": [],
    "parent": null,
    "priority": null,
    "due_date": null,
    "start_date": null,
    "points": null,
    "time_estimate": null,
    "time_spent": 0,
    "custom_fields": [
      {
        "id": "1f9c6f8a-734f-400e-a3ab-9f32eed42ee6",
        "name": "Pdu asset",
        "type": "short_text",
        "type_config": {},
        "date_created": "1724211423278",
        "hide_from_guests": false,
        "value": "62643",
        "required": false
      },
      {
        "id": "0c2803dc-d7b1-4671-b2a6-a94a0d111e6e",
        "name": "Pdu labeled number",
        "type": "number",
        "type_config": {},
        "date_created": "1724212000549",
        "hide_from_guests": false,
        "required": false
      },
      {
        "id": "91d5b176-e1fa-4165-a4a1-e1dc98556ecf",
        "name": "Pdu type",
        "type": "drop_down",
        "type_config": {
          "options": [
            {
              "id": "3ddbdc4a-541d-4abf-a4f4-846a762537ac",
              "name": "Ict",
              "color": null,
              "orderindex": 0
            },
            {
              "id": "2a6b6c7c-1b9c-4f40-ad2d-2a72a3d4aafd",
              "name": "packet flux",
              "color": null,
              "orderindex": 1
            },
            {
              "id": "d36431a7-db23-4510-a767-75d646326355",
              "name": "Synaccess",
              "color": null,
              "orderindex": 2
            },
            {
              "id": "fd901bf1-d74c-4297-8a15-61aa2e424797",
              "name": "other",
              "color": null,
              "orderindex": 3
            }
          ]
        },
        "date_created": "1724213057846",
        "hide_from_guests": false,
        "value": 2,
        "required": false
      },
      {
        "id": "5b7001f7-65cb-4d87-bc18-ce64e42003d9",
        "name": "Router Ports",
        "type": "text",
        "type_config": {},
        "date_created": "1724468101126",
        "hide_from_guests": false,
        "value": "",
        "required": false
      },
      {
        "id": "4c6b67e0-84d4-4336-95e3-ff5f2498a90d",
        "name": "Site",
        "type": "short_text",
        "type_config": {},
        "date_created": "1724211862939",
        "hide_from_guests": false,
        "value": "butte",
        "required": false
      },
      {
        "id": "2e818a16-34c0-4a98-9456-2b16570ee95f",
        "name": "Switch1 Ports",
        "type": "text",
        "type_config": {},
        "date_created": "1724468149019",
        "hide_from_guests": false,
        "value": "5:11\\n7:12",
        "required": false
      },
      {
        "id": "e8782cd7-7d7f-4e2d-bf71-da59f22d8d50",
        "name": "Tasks",
        "type": "tasks",
        "type_config": {
          "fields": []
        },
        "date_created": "1686155163294",
        "hide_from_guests": false,
        "required": false
      },
      {
        "id": "ca792f21-62b4-4d02-a6c1-27e15ecab1fb",
        "name": "schedule date",
        "type": "date",
        "type_config": {},
        "date_created": "1715716519010",
        "hide_from_guests": false,
        "required": false
      },
      {
        "id": "2898dd7a-9e26-4a6f-8000-89bae5189ad5",
        "name": "sw-2 Ports",
        "type": "text",
        "type_config": {},
        "date_created": "1724468188543",
        "hide_from_guests": false,
        "value": "",
        "required": false
      },
      {
        "id": "0cf810a6-6aa8-4b29-afdb-ca8c800a3c43",
        "name": "test",
        "type": "text",
        "type_config": {},
        "date_created": "1724467973702",
        "hide_from_guests": false,
        "required": false
      },
      {
        "id": "a4a5b4cf-9473-4ca7-9fc5-7de98d6df6eb",
        "name": "Address",
        "type": "location",
        "type_config": {},
        "date_created": "1687376969908",
        "hide_from_guests": false,
        "required": false
      },
      {
        "id": "826e6377-8a9e-4949-8733-2852c6522058",
        "name": "Install Type",
        "type": "drop_down",
        "type_config": {
          "new_drop_down": true,
          "options": [
            {
              "id": "1dd01d83-e753-4915-9fed-b277987f6e00",
              "name": "In coverage (standard install)",
              "color": "#667684",
              "orderindex": 0
            },
            {
              "id": "a4df509b-3ba7-4de5-8f6e-7aedea5dbb3d",
              "name": "Point to point",
              "color": "#7C4DFF",
              "orderindex": 1
            },
            {
              "id": "66176413-dfae-48b8-b07d-2f6aab9a6cc3",
              "name": "Upgrade",
              "color": "#e50000",
              "orderindex": 2
            },
            {
              "id": "6364982b-0875-4115-ba38-5a1f7daee82c",
              "name": "Custom ",
              "color": "#EA80FC",
              "orderindex": 3
            },
            {
              "id": "48332029-5433-43cf-b0f9-2a42526c75dc",
              "name": "Ap addition/new install",
              "color": "#ff7800",
              "orderindex": 4
            },
            {
              "id": "7f8f54ca-1a84-4215-bba4-d6675e52e8bd",
              "name": "Ap addition/upgrade",
              "color": "#AF7E2E",
              "orderindex": 5
            },
            {
              "id": "28000c32-9a8e-487f-a179-5e8e4ecb0b76",
              "name": "Licensed point to point",
              "color": "#f9d900",
              "orderindex": 6
            },
            {
              "id": "8fb462ae-eec5-462b-8168-555f19f58210",
              "name": "Not servicable",
              "color": "#800000",
              "orderindex": 7
            }
          ]
        },
        "date_created": "1703187509355",
        "hide_from_guests": true,
        "required": false
      }
    ],
    "dependencies": [],
    "linked_tasks": [],
    "locations": [],
    "team_id": "9006060954",
    "url": "https://app.clickup.com/t/86a4pp7hh",
    "sharing": {
      "public": false,
      "public_share_expires_on": null,
      "public_fields": [
        "assignees",
        "priority",
        "due_date",
        "content",
        "comments",
        "attachments",
        "customFields",
        "subtasks",
        "tags",
        "checklists",
        "coverimage"
      ],
      "token": null,
      "seo_optimized": false
    },
    "list": {
      "id": "901305181084",
      "name": "Needs documentation",
      "access": true
    },
    "project": {
      "id": "90131253041",
      "name": "Wireless enginnering",
      "hidden": false,
      "access": true
    },
    "folder": {
      "id": "90131253041",
      "name": "Wireless enginnering",
      "hidden": false,
      "access": true
    },
    "space": {
      "id": "90090223948"
    }
  }
}"""


class PDUPayloadModel(BaseModel):
    pdu_asset_number: str
    pdu_type: str
    pdu_site: str
    ports_data: Dict[str, List[str]]

    @field_validator('ports_data', mode="before")
    def remove_empty_lists(cls, v: dict):
      return {k: v for k, v in v.items() if v != ['']}

    @field_validator('ports_data', mode="after")
    def validate_ports_data(cls, v: dict):
        pattern = re.compile(r'^\d+:\d+$')
        validated_dict = {}
        for key, value_list in v.items():
            for item in value_list:
                if not pattern.match(item):
                    raise ValueError(f"Invalid format in '{key}': '{item}' is not in 'number:number' format.")
            validated_dict[key] = value_list
        return validated_dict

class PDUData:
    def __init__(self):
        self.payload_data = mock_data

    def get_pdu_data(self) -> dict: ##TODO: Break this function down into smaller functions
        json_data = json.loads(self.payload_data)
        pdu_type_index = json_data.get('payload').get('custom_fields')[2].get('value')
        match pdu_type_index:
            case 0:
                pdu_type = 'ICT'
            case 1:
                pdu_type = 'Packetflux'
            case 2:
                pdu_type = 'Synaccess'
            case _:
                raise ValueError("No PDU type defined!")

        port_list_dictionary = {}
        json_data = json.loads(mock_data)
        for entry in json_data.get('payload').get('custom_fields'):
            if (entry.get("name")) in ["Router Ports", "Switch1 Ports", "sw-2 Ports"]:
                port_list_dictionary.update({entry.get("name"): (entry.get("value").split("\n"))})

        # Create the payload model
        pdu_data = {
            "pdu_asset_number": json_data.get('payload').get('custom_fields')[0].get('value'),
            "pdu_type": pdu_type,
            "pdu_site": json_data.get('payload').get('custom_fields')[3].get('value'),
            "ports_data": port_list_dictionary
        }

        pdu_data_model = PDUPayloadModel(**pdu_data)
        return json.loads(pdu_data_model.json())
