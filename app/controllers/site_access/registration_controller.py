# -*- encoding: utf-8 -*-
"""

"""
from app import db
from app.models.site_access import Phone, Person, System_Account, Company

class UserRegistration():

    def __init__(self) -> None:
        self.username: str = None
        self.password: str = None
        self.first_name: str = None
        self.middle_name: str = None
        self.last_name: str= None
        self.company_association: str = None
        self.title: str = None
        self.sms_capable_phone: str = None
    
    def save(self):
        new_person = Person.create_new(self.first_name, self.last_name)
        new_phone = Phone.create_new(self.sms_capable_phone)
        new_account = System_Account.create_new(self.username, str(self.username+self.company_association), hashed_password=self.password)
        new_person.phone_numbers.add(new_phone)
        new_person.system_accounts.add(new_account)
        db.repo.save(new_person)

class CompanyRegistration():

    def __init__(self) -> None:
        self.company_name: str = None
        self.company_url: str = None
        self.company_logo: str = None
        
   
    def save(self):
        print(self.company_name, self.company_url, self.company_logo)
        new_company = Company.create_new(self.company_name, self.company_url, self.company_logo)
        print(new_company)
        db.repo.save(new_company)