# Copyright (c) 2023, Inventeam Solutions Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
import json
import frappe
from frappe.model.document import Document
from frappe.utils.safe_exec import get_safe_globals, safe_exec
from frappe.integrations.utils import make_post_request
from frappe.desk.form.utils import get_pdf_link

class WhatsappMessage(Document):
    def format_number(self, number):
        """Format number."""
        if (number.startswith("+")):
            number = number[1:len(number)]

        return number
