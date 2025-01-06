import frappe


@frappe.whitelist()
def get_sales_goal_progress(employee):
    emp = frappe.db.get_list(doctype='Sales Person', filters = {'employee' : employee})
    if ((emp == None) or len(emp) == 0):
        frappe.msgprint("Employee is not registered as a Sales Person")
        return 0

    doc = frappe.get_doc('Sales Person', emp[0]['name'])
    targets = frappe.get_doc('Target Detail', doc.targets)
    if ((targets == None)):
        frappe.msgprint("No Targets set yet for Sales Person")
        return 0
    
    SQL = f""" 
    SELECT     SUM(st.allocated_amount) as total_amount 
    FROM     `tabSales Invoice` AS si 
    LEFT JOIN     `tabSales Team` AS st ON st.parent = si.name 
    WHERE  st.sales_person='{emp[0]['name']}'  
    AND  si.docstatus = 1  
    AND     YEAR(posting_date) = YEAR(CURDATE());
    """
    result = frappe.db.sql(SQL)
    print(f'TEST {employee} {emp} {doc.targets} {targets.target_amount} {result[0][0]}')

    if ((result == None) or (result [0][0] == None)):
        return 0


    if ((targets == None) or (targets.target_amount == None) or (targets.target_amount == 0)):
        return 0
    
    try:
        return round(result[0][0] / targets.target_amount * 100, 4)
    except:
        return 0