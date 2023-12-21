// Copyright (c) 2023, j and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Cards', {
	
	validate(frm) {
		let totalAmount = 0;
		for (let row of frm.doc.job_item) {
			if (row.amount){
				totalAmount += row.amount
			}

		}
		frm.set_value("total_amount", totalAmount)
		
	},
	after_save(frm) {
		if (frm.doc.total_amount > frm.doc.advance_amount) {
			frm.set_value("paid_amount", frm.doc.total_amount - frm.doc.advance_amount)
		}
		else {
			frappe.throw("advance is greater")
			frm.set_value("paid_amount", "")
		}
		if (!frm.doc.service_card_refernce_number) {
			let fl = [];
			for(let each of frm.doc.job_item){
				if (each.item_type === "Service"){
					fl.push(each)
				}
			}
			// create new service card
			
			frappe.db.insert({
				doctype: 'Service Card',
				reference_number: frm.doc.name,
				service_item: fl
			}).then(r => {
				console.log(r);
				frm.set_value("service_card_refernce_number", r.name)
			})
		}


	},
	before_submit(frm) {
		frm.set_value("delivery_date", frappe.format(new Date(), { fieldtype: "Date" }))

	},
	setup(frm) {
		frm.set_query("last_service_number", function () {
			return {
				"filters": {

					"docstatus": 1
				}
			};
		});
	}
});


frappe.ui.form.on('Job Item', {
	rate(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.rate && row.quantity) {
			if (row.rate > 0) {
				row.amount = row.quantity * row.rate
				frm.refresh_field("job_item")
			}
			else {
				frappe.throw('rate invalid')

			}
		}

	},
	quantity(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.quantity && row.rate) {
			if (row.quantity > 0) {
				row.amount = row.quantity * row.rate
				frm.refresh_field("job_item")
			}
			else {
				frappe.throw('Quantity invalid')

			}
		}

	}
});



