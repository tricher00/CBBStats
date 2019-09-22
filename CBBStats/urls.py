from django.conf.urls import url
from django.urls import path
from django.urls import re_path
from django.contrib import admin
from api import views
from api.views import player
from api.views import school
from api.views import gameLine
from api.views import conference
from website.views import index

urlpatterns = [
    re_path(r'^api/players/(?P<player_id>[-\w]+)', player, name="player"),
    re_path(r'^api/schools/(?P<school_id>[-\w]+)', school, name="school"),
    re_path(r'^api/gameLines/(?P<game_line_id>[-\w]+)', gameLine, name="gameLine"),
    re_path(r'^api/conferences/(?P<conference>[-\w]+)', conference, name="conference"),
    path("", index, name="index"),
    #url(r'^$', views.home, name='home'),
    #url(r'^schools/(?P<school>[-\w]+)', views.school_page, name='school_page'),
    #url(r'^players/(?P<player_id>[-\w]+)', views.player_page, name='player_page'),
    #url(r'^conferences/(?P<conference>[-\w]+)', views.conference_page, name='conference_page'),
    url(r'^admin/', admin.site.urls),
]
