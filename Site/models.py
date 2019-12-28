from __future__ import unicode_literals

from django.db import models

class Conference(models.Model):
    abbrv = models.TextField(unique=True, primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference'

class Game(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    date = models.DateField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    conf_game = models.IntegerField(blank=True, null=True)
    home_id = models.TextField(blank=True, null=True)
    away_id = models.TextField(blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'

class GameLine(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    game_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    player_id = models.TextField(blank=True, null=True)
    team_id = models.TextField(blank=True, null=True)
    opponent_id = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    fg_made = models.IntegerField(blank=True, null=True)
    fg_attempt = models.IntegerField(blank=True, null=True)
    two_made = models.IntegerField(blank=True, null=True)
    two_attempt = models.IntegerField(blank=True, null=True)
    three_made = models.IntegerField(blank=True, null=True)
    three_attempt = models.IntegerField(blank=True, null=True)
    ft_made = models.IntegerField(blank=True, null=True)
    ft_attempt = models.IntegerField(blank=True, null=True)
    orb = models.IntegerField(blank=True, null=True)
    drb = models.IntegerField(blank=True, null=True)
    trb = models.IntegerField(blank=True, null=True)
    ast = models.IntegerField(blank=True, null=True)
    stl = models.IntegerField(blank=True, null=True)
    blk = models.IntegerField(blank=True, null=True)
    tov = models.IntegerField(blank=True, null=True)
    pf = models.IntegerField(blank=True, null=True)
    pts = models.IntegerField(blank=True, null=True)
    coolness = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_line'

class Player(models.Model):
    id = models.TextField(unique=True, primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'

class Team(models.Model):
    id = models.TextField(unique=True, primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'