from django.conf.urls import url
from django.contrib import admin
from Site import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^schools/(?P<school>[-\w]+)', views.school_page, name='school_page'),
    url(r'^players/(?P<player_id>[-\w]+)', views.player_page, name='player_page'),
    url(r'^conferences/(?P<conference>[-\w]+)', views.conference_page, name='conference_page'),
    url(r'^admin/', admin.site.urls),
]
