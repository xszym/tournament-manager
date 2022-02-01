import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Match

from .helpers import slug_to_uuid, uuid_to_slug


class ScoreUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.match_slug = self.scope['url_route']['kwargs']['match_slug']
        self.user = self.scope["user"]
        self.match = Match.objects.get(id=self.match_slug)

        self.room_group_name = self.match_slug
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.match.tournament.referee_list.filter(pk=self.user.pk).count() == 0:
            self.close()
        else:
            self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        teamA_score = text_data_json.get('teamA_score', None)
        teamB_score = text_data_json.get('teamB_score', None)

        if teamA_score:
            self.match.team_A_score = teamA_score
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'teamA_score': teamA_score
                }
            )

        if teamB_score:
            self.match.team_B_score = teamB_score
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'teamB_score': teamB_score
                }
            )
        self.match.save()

    def chat_message(self, event):
        teamA_score = event.get('teamA_score', None)
        teamB_score = event.get('teamB_score', None)

        if teamA_score:
            self.send(text_data=json.dumps({
                'teamA_score': teamA_score
            }))
        if teamB_score:
            self.send(text_data=json.dumps({
                'teamB_score': teamB_score
            }))
