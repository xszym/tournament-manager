import datetime
from enum import Enum
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .helpers import uuid_to_slug


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    img_path = models.CharField('img_path', max_length=100, unique=False, default='tournament/images/base.jpeg')

    def __str__(self):
        return '%s' % (self.name)


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=50)
    team_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_manager')
    members = models.ManyToManyField(User, related_name='members', blank=True)

    @property
    def url(self):
        slug = uuid_to_slug(self.id)
        return reverse('team_details', kwargs={'slug':slug})
    
    @property
    def slug(self):
        return

    @property
    def join_url(self):
        slug = uuid_to_slug(self.id)
        return reverse('join_team_request', kwargs={'slug':slug})

    def __str__(self):
        return '%s' % (self.name)


class EliminationType(Enum):
    KNOCKOUT = "KNOCKOUT"
    GROUP = "GROUP"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True, default="")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    team_list = models.ManyToManyField(Team, blank=True)
    type_of_elimination = models.CharField(max_length=50, choices=EliminationType.choices())
    created = models.DateTimeField(auto_now_add=True)
    referee_list = models.ManyToManyField(User, related_name='referee_list', blank=True)

    @property
    def has_matches(self):
        matches = list(Match.objects.filter(tournament=self))
        return len(matches) > 0

    @property
    def url(self):
        return reverse('tournament_details', kwargs={'slug':self.slug})

    @property
    def slug(self):
        return uuid_to_slug(self.id)

    def __str__(self):
        return '%s %s' % (self.start_date, self.name)


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match_number = models.IntegerField(null=False)
    team_A = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='teamA')
    team_B = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='teamB')
    team_A_score = models.IntegerField(default=0)
    team_B_score = models.IntegerField(default=0)
    winner_team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='winner_team')
    is_end = models.BooleanField(default=False)

    @property
    def url(self):
        return reverse('match_details', kwargs={'slug':self.slug})

    @property
    def slug(self):
        return uuid_to_slug(self.id)

    @property
    def are_two_teams(self):
        return self.team_A and self.team_B
        
        
    def __str__(self):
        return '%s | Match %d | %s (%d) vs %s (%d)' % (self.tournament.name, self.match_number, self.team_A, self.team_A_score, self.team_B, self.team_B_score)


class JoinRequestStatusType(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TeamTournamentRequest(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=JoinRequestStatusType.choices(), default=JoinRequestStatusType.PENDING.value)

    class Meta:
        unique_together = [("tournament", "team")]

    def __str__(self):
        return '%s - %s (%s)' % (self.tournament.name, self.team.name, self.status)


class TeamJoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=JoinRequestStatusType.choices(
    ), default=JoinRequestStatusType.PENDING.value)

    class Meta:
        unique_together = [("team", "user")]

    @property
    def accept_url(self):
        kwargs = {
            'request_id': self.id,
            'new_status': JoinRequestStatusType.ACCEPTED.value
        }
        return reverse('change_join_team_request_status', kwargs=kwargs)

    @property
    def reject_url(self):
        kwargs = {
            'request_id': self.id,
            'new_status': JoinRequestStatusType.REJECTED.value
        }
        return reverse('change_join_team_request_status', kwargs=kwargs)

    def is_accepted(self):
        return self.status == JoinRequestStatusType.ACCEPTED.value

    def is_pending(self):
        return self.status == JoinRequestStatusType.PENDING.value

    def is_rejected(self):
        return self.status == JoinRequestStatusType.REJECTED.value

    def __str__(self):
        return '%s - %s (%s)' % (self.team.name, self.user.username, self.status)
