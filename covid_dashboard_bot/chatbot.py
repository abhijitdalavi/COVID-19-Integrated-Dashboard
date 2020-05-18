from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller

class ChatBot:


    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.spell = Speller(lang='en')
        self.store_synonyms()
        self.reset_flags()
        return None


    def preprocess_input(self, input_string):
        input_string = self.spell(input_string)
        input_string = input_string.lower()
        tokens = word_tokenize(input_string)
        input_string_tokens = [self.lemmatizer.lemmatize(word, 'v') for word in tokens]
        if 'jello' in input_string_tokens:
            input_string_tokens.remove('jello')
            input_string_tokens.append('hello')
        return input_string_tokens


    def give_synonyms(self, *words):
        word_set = set()
        for word in words:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    word_set.add(l.name())
        return word_set


    def store_synonyms(self):
        self.greeting_words = self.give_synonyms('hello', 'hi', 'greetings')
        self.symptom_words = self.give_synonyms('tell', 'check', 'test', 'symptom', 'know', 'sign')
        self.mortality_words = self.give_synonyms('mortality', 'death', 'rate')
        self.spread_words = self.give_synonyms('number', 'case', 'spread', 'zone', 'area')
        self.general_prevention_words = self.give_synonyms('precaution', 'precautions', 'prevent', 'safe', 'safety', 'measure')
        self.immediate_prevention_words = self.give_synonyms('diagnose', 'diagnosis', 'has', 'catch', 'get')
        self.helpline_words = self.give_synonyms('help', 'helpline', 'contact')
        self.helpline_words.add('helpline')
        self.incubation_words = self.give_synonyms('incubation', 'period', 'duration', 'incubate', 'time')
        self.website_words = self.give_synonyms('website', 'site', 'page', 'webpage')
        self.forum_words = self.give_synonyms('forum')
        self.dashboard_words = self.give_synonyms('dashboard', 'graph', 'chart', 'visualization')
        self.chatbot_words = self.give_synonyms('chat', 'bot', 'chatbot')
        return None


    def reset_flags(self):
        self.flags = {
            'greetings': False,
            'symptoms': False,
            'immediate_prevention': False,
            'general_prevention': False,
            'mortality': False,
            'spread': False,
            'helpline': False,
            'incubation': False,
            'website': False,
            'forum': False,
            'dashboard': False,
            'chatbot': False,
        }
        return None


    def set_flags(self, preprocessed_tokens):
        for word in preprocessed_tokens:
            if word in self.symptom_words:
                self.flags['symptoms'] = True
            elif word in self.immediate_prevention_words:
                self.flags['immediate_prevention'] = True
            elif word in self.general_prevention_words:
                self.flags['general_prevention'] = True
            elif word in self.mortality_words:
                self.flags['mortality'] = True
            elif word in self.helpline_words:
                self.flags['helpline'] = True
            elif word in self.incubation_words:
                self.flags['incubation'] = True
            elif word in self.spread_words:
                self.flags['spread'] = True
            elif word in self.website_words:
                self.flags['website'] = True
            elif word in self.forum_words:
                self.flags['forum'] = True
            elif word in self.dashboard_words:
                self.flags['dashboard'] = True
            elif word in self.chatbot_words:
                self.flags['chatbot'] = True
            elif word in self.greeting_words:
                self.flags['greetings'] = True
        return None


    def give_reply(self):
        if self.flags['symptoms']:
            reply_string = "".join(["Most common symptoms:\n",
                            "fever, dry cough, tiredness\n\n",
                            "Less common symptoms:\n",
                            "aches and pains, sore throat, diarrhoea, conjunctivitis, headache, loss of taste or smell, a rash on skin, or discolouration of fingers or toes\n\n",
                            "Serious symptoms:\n",
                            "difficulty breathing or shortness of breath",
                            "chest pain or pressure",
                            "loss of speech or movement\n\n\n",
                            "If you or someone you know shows these symptoms,\nplease use the following helpline:\n011-23978046\nor\n1075\nor send an email to:\nncov2019@gov.in"])
        elif self.flags['immediate_prevention']:
            reply_string = "".join(["Stay home unless it is absolutely necessary to go out\n\n",
                            "Wash your hands frequently\n\n",
                            "Do not touch your eyes, nose or mouth\n\n",
                            "Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze\n\n",
                            "Maintain a safe distance from people",
                            "If you have a fever, cough and difficulty breathing, seek medical attention. Call in advance.\n\n",
                            "Follow the directions of your local health authority"])
        elif self.flags['general_prevention']:
            reply_string = "".join(["Stay Home\n\n",
                            "Keep a safe distance\n\n",
                            "Wash your hands often\n\n",
                            "Cover your cough/sneeze\n\n",
                            "If you are sick, call the helpline"])
        elif self.flags['mortality']:
            reply_string = "Mortality Rate is not a good measure of the severity of a disease, since it changes with communities. Even a relatively low mortality rate is disastrous in large numbers. So please take all necessary precautions!"
        elif self.flags['helpline']:
            reply_string = "Helpline numbers:\n011-23978046\nor\n1075\n\nE-mail:\nncov2019@gov.in"
        elif self.flags['incubation']:
            reply_string = "On average it takes 5–6 days from when someone is infected with the virus for symptoms to show, however it can take up to 14 days."
        elif self.flags['spread']:
            reply_string = "Please refer to the Dashboard for information on the spread of the disease"
        elif self.flags['website']:
            reply_string = "The website contains three distinct sections:\nA Dashboard for information on spread,\nA Forum for discussions,\n and this Chatbot"
        elif self.flags['forum']:
            reply_string = "The Forum allows you to connect to other people to seek or provide help, or for general discussions. There is also provision to reach out to government officials."
        elif self.flags['dashboard']:
            reply_string = "The Dashboard shows visualizations of the spread of the disease (the number of cases)"
        elif self.flags['chatbot']:
            reply_string = "This chatbot can be used for queries related to:\n-> The Website\n-> The Dashboard\n-> The Forum\n-> COVID-19"
        elif self.flags['greetings']:
            reply_string = "Hello, Feel free to ask me any Website or COVID-19 related queries!"
        else:
            reply_string = "Sorry, I do not have a reply for that..."

        self.reset_flags()
        return reply_string


    def reply(self, input_string):
        preprocessed_tokens = self.preprocess_input(input_string)
        self.set_flags(preprocessed_tokens)
        return self.give_reply()




if __name__ == "__main__":

    ChatBot()
