# -*- coding: utf-8 -*-

import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


class Guestbook(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    
    @staticmethod
    def get_guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
        return ndb.Key('Guestbook', guestbook_name)
        
    @classmethod
    def get_guestbook_by_name(cls, guestbook_name):
        return cls.query(Guestbook.name == guestbook_name).get()
    
    @classmethod
    def check_is_exist(cls, guestbook_name):
        if cls.get_guestbook_by_name(guestbook_name) is None:
            return False
        return True
    
    @classmethod
    def add_new_book(cls, guestbook_name):
        guestbook = cls()
        guestbook.name = guestbook_name
        guestbook.put()
        return guestbook


class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def get_greetings(cls, guestbook_name, count):
        greetings = cls.query(ancestor=Guestbook.get_guestbook_key(guestbook_name))\
            .order(-cls.date).fetch(count)
        return greetings
    
    @classmethod
    def get_all_greetings(cls, count):
        greetings = cls.query().order(-cls.date).fetch(count)
        return greetings
    
    @classmethod
    def get_greeting(cls, guestbook_name, greeting_id):
        greeting = cls.query(cls.key == ndb.Key("Guestbook", str(guestbook_name),
                                                "Greeting", int(greeting_id))).get()
        return greeting
    
    @classmethod
    def update_greeting(cls, dictionary):
        greeting = cls.get_greeting(dictionary["guestbook_name"], dictionary["greeting_id"])
        if greeting:
            greeting.content = dictionary["content"]
            greeting.updated_date = datetime.datetime.now()
            greeting.put()
        
        return greeting
    
    @classmethod
    def delete_greeting(cls, dictionary):
        key = ndb.Key(
            "Guestbook", dictionary["guestbook_name"],
            "Greeting", int(dictionary["greeting_id"]))
        greeting = key.get()
        greeting.key.delete()
    
    @classmethod
    def put_from_dict(cls, dictionary):
        guestbook_name = dictionary["guestbook_name"]
        
        if Guestbook.check_is_exist(guestbook_name) is False:
            Guestbook.add_new_book(guestbook_name)
        
        greeting = cls(parent=Guestbook.get_guestbook_key(guestbook_name))
        
        if users.get_current_user():
            greeting.author = users.get_current_user()
            
        greeting.content = dictionary["content"]
        greeting.put()
        
        return greeting