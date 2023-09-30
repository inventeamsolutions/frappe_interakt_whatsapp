import frappe
import json
import requests
import time
from frappe.integrations.utils import make_post_request
from datetime import datetime
import frappe.utils

@frappe.whitelist()
def get_user_data():
    return frappe.db.sql(f"""Select * From `tabUser`;""", as_dict=True)
    
@frappe.whitelist()
def send_message(doc_type, doc_name):
    current_datetime = datetime.now()
    doc = frappe.get_doc(doc_type, doc_name)
    doc_data = doc.as_dict()
    settings = frappe.get_doc(
            "Whatsapp Settings", "Whatsapp Settings",
        )
    api_key = settings.api_key
    headers = {
        "authorization": f"Basic {api_key}",
        "content-type": "application/json"
    }

    key = doc.get_document_share_key()  # noqa
    frappe.db.commit()
    print_format = "Standard"
    doctype = frappe.get_doc("DocType", doc_data['doctype'])
    if doctype.custom:
        if doctype.default_print_format:
            print_format = doctype.default_print_format
    else:
        default_print_format = frappe.db.get_value(
            "Property Setter",
            filters={
                "doc_type": doc_data['doctype'],
                "property": "default_print_format"
            },
            fieldname="value"
        )
        print_format = default_print_format if default_print_format else print_format
        
    link = f'/api/method/frappe.utils.print_format.download_pdf?doctype={doc_data["doctype"]}&name={doc_data["name"]}&format={print_format}&no_letterhead=1&letterhead=No Letterhead&_lang=en'
    url = f'{frappe.utils.get_url()}{link}&key={key}'
    filename = f'{doc_data["name"]}.pdf'
    
    # Define the message data
    data = {
        "countryCode": "+91",
        "phoneNumber": doc_data["contact_mobile"],
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "invoice",
            "languageCode": "en",
            "headerValues": [
                url
            ],
            "fileName": filename,
            "bodyValues": [
                doc_data["contact_display"],
                doc_data["company"],
            ]
        }
    }
    
    response = make_post_request(
        f"{settings.api_url}",
        headers=headers,
        data=json.dumps(data)
    )
    # Create a WhatsApp Message document
    frappe.get_doc({
        "doctype": "Whatsapp Message",
        "label": "API Test",
        "type": "Outgoing",
        "message": str(data['template']),
        "to": data['phoneNumber'],
        "message_id": response['id'],
        "sent_time": current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    }).save(ignore_permissions=True)

    # Return a success message
    return response
        
    
@frappe.whitelist()
def get_reference_document_numbers(reference_doctype):
    # Query the database to fetch document numbers based on the selected Reference DocType
    document_numbers = frappe.get_all(reference_doctype, pluck='name')

    return document_numbers