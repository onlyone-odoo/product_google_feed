from odoo import models, fields, api
from lxml import etree, builder
from odoo.addons.http_routing.models.ir_http import slugify
import re
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)

MY_NAMESPACES = {
    "g": "http://base.google.com/ns/1.0",
    None: "http://base.google.com/ns/1.0",
}
CLEANTAG = re.compile("<.*?>")


class ProductGoogleProducttype(models.Model):
    _name = "product.google.producttype"
    _description = "Google Product Taxonomy Version"

    tax_id = fields.Integer(string="Taxonomy Id")
    name = fields.Char(string="Tax Description")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    producttype_id = fields.Many2one(
        "product.google.producttype", string="Google Taxonomy"
    )


class ProductCategory(models.Model):
    _inherit = "product.category"

    producttype_id = fields.Many2one(
        "product.google.producttype", string="Google Taxonomy"
    )


class ProductGoogleFeed(models.Model):
    _name = "product.google.feed"
    _description = "Product Google Feed"

    name = fields.Char(string="Feed", required=True)
    website_id = fields.Many2one("website", string="Website", required=True)
    base_url = fields.Char(string="Base URL", default="shop/product/")
    slug = fields.Char(string="Slug", compute="_compute_slug", store=True)
    domain = fields.Text(string="Domain", default="[('website_published', '=', True)]")
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    context = fields.Text(string="Context", default="{}")
    producttype_id = fields.Many2one(
        "product.google.producttype", string="Google Taxonomy"
    )
    price_total_included = fields.Boolean(string="Show Price Included", default=True)
    active = fields.Boolean(string="Active", default=True)
    limit = fields.Integer(string="Limit", default=100)

    @api.depends("name")
    def _compute_slug(self):
        for feed in self:
            feed.slug = slugify(feed.name) if feed.name else ""

    def get_feed_info(self, product_id, E):
        item = E.item()

        sku = etree.Element("{%s}id" % MY_NAMESPACES["g"])
        sku.text = product_id.default_code or f"p-{product_id.id}"
        item.append(sku)

        if product_id.barcode:
            gtin = etree.Element("{%s}gtin" % MY_NAMESPACES["g"])
            gtin.text = product_id.barcode
            item.append(gtin)

        if product_id.default_code:
            mpn = etree.Element("{%s}mpn" % MY_NAMESPACES["g"])
            mpn.text = product_id.default_code
            item.append(mpn)

        title = etree.Element("title")
        title.text = product_id.name
        item.append(title)

        description = etree.Element("description")
        desc = product_id.description_sale or product_id.name
        description.text = re.sub(CLEANTAG, "", desc) if desc else product_id.name
        item.append(description)

        availability = etree.Element("{%s}availability" % MY_NAMESPACES["g"])
        availability.text = "in stock" if product_id.free_qty > 0 else "preorder"
        item.append(availability)

        brand = etree.Element("{%s}brand" % MY_NAMESPACES["g"])
        brand_field = "brand_id"  # Adjust if using a custom brand module
        brand.text = (
            product_id[brand_field].name
            if brand_field in product_id and product_id[brand_field]
            else self.website_id.name
        )
        item.append(brand)

        link = etree.Element("link")
        link.text = f"{self.website_id.domain}/{self.base_url}{slugify(product_id)}"
        item.append(link)

        price = etree.Element("{%s}price" % MY_NAMESPACES["g"])
        if self.price_total_included and product_id.taxes_id:
            amount = product_id.taxes_id.compute_all(product_id.list_price)[
                "total_included"
            ]
        else:
            amount = product_id.list_price
        price.text = f"{amount:.2f} {self.env.company.currency_id.name}"
        item.append(price)

        if product_id.image_1920:
            image_link = etree.Element("{%s}image_link" % MY_NAMESPACES["g"])
            image_link.text = f"{self.website_id.domain}/web/image/product.template/{product_id.id}/image_1920/"
            item.append(image_link)

        condition = etree.Element("{%s}condition" % MY_NAMESPACES["g"])
        condition.text = "new"
        item.append(condition)

        if not product_id.default_code or not product_id.barcode:
            identifier_exists = etree.Element(
                "{%s}identifier_exists" % MY_NAMESPACES["g"]
            )
            identifier_exists.text = "no"
            item.append(identifier_exists)

        google_product_category = etree.Element(
            "{%s}google_product_category" % MY_NAMESPACES["g"]
        )
        category = (
            product_id.producttype_id
            or product_id.categ_id.producttype_id
            or self.producttype_id
        )
        google_product_category.text = str(category.tax_id) if category else ""
        item.append(google_product_category)

        return item

    def make_xml(self):
        self.ensure_one()
        domain = safe_eval(self.domain)
        context = safe_eval(self.context)
        if self.pricelist_id:
            context["pricelist"] = self.pricelist_id.id

        product_ids = (
            self.env["product.template"]
            .sudo()
            .with_context(context)
            .search(domain, limit=self.limit)
        )

        E = builder.ElementMaker()
        rss = etree.Element("rss", nsmap=MY_NAMESPACES, version="2.0")
        channel = E.channel(
            E.title(self.name), E.link(self.website_id.domain), E.description(self.name)
        )
        rss.append(channel)

        for product_id in product_ids:
            item = self.get_feed_info(product_id, E)
            channel.append(item)

        return etree.tostring(
            rss, xml_declaration=True, encoding="utf-8", pretty_print=True
        )
