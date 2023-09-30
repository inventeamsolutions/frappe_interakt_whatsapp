// Copyright (c) 2023, Inventeam Solutions Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whatsapp Message', {
	refresh: function(frm) {
        // Add a trigger to watch for changes in the first dropdown
        frm.fields_dict['reference_document_no'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    // Define filters based on the selected Doctype
                    ['name', '=', frm.reference_doctype] // Example: 'Sales Invoice'
                ]
            };
        };
    }
});