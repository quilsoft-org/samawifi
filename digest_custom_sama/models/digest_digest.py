from odoo import fields, models, _
from datetime import datetime
from werkzeug.urls import url_join


class DigestDigestInherit(models.Model):
    _inherit = 'digest.digest'

    def _get_kpi_compute_parameters(self):
        return fields.Date.to_string(self._context.get('start_date')), fields.Date.to_string(self._context.get('end_date')), self.company_id

    def _action_send_to_user(self, user, tips_count=1, consum_tips=True):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        rendered_body = self.env['mail.render.mixin']._render_template(
            'digest.digest_mail_main',
            'digest.digest',
            self.ids,
            engine='qweb',
            add_context={
                'title': self.name,
                'top_button_label': _('Connect'),
                'top_button_url': url_join(web_base_url, '/web/login'),
                'company': self.company_id,
                'user': user,
                'tips_count': tips_count,
                'formatted_date': datetime.today().strftime('%B %d, %Y'),
                'display_mobile_banner': True,
                'kpi_data': self.compute_kpis(self.company_id, user),
                'tips': self.compute_tips(self.company_id, user, tips_count=tips_count, consumed=consum_tips),
                'preferences': self.compute_preferences(self.company_id, user),
            },
            post_process=True
        )[self.id]
        full_mail = self.env['mail.render.mixin']._render_encapsulate(
            'digest.digest_mail_layout',
            rendered_body,
            add_context={
                'company': self.company_id,
                'user': user,
            },
        )
        # create a mail_mail based on values, without attachments
        mail_values = {
            'auto_delete': True,
            'email_from': (
                self.company_id.partner_id.email_formatted
                or self.env.user.email_formatted
                or self.env.ref('base.user_root').email_formatted
            ),
            'email_to': user.email_formatted,
            'body_html': full_mail,
            'state': 'outgoing',
            'subject': '%s: %s' % (self.company_id.name, self.name),
            'author_id': user.partner_id.id,
        }
        mail = self.env['mail.mail'].sudo().create(mail_values)
        return True
