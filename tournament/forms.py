from .models import Tournament, UserToTournament
from django import forms
from django.forms import DateTimeInput, ChoiceField, Select, DateTimeField, ModelChoiceField, IntegerField
from user.models import UserUser
from django.core.validators import MaxValueValidator, MinValueValidator


class AddTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        widgets = {'start_date': DateTimeInput(
                    format=('%Y-%m-%d %H:%M'),
                    attrs={'class': 'form-control',
                           'placeholder': 'Select a date',
                           'type': 'datetime-local'}),
                    'max_attendants': Select(
                        choices=(('4', '4'),
                                 ('8', '8'),
                                 ('16', '16'),
                                 ('32', '32'),
                                 )
                    )}
        exclude = ("creator", "is_finished", "ladder_created", "winner")


class AddAttendantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.tournament_id = kwargs.pop('tournament_id')

        super(AddAttendantForm, self).__init__(*args,**kwargs)

        self.in_tournament = UserToTournament.objects.filter(tournament_id__exact=self.tournament_id)\
            .values_list('user_id')
        #print(self.in_tournament)
        self.CHOICES = UserUser.objects.exclude(id__in=self.in_tournament).values_list('id', 'username')
        #print(self.CHOICES)
        users = ()
        for x in range(len(self.CHOICES)):
            users = users + ((str(self.CHOICES[x][0]), str(self.CHOICES[x][1])),)
        self.fields['user_id'] = ChoiceField(choices=users)

    class Meta:
        model = UserToTournament
        fields = "__all__"
        #fields = ['user_id', 'tournament_id']
        exclude = ('user', 'tournament')


class AddMatchScore(forms.Form):
    score_player_one = IntegerField()
    score_player_two = IntegerField()


class AddFilters(forms.Form):
    date_start = forms.DateTimeField(input_formats='%Y-%m-%d', required=False)
    date_end = forms.DateTimeField(input_formats='%Y-%m-%d', required=False)
