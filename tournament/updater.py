import datetime
import random
import time
import math
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Tournament, UserToTournament, Match

random.seed(time.process_time())


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_ladder, 'interval', minutes=1)
    scheduler.start()


def create_ladder():
    if Tournament.objects.all().count() > 0:
        date = str(datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M'))+\
               '+00:00'
        for single_tournament in Tournament.objects.all():
            if str(single_tournament.start_date) == str(date) and not single_tournament.ladder_created:
                registered_users = UserToTournament.objects.filter(tournament_id__exact=single_tournament.id)
                print(registered_users.count())
                if registered_users.count() == 0:
                    single_tournament.is_finished = True
                    single_tournament.ladder_created = True
                    single_tournament.save()
                elif registered_users.count() == 1:
                    single_tournament.winner_id = registered_users[0].user_id
                    single_tournament.is_finished = True
                    single_tournament.ladder_created = True
                    single_tournament.save()
                else:
                    if math.ceil(math.log(registered_users.count(), 2)) < math.log(single_tournament.max_attendants, 2):
                        single_tournament.max_attendants = int(math.pow(2, math.ceil(math.log(registered_users.count(), 2))))
                    print(single_tournament.max_attendants)
                    attendants = [None] * single_tournament.max_attendants
                    for user in registered_users:
                        x = random.randint(0, single_tournament.max_attendants - 1)
                        while attendants[x] is not None:
                            x = random.randint(0, single_tournament.max_attendants)
                        attendants[x] = user.user_id
                    for i in range(0, len(attendants) - 1, 2):
                        new_match = Match.objects.create(
                            score=None,
                            player_one_id=attendants[i],
                            player_two_id=attendants[i + 1],
                            tournament_id=single_tournament.id,
                            round=1,
                            tournament_match_id=i / 2
                        )
                        new_match.save()
                    for j in range(2, int(math.log(single_tournament.max_attendants, 2))+1):
                        for i in range(int(single_tournament.max_attendants/pow(2, j))):
                            new_tournament_match_id = Match.objects.filter(round__exact=j-1,
                                                                           tournament_id__exact=single_tournament.id
                                                                           ).order_by("-tournament_match_id")[
                                0].tournament_match_id
                            new_tournament_match_id = new_tournament_match_id + 1 + i
                            new_match = Match.objects.create(
                                score=None,
                                player_one_id=None,
                                player_two_id=None,
                                tournament_id=single_tournament.id,
                                round=j,
                                tournament_match_id=new_tournament_match_id
                            )
                            new_match.save()
                    single_tournament.ladder_created = True
                    single_tournament.save()
