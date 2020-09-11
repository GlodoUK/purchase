from odoo import _, api, fields, models  # noqa


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _make_po_get_domain(self, values, partner):
        domain = super(StockRule, self)._make_po_get_domain(values, partner)
        if partner.property_supplier_consolidation == "consolidate":
            return domain

        so = self.env["sale.order"].search(
            [("order_line", "in", values.get("sale_line_id"))]
        )
        domain += (("order_line.sale_line_id.order_id", "=", so.id),)
        return domain


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_supplier_consolidation = fields.Selection(
        [("separate", "Separated"), ("consolidate", "Consolidated")], default="separate"
    )
