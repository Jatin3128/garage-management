# Copyright (c) 2023, j and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ServiceCard(Document):
	def on_update(self):
		# frappe.thmsgprint(f"{self.workflow_state}")
		if self.workflow_state == "inspection Pending":
			# getting job item from job card
			jobcard = frappe.get_doc('Job Cards', self.reference_number)
			itemlist = []
			for row in jobcard.job_item:
				if row.item_type not in itemlist:
					itemlist.append(row.item_type)
			item_type_parameter={}
			for itemtype in itemlist:
				parameterlist=frappe.db.get_list('Parameter',
				filters={
					'item_type': itemtype
				},
				pluck='name')
				item_type_parameter[itemtype] = parameterlist
			# frappe.throw(f"{item_type_parameter}")
			inspection_item = []
			for key,value in item_type_parameter.items():
				for parameter in value:
					parameter_dict = {}
					parameter_dict["parameter"] = parameter
					inspection_item.append(parameter_dict)
			# frappe.throw(f"{inspection_item}")
							
			# create a new document
		
			qi_doc = frappe.get_doc({
				'doctype': 'Quality Inspection',
				'job_reference_number': self.reference_number,
				'service_reference_number': self.name,
				'inspection_details':inspection_item
			})
			qi_doc.insert()
			# self.qi_ref = qi_doc.name
			frappe.db.set_value('Service Card', self.name, 'qi_ref', qi_doc.name)

