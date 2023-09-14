from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_sellers(self, params=False):
        self.ensure_one()
        res = super()._prepare_sellers(params)
        to_remove = self.env["product.supplierinfo"]

        for record in res.filtered(lambda p: p.apply_on_ptav_ids and not p.product_id):
            if not self._match_all_variant_values(record.apply_on_ptav_ids):
                to_remove |= record

        return res - to_remove


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    possible_ptav_ids = fields.Many2many(
        "product.template.attribute.value", compute="_compute_possible_ptav_ids"
    )
    apply_on_ptav_ids = fields.Many2many(
        "product.template.attribute.value",
        string="Apply on Variants",
        ondelete="restrict",
        domain="[('id', 'in', possible_ptav_ids)]",
    )

    @api.depends(
        "product_tmpl_id.attribute_line_ids.value_ids",
        "product_tmpl_id.attribute_line_ids.attribute_id.create_variant",
        "product_tmpl_id.attribute_line_ids.product_template_value_ids.ptav_active",
    )
    def _compute_possible_ptav_ids(self):
        for record in self:
            # Disable formatting as black attempts to make this 1 very very
            # large line
            # fmt: off
            record.possible_ptav_ids = (
                record
                .product_tmpl_id
                .valid_product_template_attribute_line_ids
                ._without_no_variant_attributes()
                .product_template_value_ids
                ._only_active()
            )
            # fmt: on
