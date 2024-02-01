import datetime
import operator
import math
from functools import reduce

from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from .forms import AddTournamentForm, AddAttendantForm, AddMatchScore, AddFilters
from .models import Tournament, UserToTournament, Match
from user.models import UserUser
# Create your views here.


def say_hello(request):
    return HttpResponse('hello from tournament')


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddTournamentForm(request.POST)
            form.creator = UserUser.objects.get(pk=request.user.id)

            if form.is_valid():
                new_tournament = Tournament.objects.create(
                    creator=UserUser.objects.get(pk=request.user.id),
                    name=form.cleaned_data["name"],
                    start_date=form.cleaned_data["start_date"],
                    max_attendants=form.cleaned_data["max_attendants"],
                )
                new_tournament.save()
                return redirect('/tournament/list/')
            else:
                return HttpResponse(form.data)
        else:
            form = AddTournamentForm()

        return render(request, "create.html", {'form': form})
    else:
        return redirect('/user/login')


def edit_tournament(request, selected_tournament_id):
    if request.user.is_authenticated:
        editing_tournament = Tournament.objects.filter(id__exact=selected_tournament_id)[0]
        if request.method == "POST":
            form = AddTournamentForm(request.POST)
            if form.is_valid():
                editing_tournament.name = form.cleaned_data["name"]
                editing_tournament.start_date = form.cleaned_data["start_date"]
                editing_tournament.max_attendants = form.cleaned_data["max_attendants"]
                editing_tournament.save()
                return redirect('/tournament/view/'+str(selected_tournament_id))
            else:
                return HttpResponse(form.data)
        else:
            form = AddTournamentForm(initial={'name': editing_tournament.name,
                                              'start_date': editing_tournament.start_date,
                                              'max_attendants': editing_tournament.max_attendants})

        return render(request, "edit.html", {'form': form})
    else:
        return redirect('/user/login')


def show_list(request):
    if not request.user.is_authenticated:
        tournaments = Tournament.objects.filter(ladder_created=True)
        return render(request, "list.html", {'tournaments': tournaments})
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters))
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournaments = Tournament.objects.all()

    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def show_started_list(request):
    if not request.user.is_authenticated:
        return redirect('/tournament/list')
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters),
                                                            ladder_created__exact=True, is_finished__exact=False)
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournaments = Tournament.objects.filter(ladder_created__exact=True, is_finished__exact=False)
    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def show_finished_list(request):
    if not request.user.is_authenticated:
        return redirect('/tournament/list')
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters),
                                                            is_finished__exact=True)
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournaments = Tournament.objects.filter(is_finished__exact=True)
    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def show_open_list(request):
    if not request.user.is_authenticated:
        return redirect('/tournament/list')
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters),
                                                            ladder_created=False)
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournaments = Tournament.objects.filter(ladder_created=False)
    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def show_created_list(request):
    if not request.user.is_authenticated:
        return redirect('/tournament/list')
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters),
                                                            creator_id__exact=request.user.id)
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournaments = Tournament.objects.filter(creator_id__exact=request.user.id)
    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def show_registered_list(request):
    if not request.user.is_authenticated:
        return redirect('/tournament/list')
    else:

        if request.method == "POST":
            form = AddFilters(request.POST)
            if form.is_valid():
                date_filters = []
                if form.cleaned_data["date_start"]:
                    date_filters.append(Q(start_date__gte=form.cleaned_data["date_start"]))
                if form.cleaned_data["date_end"]:
                    date_filters.append(Q(start_date__lte=form.cleaned_data["date_end"]))
                if date_filters:
                    tournament_ids = UserToTournament.objects.filter(
                        user_id__exact=request.user.id).values('tournament_id')
                    tournaments = Tournament.objects.filter(reduce(operator.and_, date_filters),
                                                            id__in=tournament_ids)
                else:
                    tournaments = Tournament.objects.all()
                return render(request, "list.html", {'tournaments': tournaments, 'form': form})
            else:
                return HttpResponse(form.data)
        else:
            form = AddFilters()
            tournament_ids = UserToTournament.objects.filter(user_id__exact=request.user.id).values('tournament_id')
            tournaments = Tournament.objects.filter(id__in=tournament_ids)
    if tournaments.count() > 0:
        return render(request, "list.html", {'tournaments': tournaments, 'form': form})
    else:
        return render(request, "list_empty.html")


def tournament_page(request, selected_tournament_id):
    try:
        users_in_tournament = UserToTournament.objects.filter(tournament_id__exact=selected_tournament_id)
    except UserToTournament.DoesNotExist:
        users_in_tournament = None
    if users_in_tournament is not None:
        current_count = users_in_tournament.count()
    else:
        current_count = 0
    round_count = int(math.log(Tournament.objects.filter(id__exact=selected_tournament_id)[0].max_attendants, 2))
    matches = []
    for x in range(1, round_count+1):
        matches.append(Match.objects.filter(tournament_id__exact=selected_tournament_id, round__exact=x))
    return render(request, "tournament_view.html", {
        'tournament': Tournament.objects.get(id=selected_tournament_id),
        'current_attendants': current_count,
        'users_in_tournament': users_in_tournament,
        'matches': matches
        })


def delete_tournament(request, tournament_id):
    Tournament.objects.get(id=tournament_id).delete()
    return redirect('/tournament/list/')


def add_attendant(request, tournament_id):
    if request.method == "POST":
        form = AddAttendantForm(request.POST, tournament_id=tournament_id)

        if form.is_valid():
            new_attendant = UserToTournament.objects.create(
                user=UserUser.objects.get(pk=form.cleaned_data["user_id"]),
                tournament=Tournament.objects.get(pk=tournament_id),
            )
            new_attendant.save()
            return redirect('/tournament/view/'+str(tournament_id))
        else:
            return HttpResponse(form.data)
    else:
        form = AddAttendantForm(tournament_id=tournament_id)

    return render(request, "add_attendant.html",  {'form': form})


def match_page(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'match_view.html', {'match': match})


def match_add_score(request, match_id):
    if request.method == "POST":
        form = AddMatchScore(request.POST)

        if form.is_valid():
            match = Match.objects.get(pk=match_id)
            match.score = str(form.cleaned_data["score_player_one"]) + ':' + str(form.cleaned_data["score_player_two"])
            if form.cleaned_data["score_player_one"] > form.cleaned_data["score_player_two"]:
                match.winner = UserUser.objects.get(pk=match.player_one_id)
            elif form.cleaned_data["score_player_one"] == form.cleaned_data["score_player_two"]:
                ...
            else:
                match.winner = UserUser.objects.get(pk=match.player_two_id)
            match.save()
            current_round = match.round
            tournament_id = match.tournament_id
            new_tournament_match_id = Match.objects.filter(round__exact=current_round,
                                                           tournament_id__exact=tournament_id
                                                           ).order_by("-tournament_match_id")[0].tournament_match_id
            new_tournament_match_id = new_tournament_match_id + 1 + math.floor(
                (match.tournament_match_id - Match.objects.filter(round__exact=current_round,
                                                                  tournament_id__exact=tournament_id
                                                                  ).order_by("tournament_match_id")[0]
                                                                   .tournament_match_id)
                /2
            )
            if match.round == int(math.log(match.tournament.max_attendants, 2)):
                match.tournament.winner_id = match.winner_id
                match.tournament.is_finished = True
                match.tournament.save()
            elif Match.objects.filter(
                    tournament_match_id__exact=new_tournament_match_id, tournament_id=tournament_id).count() > 0:
                existing_match = Match.objects.filter(
                    tournament_match_id__exact=new_tournament_match_id, tournament_id=tournament_id)[0]
                if existing_match.player_one_id is None and match.tournament_match_id % 2 == 0:
                    existing_match.player_one_id = match.winner_id
                elif existing_match.player_two_id is None and match.tournament_match_id % 2 != 0:
                    existing_match.player_two_id = match.winner_id
                existing_match.save()
            else:
                new_match = Match.objects.create(
                    score=None,
                    player_one_id=match.winner_id if match.tournament_match_id % 2 == 0 else None,
                    player_two_id=match.winner_id if match.tournament_match_id % 2 != 0 else None,
                    tournament_id=match.tournament_id,
                    round=current_round+1,
                    tournament_match_id=new_tournament_match_id
                )
                new_match.save()
            return redirect('/tournament/match/view/'+str(match_id))
        else:
            return HttpResponse(form.data)
    else:
        form = AddMatchScore()

    return render(request, "add_match_score.html",  {'form': form})
