# -*- coding: utf-8 -*-
from meya import Component

# Checks that all fields have been filled by the OCR
class LpaOcrCheck(Component):
    def start(self):
        
        message = self.create_message(text=text)
        return self.respond(message=message, action="next")
