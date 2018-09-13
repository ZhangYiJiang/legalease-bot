# -*- coding: utf-8 -*-
from meya import Component
from geopy.distance import distance
from meya.cards import List, Element, Button
import urllib
import googlemaps

all_providers = [
    ['Lee Siu Lin', 'Enlight Family Clinic', '226C, Ang Mo Kio Avenue 1 #01-649\nSingapore 563226', '64560022', 1.36714639333261, 103.839256956987],
    ['Yeo Cheng Hsun Jonathan', 'Family Medicine Clinic Chinatown', '133, New Bridge Road #02-09/10\nSingapore 059413', '62255155', 1.28499882847404, 103.844697081142],
    ['Tan Sai Tiang', 'Hua Mei Clinic', '298, Tiong Bahru Road #15-01/06, Central Plaza Singapore 168730', '65939530', 1.28629937187779, 103.828093503404],
    ['See Shean Yaw', 'Make-Well Family Clinic & Surgery', '70, Toa Payoh Lorong 4\n#01-351\nSingapore 310070', '62534235', 1.33444874946939, 103.852333287558],
    ['Ng Wei Seng', 'London (MH) Clinic & Surgery', '104, Hougang Avenue 1\n#01-1123\nSingapore 530104', '62807262', 1.35478438666058, 103.890318475929],
    ['Tham Tuck Seng', 'Camry Medical Centre', '95, Toa Payoh Lorong 4\n#01-66\nSingapore 310095', '62580553', 1.33889072150038, 103.848993316875],
    ['Saiful Nizam Bin Subari', 'MyHealth Medical Centre', '501, West Coast Drive #01-256\nSingapore 120501', '68726920', 1.31231254760546, 103.759312529215],
    ['Yeap Eng Hooi', "Wee's Clinic and Surgery", '418, Bedok North Avenue 2\n#01-79\nSingapore 460418', '64445316', 1.32856421177176, 103.930036524233],
    ['Lim Wee Ni', 'Lim Clinic', '7, Wallich Street #B1-15\nSingapore 078884', '63868980', 1.27672492702289, 103.845155395387],
    ['Tan Ru Yuh', 'Victoria Medical House', '888, Woodlands Drive 50\n#02-739, 888 Plaza\nSingapore 730888', '63647551', 1.43712301500436, 103.795314383823],
    ['Tan Shen Kiat', 'Fortis Law Corporation', '24, Raffles Place\n#29-05 Clifford Centre\nSingapore 048621', '65323848', 1.28385590711691, 103.85213030831],
    ['Tan Kwee Sain Pauline', 'P Tan & Co', '133, New Bridge Road #15-07 Chinatown Point\nSingapore 059413', '65385263', 1.28499882847404, 103.844697081142],
    ['Ho Soon Wah Daniel', 'Summit Law Corporation', '61, Robinson Road\n#15-02 Robinson Centre\nSingapore 068893', '65978363', 1.27926171654784, 103.849345796307],
    ['Yeo Poh Tiang, Beatrice', 'Yeo & Associates LLC', '47A Circular Road Singapore 049402', '62203400', 1.28607369378752, 103.849523073043],
    ['Khoo Aik Yeow', 'AY Khoo Law Chambers', '150, South Bridge Road #03-07 Fook Hai Building Singapore 058757', '64566146', 1.28346171522876, 103.845742497301],
    ['Joan Lim Pheck Hoon', 'Legal Options LLC', '20, Havelock Road\n#02-46 Central Square\nSingapore 059765', '64388039', 1.28815884529188, 103.843285805896],
    ['Jacintha Pillay D/O Rajagopal Pillay', 'Sim Mong Teck & Partners', '490 Lorong 6 Toa Payoh\nHDB Hub #03-18\nSingapore 310490', '64787878\n63566962', 1.33256788157965, 103.848418805864],
    ['Tan Chye Kwee', 'Tan Chye Kwee', '133, New Bridge Road #11-06 Chinatown Point\nSingapore 059413', '65383330', 1.28499882847404, 103.844697081142],
    ['Kok Lak Hin', 'Fortis Law Corporation', '24, Raffles Place\n#29-05 Clifford Centre\nSingapore 048621', '65323848', 1.28385590711691, 103.85213030831],
    ['Lee Kim Kee', 'K K Lee Law Corporation', '511, Guillemard Road\n#03-13 Grandlink Square\nSingapore 399849', '67440419', 1.31419129803568, 103.891500511283],
    ['Ong Seh Hong', 'Department of Psychological Medicine, Khoo Teck Puat Hospital', '90 Yishun Central\nSingapore 768828', '66020699', 1.42408101871824, 103.83857888869],
    ['Yong Mo Juin', 'Khoo Teck Puat Hospital', '90 Yishun Central\nSingapore 768828', '66023041', 1.42408101871824, 103.83857888869],
    ['Ong Pui Sim', 'Changi General Hospital', '11, Jalan Tan Tock Seng Singapore 308433', '67888833', 1.31989910062863, 103.85194511373],
    ['Tan Wee Lun', 'Nobel Psychological Wellness Clinic', '452 Ang Mo Kio Ave 10\nSingpaore 560452', '64592630', 1.3688975113138, 103.856200835147],
    ['Kwan Yunxin', 'Tan Tock Seng Hospital', '11 Department of Psychological Medicine  #Clinic 4A-4\nJalan Tan Tock Seng Singapore 308433', '63577841', 1.31989910062863, 103.85194511373],
    ['Teoh Si Jing Lynnette', 'Department of Psychological Medicine, Tan Tock Seng Hospital', '11, Jalan Tan Tock Seng Singapore 308433', '63577841', 1.31989910062863, 103.85194511373],
    ['Tsoi Tung', 'National University Hospital, Psychological Medicine', '5, Lower Kent Ridge Road Singapore 119074', '67795555', 1.29442025984977, 103.783686904855],
    ['Ang Lye Poh Aaron', 'Tan Tock Seng Hospital', '11, Jalan Tan Tock Seng Singapore 308433', '62566011', 1.31989910062863, 103.85194511373],
    ['Tan Soo Teng', 'Clinic B, Institute of Mental Health', '10 Buangkok View\nSingapore 539747', '63892000', 1.38159451793257, 103.885209972539]
]

def nearest(lat, lng):
    return sorted(all_providers, key=lambda p: distance((p[-2], p[-1]), (lat, lng)))


def map_url(key, lat, lng):
    params = urllib.urlencode({
        'key': key,
        'markers': '{},{}'.format(lat, lng),
        'size': '150x150',
        'scale': 2,
    })
    
    return 'https://maps.googleapis.com/maps/api/staticmap?' + params
    
def place_photo_url(key, reference):
    params = urllib.urlencode({
        'key': key,
        'photoreference': reference,
        'maxwidth': 250,
        'maxheight': 250,
    })
    
    return 'https://maps.googleapis.com/maps/api/place/photo?' + params


class NearestCertification(Component):
    def start(self):
        lat = self.db.user.get('lat')
        lng = self.db.user.get('lng')
        map_key = self.db.bot.settings['google_cloud_key']
        gmap_client = googlemaps.Client(key=map_key)
        
        # Look for nearest certificate issuers
        providers = nearest(lat, lng)
        
        elements = []
        for name, firm, address, tel, plat, plng in providers[:3]:
            d = distance((plat, plng), (lat, lng))
            
            # Try to use Google Places API to find a photo of the place
            image = None
            try:
                place_response = gmap_client.find_place(
                    input=firm, 
                    input_type='textquery', 
                    fields=['icon', 'photos'], 
                    location_bias='point:{},{}'.format(plat, plng),
                )
                
                if place_response['candidates']:
                    place = place_response['candidates'][0]
                    
                    if place['photos']:
                        image = place_photo_url(map_key, place['photos'][0]['photo_reference'])
                    elif place['logo']:
                        image = place['logo']
            except Exception as e:
                self.log({ 'error': str(e), 'place': firm }, status='error', type='places_error')
                    
            default_action = Button(url="https://www.google.com/maps/search/?api=1&query=" + urllib.quote_plus(address))
            call_btn = Button(text="Call", url="tel://" + tel)
            element = Element(title=name,
                              subtitle="{:.2f}km, {}".format(d.km, firm),
                              buttons=[call_btn],
                              image_url=image,
                              default_action=default_action)
            
            elements.append(element)
        
        show_all_btn = Button(text="View More", url="https://www.publicguardian.gov.sg/opg/Pages/The-LPA-Where-to-find-a-Certificate-Issuer.aspx")
        card = List(elements=elements,
                    buttons=[show_all_btn],
                    top_element_style="compact")
        
        return self.respond(messages=[
            self.create_message(text="Here are the nearest certification providers"),
            self.create_message(card=card),
        ], action="next")
