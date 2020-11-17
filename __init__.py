import json
import googlemaps
import pprint
import time
from os.path import dirname, join

from mycroft import MycroftSkill, intent_file_handler
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)

class GoogleMapsClient(object):
    
    def __init__(self, api_key=None):
        self.gmaps = googlemaps.Client(key=api_key)
        LOGGER.debug("Connected to Google API: %s" % self.gmaps)
        
    def places(self, **places_ag):
        LOGGER.debug('Google API - Places')
        if places_ag['location'].isnumeric() is False:
            geo_response = self.gmaps.geocode(places_ag['location'])[0]
            LOGGER.debug("API Response: %s" % json.dumps(geo_response))
            src_crd = geo_response["geometry"]["location"]
            places_ag['location'] = "%s,%s" % (src_crd['lat'],
                                                 src_crd['lng'])
        LOGGER.debug('API Ag: %s' % places_ag)
        response = self.gmaps.places(**places_ag)
        results = response['results']
        clst_result = results[0]
        LOGGER.debug("Closest Result: %s" % json.dumps(clst_result))
        location = clst_result['geometry']['location']
        geo_loc = "%s, %s" % (location['lat'], location['lng'])
        geo_place_id = "place_id:%s" % closest_result['place_id']
        return geo_place_id
    
     def places_nearby(self, **places_nearby_ag):
        LOGGER.debug('Google API - Places Nearby')
        response = self.gmaps.places_nearby(**places_nearby_ag)
        LOGGER.debug("API Response: %s" % json.dumps(response))
        results = response['results']
        result = results[0]
        location = result['geometry']['location']
        geo_loc = [location['lat'], location['lng']]
        return geo_loc

class Poi(MycroftSkill):
    def __init__(self):
         super(Poi, self).__init__("Poi")
      #  MycroftSkill.__init__(self)
         provider = self.config.get('provider', 'google')
         LOGGER.debug("Configured Provider: %s" % provider
         if provider == 'google':
            api_key = self.config.get('api_key', None)
            self.maps = GoogleMapsClient(api_key)
            LOGGER.debug("Connected to Google API: %s" % self.maps)
         

     def initialize(self):
             poi_intent = IntentBuilder("PoiIntent").require("PoiKeyword").build()
             self.register_intent(poi_intent, self.handle_poi_intent)
            
    @intent_file_handler('poi.intent')
    def poi_intent(self, message):
        try:
        start = message.data.get('whatIsTheStartingPoint')
        end = message.data.get('whereIsTheDestination')
        self.speak_dialog("welcome",
                          data={'destination': end,
                                'origin': start})
        except Exception as err:
            LOGGER.error("Error: {0}".format(err))
        
      
    def request_places(self, message):
        
        self.speak_dialog("welcome",
                          data={'destination': itinerary['dest_name'],
                                'origin': itinerary['origin_name']})
        # Places Nearby API
        places_nearby_args = {
            'name': itinerary['destination'],
            'location': itinerary['origin']
            }
        if "OpenNowKeyword" in message.data:
            places_nearby_args['open_now'] = True
        # nearby_places = self.maps.places_nearby(**places_nearby_args)
        # Places API
        places_args = {
            'query': itinerary['destination'],
            'location': itinerary['origin']
            }
        if "OpenNowKeyword" in message.data:
            places_args['open_now'] = True
        places = self.maps.places(**places_args)
        LOGGER.debug("Places Module Result: %s" % places)
        itinerary['destination'] = places
        dist_args = {
            'origins': itinerary['origin'],
            'destinations': itinerary['destination'],
            'mode': 'driving',
            'units': self.dist_units
            }
        drive_details = self.maps.distance(**dist_args)
        duration_norm = drive_details[0]
        duration_traffic = drive_details[1]
        traffic_time = drive_details[2]


def create_skill():
    return Poi()

