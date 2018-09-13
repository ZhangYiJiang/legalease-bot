# -*- coding: utf-8 -*-
from meya import Component
import regex as re

NRIC_REGEX = re.compile(r"[STFG]\d{7}[A-Z]")

class NricValidityCheck(Component):
    def start(self):
        ic = self.db.user.get('ic_number')
        match = re.search(NRIC_REGEX, ic)
        if match:
            return self.respond(message=None, action="valid")
        else:
            return self.respond(message=None, action="invalid")