# -*- coding: utf-8 -*-
from meya import Component


class ClearUserData(Component):
    def start(self):
        self.db.user.put({})
        return self.respond(message=None, action="next")
