from django.urls import path
from . import views


#ulrConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('create/', views.create),
    path('list/', views.show_list),
    path('listStarted/', views.show_started_list),
    path('listOpen/', views.show_open_list),
    path('listFinished/', views.show_finished_list),
    path('listMyCreated/', views.show_created_list),
    path('listMyRegistered/', views.show_registered_list),
    path('view/<int:selected_tournament_id>/', views.tournament_page),
    path('edit/<int:selected_tournament_id>/', views.edit_tournament),
    path('delete/<int:tournament_id>/', views.delete_tournament),
    path('add_attendant/<int:tournament_id>/', views.add_attendant),
    path('match/view/<int:match_id>/', views.match_page),
    path('match/setScore/<int:match_id>/', views.match_add_score),
]
