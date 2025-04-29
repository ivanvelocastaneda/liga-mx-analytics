# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllPlayers(models.Model):
    player_id = models.AutoField(primary_key=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    player_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    field_position = models.CharField(max_length=2, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'All_Players'


class FieldPlayerStats(models.Model):
    player = models.OneToOneField(AllPlayers, models.DO_NOTHING, primary_key=True)
    games_played = models.IntegerField(blank=True, null=True)
    goals = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    yellow_cards = models.IntegerField(blank=True, null=True)
    red_cards = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    pk_made = models.IntegerField(blank=True, null=True)
    pk_attempted = models.IntegerField(blank=True, null=True)
    total_shots = models.IntegerField(blank=True, null=True)
    shots_on_target = models.IntegerField(blank=True, null=True)
    fouls_commited = models.IntegerField(blank=True, null=True)
    fouls_drawn = models.IntegerField(blank=True, null=True)
    offsides = models.IntegerField(blank=True, null=True)
    crosses = models.IntegerField(blank=True, null=True)
    interceptions = models.IntegerField(blank=True, null=True)
    tackles_won = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Field_Player_Stats'


class Fixtures(models.Model):
    tournament = models.CharField(max_length=100, blank=True, null=True)
    matchweek = models.IntegerField(blank=True, null=True)
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateField()
    home_team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    away_team = models.ForeignKey('Teams', models.DO_NOTHING, related_name='fixtures_away_team_set', blank=True, null=True)
    stadium = models.ForeignKey('Stadiums', models.DO_NOTHING, blank=True, null=True)
    referee = models.ForeignKey('Referees', models.DO_NOTHING, blank=True, null=True)
    score = models.CharField(max_length=50, blank=True, null=True)
    winner = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Fixtures'


class GoalkeepersStats(models.Model):
    player = models.OneToOneField(AllPlayers, models.DO_NOTHING, primary_key=True)
    games_played = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    pk_made = models.IntegerField(blank=True, null=True)
    pk_attempted = models.IntegerField(blank=True, null=True)
    clean_sheets = models.IntegerField(blank=True, null=True)
    goals_against = models.IntegerField(blank=True, null=True)
    shots_on_target_against = models.IntegerField(blank=True, null=True)
    saves = models.IntegerField(blank=True, null=True)
    yellow_cards = models.IntegerField(blank=True, null=True)
    red_cards = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Goalkeepers_Stats'


class Referees(models.Model):
    referee_id = models.AutoField(primary_key=True)
    referee_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Referees'


class Stadiums(models.Model):
    stadium_id = models.AutoField(primary_key=True)
    stadium_name = models.CharField(max_length=100)
    capacity = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Stadiums'


class TeamStats(models.Model):
    season = models.CharField(max_length=50, blank=True, null=True)
    team = models.OneToOneField('Teams', models.DO_NOTHING, primary_key=True)
    games_played = models.IntegerField(blank=True, null=True)
    wins = models.IntegerField(blank=True, null=True)
    draws = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)
    goals_scored = models.IntegerField(blank=True, null=True)
    goals_conceded = models.IntegerField(blank=True, null=True)
    goal_difference = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    table_position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Team_Stats'


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    stadium = models.ForeignKey(Stadiums, models.DO_NOTHING, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Teams'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
