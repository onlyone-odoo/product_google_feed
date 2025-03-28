from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class GoogleFeed(http.Controller):
    @http.route(
        "/google_feed/<string:slug>", auth="public", website=True, methods=["GET"]
    )
    def google_feed(self, slug, **kwargs):
        feed_id = (
            request.env["product.google.feed"]
            .sudo()
            .search([("slug", "=", slug)], limit=1)
        )
        if feed_id:
            return request.make_response(
                feed_id.make_xml(), headers=[("Content-Type", "text/xml")]
            )
        return ""
