# -*- encoding: utf-8 -*-
"""

"""

from app import db
from app.models.phone import Phone, Person, System_Account

class RegistrationSystem(): 
    username: str = None
    password: str = None
    first_name: str = None
    middle_name: str = None
    last_name: str= None
    company_association: str = None
    title: str = None
    sms_capable_phone: str = None
    
    def save(self):
        new_person = Person.create_new(self.first_name, self.last_name)
        new_phone = Phone.create_new(self.sms_capable_phone)
        new_account = System_Account.create_new(self.username, str(self.username+self.company_association), password=self.password)
        new_person.phone_numbers.add(new_phone)
        new_person.system_accounts.add(new_account)
        db.repo.save(new_person)