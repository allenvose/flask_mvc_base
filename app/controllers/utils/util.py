# -*- encoding: utf-8 -*-
"""

"""
 
import hashlib, binascii, os
import requests, json
from requests.api import request
from pprint import pprint as pp

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

class PeopleDataAPI():

    api_header = {'accept': "application/json",'content-type': "application/json", 'x-api-key': '3ddc66dad79fd74aef2eed61dfe69129c8c41c2d336dddcfcbf89ce6e024b80a'}
    company_encrichment_url = 'https://api.peopledatalabs.com/v5/company/enrich'
    person_encrichment_url = 'https://api.peopledatalabs.com/v5/person/enrich'
      
    def company_encrichment(self, name=None, profile=None, website=None, location=None,
                            locality=None, region=None, country=None,
                            street_address=None, postal_code=None, save_file=False) -> requests.Response.json:

        self.company_query = {key:value for (key,value) 
                                in  {'name': name,  'profile': profile, 'website': website, 'location': location,
                                    'locality': location,'region' : region,'country': country,
                                    'street_address': street_address, 'postal_code': postal_code}.items()
                                if value}

        result = self.get_response(url=self.company_encrichment_url, headers=self.api_header, params=self.company_query).json()
        print(result)

        #####THIS IS TEMPORARY####
        if save_file:
            with open('/home/vscode/flask/results/company/'+str(result['name'])+'.json', 'w') as json_file:
                json.dump(result, json_file)

        ####################
        return result
    


    def person_encrichment(self, name=None, first_name=None, last_name=None, middle_name=None,
                            location=None, street_address=None, locality=None, region=None, country=None, postal_code=None,
                            company=None, school=None, phone=None, email=None, profile=None, lid=None, birth_date=None) -> requests.Response.json:

        self.person_query = {key:value for (key,value) 
                                in  {'name': name , 'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name,
                            'location': location, 'street_address': street_address, 'locality': locality, 'region': region, 'country': country, 'postal_code': postal_code,
                            'company': company, 'school': school, 'phone': phone, 'email': email, 'profile': profile, 'lid': lid, 'birth_date': birth_date}.items()
                                if value}

        return self.get_response(url=self.person_encrichment_url, headers=self.api_header, params=self.person_query).json()
   
    @staticmethod
    def get_response(url, headers, params):
        return requests.request('Get', url=url, headers=headers, params=params)

   

def hash_pass( password ):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def get_company_logo_name(name_domain):
    r = requests.get(f'https://autocomplete.clearbit.com/v1/companies/suggest?query={name_domain}')
    details = requests.get(f'https://financialmodelingprep.com/api/v3/profile/csco?apikey=0123f5d0cfb5691cc66a39467f7371cd')
    return [r.json(), details.json()]
    

if __name__ == '__main__':
    company = PeopleDataAPI()
    pp(company.company_encrichment(name='Cisco',  website='cisco.com ', save_file=True))
    #(company.person_encrichment(first_name='Chris', last_name='Butler', company='iSenpai', save_file=True))
    
    