===========
Google Feed for Meta Catalog
===========

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: https://onlyone.odoo.com/
    :alt: Be OnlyOne

|badge1| |badge2| |badge3| 

This module extends the functionality of Odoo’s website and product management to support generating an XML feed compatible with Meta’s product catalog platform (e.g., Facebook/Instagram). It allows you to export website-published products with pricing, taxonomy, and availability details.

**Table of contents**

.. contents::
   :local:

Install
=======

To install this module, you need to:

1. Ensure the Python library `lxml` is installed on your server:
   - Run `pip install lxml` in your Odoo environment.
2. Install the module via Odoo’s Apps menu or by adding it to your addons path and updating the module list.

Configure
=========

To configure this module, you need to:

1. Go to *Website > Configuration > Google Feed*.
2. Create a new feed:
   - Set a name and select a website.
   - Optionally, define a pricelist, domain filter (e.g., `[('website_published', '=', True)]`), and Google taxonomy.
   - Adjust the base URL if your shop route differs from `/shop/product/`.
3. Save the feed; the slug will be auto-generated.

Usage
=====

1. Go to *Website > Configuration > Google Feed*.
2. Open an existing feed or create a new one.
3. Access the XML feed at `/google_feed/<slug>` (e.g., `/google_feed/my-feed`) in your browser or provide this URL to Meta’s catalog system.
4. Assign Google taxonomy categories to products or categories via *Products > Products* or *Products > Categories* for precise categorization in the feed.

Known issues / Roadmap
======================

* **Known Issues**: None reported yet.
* **Roadmap**: Add support for multi-language descriptions in the XML feed.

Bug Tracker
===========

For issues, contact us at:
* Help Contact: <support@onlyone.odoo.com> (adjust to your actual support email)

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne