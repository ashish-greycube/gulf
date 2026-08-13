# Copyright (c) 2026, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe

from erpnext.accounts.report.general_ledger.general_ledger import execute as gl_execute
# erpnext/erpnext/accounts/report/general_ledger/general_ledger.py


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
	"""Return columns for the report."""
	columns = [
		{
			"fieldname": "bank_no",
			"label": "Bank Number",
			"fieldtype": "Data",
			"width": "150",
		},
		{
			"fieldname": "bank_name",
			"label": "Bank Name",
			"fieldtype": "Data",
			"width": "300",
		},
		{
			"fieldname": "balance",
			"label": "Balance",
			"fieldtype": "Currency",
			"width": "200",
		},
	]
	return columns

def get_data(filters):
	accounts_list =  frappe.db.sql("""
		SELECT
			a.account_number AS bank_no,
			a.account_name AS bank_name,
			a.name as acc_name
		FROM
			`tabAccount` a
		WHERE
			a.account_type = "Bank"
			AND a.is_group = "0"
	""", as_dict=1)

	for acc in accounts_list:
		gl_filters = frappe._dict({
			"company": frappe.defaults.get_user_default("Company"),
			"from_date": filters.get("date"),
			"to_date": filters.get("date"),
			"account": [acc.acc_name],
		})

		gl_report = gl_execute(gl_filters)
		gl_report_data = gl_report[1] if len(gl_report) > 1 else []
		total_balance = 0

		for row in gl_report_data:
			if row.get("account") == "'Closing (Opening + Total)'":
				total_balance += row.get("balance")

		acc["balance"] = total_balance

	return accounts_list
