
from datetime import (datetime, timezone)
import phonenumbers
import requests
from passlib.hash import sha256_crypt
from phonenumbers import NumberParseException, PhoneNumber, carrier, timezone, PhoneNumberMatcher, geocoder, geodata
from py2neo.ogm import Model, Repository
from py2neo.ogm import  Node, Label,  Property, Related, RelatedTo, RelatedFrom

from app import db
from app.controllers.utils.mobile_verification import MobileVerification


class Person(Model):
    __primarylabel__ = 'Person'
    __primarykey__ = 'first_name'

    first_name = Property()
    last_name = Property()
    middle_name = Property()
    title = Property()
    birth_day = Property()
    image = Property()

    system_accounts = RelatedTo('System_Account')
    employed_by = RelatedTo('Company')
    phone_numbers = RelatedTo('Phone')
    
    def fetch(self, _id):
        return Person.match(db.repo, _id).first()
    
    def fetch_by_first_and_last(self):
        return Person.match(db.repo).where(
            f'_.first_name = "{self.first_name}" AND _.last_name = "{self.last_name}"'
        ).first()
    
    @classmethod
    def create_new(cls, first_name, last_name, middle_name=None, title=None, birth_day=None, image=None):
        return cls(first_name=first_name, last_name=last_name, middle_name=middle_name,
                    title=title, birth_day=birth_day, image=image)

    def save(self):
        db.repo.save(self)

class Phone(Model):
    __primarylabel__ = 'Phone'
    __primarykey__ = "phone_number"

    phone_number = Property()
    national_format = Property()
    international_format= Property()
    e164_format = Property()
    likely_region = Property()
    get_timezone = Property()
    likely_timezone = Property()
    likely_carrier = Property()
    line_type = Property()
    shared_line = Property()
    personal_line = Property()
    company_line = Property()
    is_validated = Property()
    sms_capable = Property()
    push_capable = Property()

    indivdual_phoneline = RelatedFrom('Person', 'PHONE_NUMBERS')
    company_phoneline = RelatedFrom('Company', 'PHONE_NUMBERS') 

    def get(self):
        return self.match(db.repo, self.phone_number).first()
    
    def exists(self):
        check = self.get()
        if check:
            return True
        return False
    
    def save(self):
        db.repo.save(self)
    
    @classmethod
    def create_new(cls, new_phone_number, shared_line=None, personal_line=None, company_line=None):
        phone_number = phonenumbers.parse(new_phone_number)
        is_possible = phonenumbers.is_possible_number(phone_number)
        is_valid = phonenumbers.is_valid_number(phone_number)
        if is_possible is True and is_valid is True:
            is_validated = True
            national_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            international_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164 )
            likely_carrier = str(Phone.get_carrier(e164_format))
            likely_region = geocoder.description_for_number(phone_number, 'en')
            likely_timezone =  timezone.time_zones_for_number(phone_number)
            line_type =  MobileVerification(e164_format).line_type()
            is_shared_line = shared_line
            is_personal_line = personal_line
            is_company_line = company_line
            return cls(phone_number=e164_format, national_format=national_format, international_format=international_format,
                        e164_format=e164_format, likely_region=likely_region, likely_timezone=likely_timezone,
                    likely_carrier=likely_carrier, line_type=line_type, is_shared_line=is_shared_line,
                    is_personal_line=is_personal_line, is_company_line=is_company_line, is_validated=is_validated,
                    sms_capable=False, push_capable=False)
        
    @staticmethod
    def get_carrier(phone_number):
        try:
            response = requests.get('https://api.telnyx.com/v1/phone_number/'+phone_number, timeout=5)
            #response.raise_for_status()
            data = response.json()
            # Code here will only run if the request is successful
        except requests.exceptions.HTTPError:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
            return None
                
        return data["carrier"]["name"]


class System_Account(Model):
    __primarylabel__ = 'System_Account'
    __primarykey__ = "email"

    username = Property()
    email = Property()
    hashed_password =Property()
    is_active = Property() 

    user_account = RelatedFrom('Person', 'USER_ACCOUNT') 
    
    @classmethod
    def create_new(cls, username, email, password, is_active=False):
        return cls(username=username, email=email, is_active=is_active)
    
    def verify_password(self, input_password):
        return sha256_crypt.verify(input_password, self.hashed_password)

    def save(self):
        db.repo.save(self)

class Company(Model):
    __primarylabel__ = 'Company'
    __primarykey__ = 'display_name'

    company_name = Property()
    company_url = Property()
    company_logo = Property()
    company_type = Property()
    duns = Property()
    figi = Property()
    foundedYear = Property()
    locationsCount = Property()
    long_description = Property()
    short_description = Property()
    status = Property()
    stock_ticker = Property()
    tax_id = Property()
    homepage_url = Property()
    blog_url = Property()
    craft_url = Property()
    crunchbase_url = Property()
    facebook_url = Property()
    instagram_url = Property()
    linkedin_url = Property()
    pinterest_url = Property()
    twitter_url = Property()
    youtube_url = Property()

    parent_company = RelatedFrom('Company')
    employees = RelatedFrom('People', 'EMPLOYED_BY')
    phonenumbers = RelatedFrom('Phone', 'COMPANY_PHONELINE')
    locations = RelatedFrom('Places', 'ADDRESS')

    @classmethod
    def create_new(cls, company_name, company_url, company_logo):
        return cls()

    def save(self):
        db.repo.save(self)

    
class Places(Model):
    __primarylabel__ = 'Places'
    __primarykey__ = 'address'

    address = Property()

