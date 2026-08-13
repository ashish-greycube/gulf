# Copyright (c) 2026, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def execute_snapshot_report(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for snapshot report. When 'Synced
	Report' is enabled in report, framework will call this method
	every time the report is refreshed or a filter is updated. It
	accepts the same filters as normal execute. But a utility method -
	get_latest_sync, is also imported.

	"""
	from frappe.database.duckdb.database import get_latest_sync

	columns, data = [], []
	return columns, data

def get_columns():
	columns = [
		{
			"fieldname": "pe_id",
			"label": "Payment Entry",
			"fieldtype": "Link",
			"options": "Payment Entry",
		},
		{
			"fieldname": "party_name",
			"label": "Party Name",
			"fieldtype": "Data",
		},
		{
			"fieldname": "project_name",
			"label": "Project Name",
			"fieldtype": "Data",
		},
		{
			"fieldname": "amount",
			"label": "Amount",
			"fieldtype": "Currency",
		},
		{
			"fieldname": "date",
			"label": "Date",
			"fieldtype": "Date",
		},
		{
			"fieldname": "remarks",
			"label": "Remarks",
			"fieldtype": "Data",
		},
		{
			"fieldname": "transfer_status",
			"label": "Transfer Status",
			"fieldtype": "Data",
		},
	]
	return columns

def get_data(filters):

	condition = ""
	if filters.get("from_date") and filters.get("to_date"):
		condition = "AND pe.posting_date BETWEEN '{0}' AND '{1}'".format(filters.get('from_date'), filters.get('to_date'))
		
	return frappe.db.sql("""
		SELECT
			pe.name AS pe_id,
			pe.party AS party_name,
			pe.custom_project_name AS project_name,
			pe.paid_amount AS amount,
			pe.posting_date AS date,
			pe.remarks AS remarks,
			pe.custom_transfer_status AS transfer_status
		FROM
			`tabPayment Entry` pe
		WHERE
			pe.payment_type = '{0}'
			{1}
	""".format(filters.get("payment_type"), condition), as_dict=1)
