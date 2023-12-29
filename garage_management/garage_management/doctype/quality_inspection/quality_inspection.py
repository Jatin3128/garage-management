# Copyright (c) 2023, j and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document



        
class QualityInspection(Document):
	
	def validate(self):
		count = 0
		numRows = len(self.inspection_details)
		for row in self.get("inspection_details"):
			if row.rating_1 and row.rating_2:
				average = (float(row.rating_1) + float(row.rating_2))/2
				parameter_dict = frappe.db.get_value('Parameter', row.parameter, ['min_acceptable_value', 'max_acceptable_value'], as_dict=1)
				parameter_dict.min_acceptable_value
				parameter_dict.max_acceptable_value
				# frappe.throw(f"{parameter_dict}")
				if parameter_dict.min_acceptable_value <= average and parameter_dict.max_acceptable_value >= average:
					row.status = 1
					count +=1
				else:
					row.status = 0
			if count >= numRows/2:
		# frappe.db.set_value('Quality Inspection', 'overall_rating', "Passed")
				self.state = "Passed"
			elif count< numRows/2: 
				self.state = "Rejected"
			# frappe.throw(f"{numRows}")
	def before_submit(self):
		if self.state == "Passed":
		# frappe.db.set_value('Quality Inspection', 'overall_rating', "Passed")
			self.overall_rating = "Passed"
		else: 
			self.overall_rating = "Rejected"
	def on_update(self):
		frappe.db.set_value('Service Card', self.service_reference_number, 'qi_status', self.overall_rating)
		if self.overall_rating == "Passed":
			frappe.set_value('Service Card', self.service_reference_number, 'workflow_state', 'Approved')
			frappe.set_value('Job Cards', self.job_reference_number, 'delivery_date', self.service_complition_date)
			frappe.set_value('Job Cards', self.job_reference_number, 'workflow_state', 'submitted')
		elif self.overall_rating == "Rejected":
			frappe.set_value('Service Card', self.service_reference_number, 'workflow_state', 'Rejected')
	
		# frappe.thmsgprint(f"{self.workflow_state}")
		if self.workflow_state == "rejected":
			pass
	

			
		
		