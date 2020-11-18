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
        self.speak_dialog("welcome")
        latlong = message.data.get(places_nearby['geo_loc'])
        api_root = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        api_params = '?location=' + latlong +\
                     '&radius=' + 1500 +\
                     '&type=best_guess' +\
                     '&key=' + api_key
        api_url = api_root + api_params
        LOGGER.debug("API Request: %s" % api_url)
        response = requests.get(api_url)
                      
        if response.status_code == requests.codes.ok and \
                response.json()['status'] == "REQUEST_DENIED":
           LOGGER.error(response.json())
           self.speak_dialog('places.error.api')
                      
        
        elif response.status_code == requests.codes.ok:
            LOGGER.debug("API Response: %s" % response)

        places_nearby_ag = {
            'name': poi_intent['end'],
            'location': poi_intent['start']
            }
        if "OpenNowKeyword" in message.data:
            places_nearby_ag['open_now'] = True
        places_ag = {
            'query': poi_intent['end'],
            'location': poi_intent['start']
            }
        if "OpenNowKeyword" in message.data:
            places_ag['open_now'] = True
        places = self.maps.places(**places_ag)
        LOGGER.debug("Places Module Result: %s" % places)
        poi_intent['end'] = places
        self.speak_dialog("The places are", data={"places":places})

        def stop(self):
        pass
                      
def create_skill():
    return Poi()

