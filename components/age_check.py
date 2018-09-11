# -*- coding: utf-8 -*-
from meya import Component
from datetime import datetime, date

AGE_LIMIT = 21

class AgeCheck(Component):
    def start(self):
        age = self.db.user.get('raw_birthday')
        # TODO: Replace this with https://dateparser.readthedocs.io/en/latest/
        
        try:
            birthday = datetime.strptime(age, '%d-%m-%Y').date()
        except ValueError:
            return self.respond(message=None, action="parse_fail")
        
        if date(birthday.year + AGE_LIMIT, birthday.month, birthday.day) < date.today():
            return self.respond(message=None, action="y")
        else:
            return self.respond(message=None, action="n")
