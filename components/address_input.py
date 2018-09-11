# -*- coding: utf-8 -*-
from meya import Component


class AddressInput(Component):
    def start(self):
        text = "Hello, world!"
        message = self.create_message(text=text)
        return self.respond(message=message, action="next")
