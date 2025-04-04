# -*- coding: utf-8 -*-
{
    "name": "Google Feed for Meta Catalog",
    "summary": """
        Generate an XML feed for Meta product catalogs from Odoo website products""",
    "author": "Filoquin",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Website",
    "version": "17.0.2.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["website_sale", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_google_feed_views.xml",
        "views/product_template_views.xml",
        "views/product_category_views.xml",
        "data/product_google_producttype.xml",
    ],
    "external_dependencies": {
        "python": ["lxml"],
        "bin": [],
    },
}
