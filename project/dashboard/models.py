from django.db import models

class PollingData(models.Model):
    state = models.CharField(max_length=100)
    polling_station = models.IntegerField()
    gmen = models.IntegerField()
    gwomen = models.IntegerField()
    gthird = models.IntegerField()
    gtotal = models.IntegerField()
    omen = models.IntegerField()
    owomen = models.IntegerField()
    othird = models.IntegerField()
    ototal = models.IntegerField()
    smen = models.IntegerField()
    swomen = models.IntegerField()
    stotal = models.IntegerField()
    overall_total = models.IntegerField()

    def __str__(self):
        return f"{self.state} - Polling Station {self.polling_station}"

class History(models.Model):
    pc_name = models.CharField(max_length=100)
    no = models.IntegerField()
    type = models.CharField(max_length=100)  # Renamed from 'type'
    state = models.CharField(max_length=100)
    candidate_name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    electors = models.IntegerField()
    votes = models.IntegerField()
    turnout = models.FloatField()
    margin = models.IntegerField()
    margin_percentage = models.FloatField()
    year = models.IntegerField()

    def __str__(self):
        return self.pc_name
