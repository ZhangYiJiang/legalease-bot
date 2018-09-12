# -*- coding: utf-8 -*-
from meya import Component
from meya.cards import File
import form_api

TEMPLATE_ID = "tpl_E3srgedRdHXXyAX2Gr"


class LpaForm(Component):
    def start(self):
        client = form_api.Client()
        client.api_client.configuration.username = self.db.bot.settings["form_api_key"]
        client.api_client.configuration.password = self.db.bot.settings["form_api_secret"]
        
        # JSON schema: https://app.formapi.io/api/v1/templates/tpl_E3srgedRdHXXyAX2Gr/schema.json?pretty=1
        data = {
            "donar": {
                'dob':           self.db.user.get('parsed_birthday'),
                'id':            self.db.user.get('ic_number'),
                'name':          self.db.user.get('ic_name'),
                'issue_country': self.db.user.get('ic_country') or 'Singapore',
                'address':       self.db.user.get('ic_address'),
                'is_nric':       self.db.user.get('ic_type') == 'NRIC',
            },
            "donee": []
        }
        
        submission = client.generate_pdf({
          "template_id": TEMPLATE_ID,
          "test": True,
          "data": data,
        })
        
        # Meya has a bug where it can't handle underscores in links properly
        # So we encode them to make them work
        download_url = submission.download_url.replace('_', '%5F')
        
        text = self.create_message(text='Your form is ready!')
        card = self.create_message(card=File(url=download_url))
        
        return self.respond(messages=[text, card], action="next")
