from __future__ import unicode_literals
from frappe.utils import today
from frappe.core.doctype.prepared_report.prepared_report import run_background
from frappe.desk.query_report import get_report_doc

import frappe
import json


FILTERS = {
	"Accounts Receivable": {
		"company": "Service Lee Technologies Pvt Ltd",
		"range1": 30,
		"range2": 60,
		"range3": 90,
		"range4": 120,
		"report_date": today(),
		"ageing_based_on": "Posting Date"
	}
}


def generate_reports():
	"""reports generated by scheduler at midnight"""
	reports = ["Accounts Receivable"]
	for report in reports:
		report_doc = get_report_doc(report)
		prepared_report = frappe.new_doc("Prepared Report")
		prepared_report.update({
			"report_name": report,
			"filters": json.dumps(FILTERS.get(report, {})),
			"ref_report_doctype": report,
			"report_type": report_doc.report_type,
			"query": report_doc.query,
			"module": report_doc.module
		})
		prepared_report.save(ignore_permissions=True)
		run_background(prepared_report.name)

