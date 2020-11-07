from mycroft import MycroftSkill, intent_file_handler


class Poi(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('poi.intent')
    def handle_poi(self, message):
        self.speak_dialog('poi')


def create_skill():
    return Poi()

