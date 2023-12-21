// Copyright (c) 2023, j and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Card', {
	// refresh: function(frm) {
	before_submit(frm) {
		frm.set_value("delivery_date", frappe.format(new Date(), { fieldtype: "Date" }))
		// }
	}
	});