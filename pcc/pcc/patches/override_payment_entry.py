import frappe
import json
from frappe import _
from frappe.model.document import Document
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

class CustomPE(PaymentEntry):
    def set_amounts(self):
        self.set_received_amount()
        self.set_amounts_in_company_currency()
        self.set_total_allocated_amount()
        self.set_unallocated_amount()
        self.set_difference_amount()
