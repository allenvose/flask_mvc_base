

from py2neo.ogm import Model
from py2neo.ogm import  Node, Label,  Property, Related, RelatedTo, RelatedFrom

from app import db

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
