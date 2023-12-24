import json
from channels.generic.websocket import AsyncWebsocketConsumer
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class ChatRoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_mapping = {
            'NN': 'Noun', 'PRP$': 'Possessive', 'VBZ': 'Verb', 'JJ': 'Adjective', 'RB': 'Adverb', 'VBD': 'Verb', 'VBG': 'Verb', 'VBN': 'Verb', 'IN': 'Preposition', 'DT': 'Determiner', 'CC': 'Conjunction', 'MD': 'Modal', 'UH': 'Interjection', 'WP': 'Wh-pronoun', 'WDT': 'Wh-determiner', 'WRB': 'Wh-adverb', 'CD': 'Number', 'PRP': 'Personal Pronoun', 'VBP': 'Verb', 'NNP': 'Proper Noun',
        }
        self.last_message = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user.login',
                'username': self.scope['user'].username,
            }
        )

        await self.accept()

    async def disconnect(self, close_codes):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def calculate_figures_of_speech(self, message):
        words = word_tokenize(message)
        #print(words)
        tagged_words = pos_tag(words)
        #print(tagged_words)
        figures_of_speech = {}

        for word, tag in tagged_words:
            full_name = self.pos_mapping.get(tag, tag)
            figures_of_speech.setdefault(full_name, []).append(word)

        return figures_of_speech

    async def send_figures_of_speech(self, username, figures_of_speech):
        formatted_figures = json.dumps(figures_of_speech, indent=2)

        await self.send(text_data=json.dumps({
            'message': f"Figures of Speech analysis:\n{formatted_figures}",
            'username': 'System',
            'analysisResult': True, 
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        if message.startswith("!figures_of_speech"):
            if self.last_message is not None:
                figures_of_speech = self.calculate_figures_of_speech(self.last_message)
                await self.send_figures_of_speech(username, figures_of_speech)
        else:
            self.last_message = message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',
                    'message': message,
                    'username': username,
                }
            )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def user_login(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': 'someone has joined the chat.',
            'username': 'System',
        }))
