// Copyright (c) 2023, j and contributors
// For license information, please see license.txt

frappe.ui.form.on('learning page', {
	refresh: function(frm) {
			frm.add_custom_button("button",() =>
				console.log("clicked on the VS"),
				"action"
			)
			frm.add_custom_button("button2",() =>
				console.log("clicked on the VS"),
				"action"
			)
	}
});
