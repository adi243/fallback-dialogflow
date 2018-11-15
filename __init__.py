
from mycroft.skills.core import FallbackSkill


import uuid
import os
import dialogflow_v2 as dialogflow

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'MyRobo-b0081c95313a.json'

class DialogFallback(FallbackSkill):
    """
        A Fallback skill to access the Dialogflow api for specific scripted questions.
    """
    def __init__(self):
        super(DialogFallback, self).__init__(name='Dialog Fallback')

    def initialize(self):
        """
            Registers the fallback skill, in this case I'll connect to dialogflow for a possible response.
        """
        self.register_fallback(self.check_dialogflow, 10)
        # Any other initialize code goes here

    def check_dialogflow(self, message):
        """
            Ask DialogFlow if there is a matching intent.
        """
        project_id = 'myrobo-5b4b5'

        session_id = str(uuid.uuid4())

        language_code = 'en-US'

        texts = message.data.get("utterance")

	
        session_client = dialogflow.SessionsClient()


        session = session_client.session_path(project_id, session_id)

        print('Session path: {}\n'.format(session)) ## To be commented out after testing, To check for api connection

        #for text in texts:
        text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)

        reply = response.query_result.fulfillment_text


        if reply == '':	

           return False

        else:

           self.speak_dialog(reply)

           return True
		     

    def shutdown(self):
        """
            Remove this skill from list of fallback skills.
        """
        self.remove_fallback(self.check_dialogflow)
        super(DialogFallback, self).shutdown()


def create_skill():
    return DialogFallback()
