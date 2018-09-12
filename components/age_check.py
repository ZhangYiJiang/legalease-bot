# -*- coding: utf-8 -*-
from meya import Component
from datetime import datetime, date
import dateparser

AGE_LIMIT = 21

class AgeCheck(Component):
    def start(self):
        age = self.db.user.get('raw_birthday')
        
        try:
            parsed_birthday = dateparser.parse(age, settings={'DATE_ORDER': 'DMY'})
            if not parsed_birthday:
                raise ValueError()
            birthday = parsed_birthday.date()
        except ValueError:
            return self.respond(message=None, action="parse_fail")
        
        self.db.user.set('parsed_birthday', birthday.strftime('%d-%m-%Y'))
        
        if date(birthday.year + AGE_LIMIT, birthday.month, birthday.day) < date.today():
            return self.respond(message=None, action="y")
        else:
            return self.respond(message=None, action="n")
