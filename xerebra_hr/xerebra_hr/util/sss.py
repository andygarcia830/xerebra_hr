import frappe

@frappe.whitelist()
def get_computation():
    doc = frappe.get_doc('Localization Server Settings')
    return doc.sss_formula