# -*- coding: utf-8 -*-
import requests
import urllib
import re
from meya import Component

POSTAL_REGEX = re.compile(r'\d{6}')


# Convert the user's address into latlng using OneMap
class GeocodeAddress(Component):
    def start(self):
        address = self.db.user.get('ic_address')
        postal_codes = re.findall(POSTAL_REGEX, address)
        
        if postal_codes:
            code = postal_codes[0]
            response = requests.get(
                'https://developers.onemap.sg/commonapi/search?searchVal={}&returnGeom=Y&getAddrDetails=N'.format(code)
            ).json()
            
            if response['results']:
                result = response['results'][0]
                self.db.user.set('lat', result['LATITUDE'])
                self.db.user.set('lng', result['LONGITUDE'])
            
        return self.respond(message=None, action="next")
