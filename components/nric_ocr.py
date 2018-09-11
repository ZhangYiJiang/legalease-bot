import re
import requests
from google.cloud import vision
from google.oauth2 import service_account
from meya import Component

NRIC_REGEX = re.compile(r"[STFG]\d{7}[A-Z]")
POSTAL_REGEX = re.compile(r"SINGAPORE\s+\d{6}")
UNIT_NUMBER_REGEX = re.compile(r"#\d{1,3}-\d{1,5}")


def first_index(lst):
    for i, element in enumerate(lst):
        if element:
            return i
    return None


class NricOcr(Component):
    def log_parse_error(self, error, message, ocr_text):
        context = { 
            'error': e,
            'message': message,
            'ocr_text': ocr_text,
        }
        
        self.log(context, status='error', type='parse_error')
    
    def start(self):
        # Set up the Google Vision client
        credentials = service_account.Credentials.from_service_account_info(
            self.db.bot.settings['google_cloud_credentials']
        )
        client = vision.ImageAnnotatorClient(credentials=credentials)
        
        image_url = self.db.flow.get('ic_image')
        self.log({ 'image_url': image_url }, status='info', type='google_vision')
        
        # Have to download the image first, otherwise Vision API refuse to 
        # work with the file
        image_contents = requests.get(image_url).content
        image = vision.types.Image(content=image_contents)
        response = client.text_detection(image=image)
        
        if response.error:
            self.log({ 'error': str(response.error) }, status='error', type='google_vision')

        # These recognitions are pretty weak, but let's use them for now
        ocr_text = response.full_text_annotation.text
        lines = ocr_text.split('\n')
        self.log({ 'ocr_text': ocr_text }, status='info', type='google_vision')
        
        # NRIC recognition
        try:
            nric = re.findall(NRIC_REGEX, ocr_text)
            if nric:
                self.db.user.set('ic_number', nric[0])
        except Exception as e:
            log_parse_error(e, 'Error parsing NRIC number', ocr_text)
        
        # Name recognition - assume the line after "Name" is the name
        try:
            name_line = first_index(l.strip().upper() == 'NAME' for l in lines)
            if name_line is not None:
                self.db.user.set('ic_name', lines[name_line + 1].strip())
        except Exception as e:
            log_parse_error(e, 'Error parsing NRIC name', ocr_text)
        
        # Address recognition - postal code + unit number (optional) + one line above
        try:
            address = None
            unit_line = first_index(re.findall(UNIT_NUMBER_REGEX, l) for l in lines)
            postal_line = first_index(re.findall(POSTAL_REGEX, l) for l in lines)
            
            if unit_line is not None:
                address = ' '.join([lines[unit_line-1], lines[unit_line], lines[unit_line+1]])
            elif postal_line is not None:
                address = ' '.join([lines[postal_line-1], lines[postal_line]])
            
            if address:
                self.db.user.set('ic_address', address)
        except Exception as e:
            log_parse_error(e, 'Error parsing address name', ocr_text)
            
        return self.respond(message=None, action="next")
