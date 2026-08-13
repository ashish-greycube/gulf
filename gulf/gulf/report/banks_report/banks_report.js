// Copyright (c) 2026, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Banks Report"] = {
	"filters": [
		{
			fieldname: "date",
			fieldtype: "Date",
			label: __("Date"),
			default: frappe.datetime.nowdate(),
			reqd: 1
		},
	]
};
