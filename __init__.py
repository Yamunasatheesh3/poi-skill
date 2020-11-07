import json
import googlemaps
import pprint
import time


from mycroft import MycroftSkill, intent_file_handler
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger


class Poi(MycroftSkill):
    def __init__(self):
         super(Poi, self).__init__(name="Poi")
      #  MycroftSkill.__init__(self)

     def initialize(self):
             poi_intent = IntentBuilder("PoiIntent").require("PoiKeyword").build()
             self.register_intent(poi_intent, self.handle_poi_intent)
            
    @intent_file_handler('poi.intent')
    def handle_poi(self, message):
        api_key = 'AIzaSyBp25k9LqhGDh4nAIHeFnhu045jrWPnWkg'
        gmaps = googlemaps.Client(key = api_key)
        places_result = gmaps.places_nearby(location= '45.421532,-75.697189', radius = 10000, open_now = False, type = 'gas_station')
        
        for place in places_result['results']:
           my_place_id = place['place_id']
           my_fields = ['name', 'formatted_phone_number', 'type', 'formatted_address']
           place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
        self.speak_dialog('place_details')


def create_skill():
    return Poi()

