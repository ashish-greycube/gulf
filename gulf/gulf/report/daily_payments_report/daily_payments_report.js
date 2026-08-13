// Copyright (c) 2026, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Payments Report"] = {
	"filters": [
		{
			fieldname: "from_date",
			fieldtype: "Date",
			label: __("From Date"),
			default: frappe.datetime.add_months(frappe.datetime.nowdate(), -1),
		},
		{
			fieldname: "to_date",
			fieldtype: "Date",
			label: __("To Date"),
			default: frappe.datetime.nowdate(),
		},
		{
			fieldname: "payment_type",
			fieldtype: "Select",
			label: __("Payment Type"),
			reqd: 1,
			options: "Receive\nPay\nInternal Transfer",
			default: "Receive",
		},
	]
};
