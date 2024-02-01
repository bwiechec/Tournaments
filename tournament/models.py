from django.db import models
from user.models import UserUser

# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('date start')
    max_attendants = models.IntegerField()
    creator = models.ForeignKey(UserUser, on_delete=models.CASCADE, related_name='creator', default='')
    is_finished = models.BooleanField(default=False)
    ladder_created = models.BooleanField(default=False)
    winner = models.ForeignKey(UserUser, on_delete=models.CASCADE, related_name='winner', default='', null=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    score = models.CharField(max_length=10, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default='')
    player_one = models.ForeignKey(UserUser, on_delete=models.CASCADE, related_name='player_one', default='', null=True)
    player_two = models.ForeignKey(UserUser, on_delete=models.CASCADE, related_name='player_two', default='', null=True)
    round = models.IntegerField(default=0)
    tournament_match_id = models.IntegerField(default=0)
    winner = models.ForeignKey(UserUser, on_delete=models.CASCADE, related_name='match_winner', default='', null=True)


class UserToTournament(models.Model):
    user = models.ForeignKey(UserUser, on_delete=models.CASCADE, default='')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default='')

    def __str__(self):
        return str(self.user, self.tournament)
