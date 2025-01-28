import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

# Save the original method for reference (optional)
original_set_exchange_gain_loss = PaymentEntry.set_exchange_gain_loss

# Define the custom method
def custom_set_exchange_gain_loss(self):
    """
    Custom implementation of set_exchange_gain_loss.
    This method skips automatic calculation and allows manual entry.
    """
    # Your custom logic here
    frappe.msgprint("Custom set_exchange_gain_loss method is called!")

    # Example: Skip automatic calculation
    exchange_gain_loss = 0  # Default to 0, or you can remove this entirely

    # Identify existing exchange gain/loss rows
    exchange_gain_loss_rows = [row for row in self.get("deductions") if row.is_exchange_gain_loss]
    exchange_gain_loss_row = exchange_gain_loss_rows.pop(0) if exchange_gain_loss_rows else None

    # Remove extra exchange gain/loss rows (if any)
    for row in exchange_gain_loss_rows:
        self.remove(row)

    # If no exchange gain/loss is calculated, remove the existing row (if any)
    if not exchange_gain_loss:
        if exchange_gain_loss_row:
            self.remove(exchange_gain_loss_row)
        return

    # If no exchange gain/loss row exists, create one (optional, only if needed)
    if not exchange_gain_loss_row:
        values = frappe.get_cached_value(
            "Company", self.company, ("exchange_gain_loss_account", "cost_center"), as_dict=True
        )

        # Check if required fields are set in the Company
        for fieldname, value in values.items():
            if value:
                continue

            label = _(frappe.get_meta("Company").get_label(fieldname))
            frappe.msgprint(
                _("Please set {0} in Company {1} to account for Exchange Gain / Loss").format(
                    label, get_link_to_form("Company", self.company)
                ),
                title=_("Missing Default in Company"),
                indicator="red" if self.docstatus.is_submitted() else "yellow",
                raise_exception=self.docstatus.is_submitted(),
            )

        # Append a new row for exchange gain/loss (optional, only if needed)
        exchange_gain_loss_row = self.append(
            "deductions",
            {
                "account": values.exchange_gain_loss_account,
                "cost_center": values.cost_center,
                "is_exchange_gain_loss": 1,
            },
        )

    # Set the exchange gain/loss amount (optional, only if needed)
    exchange_gain_loss_row.amount = exchange_gain_loss

# Replace the original method with the custom one
PaymentEntry.set_exchange_gain_loss = custom_set_exchange_gain_loss