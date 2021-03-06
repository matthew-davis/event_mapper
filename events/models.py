from django.db import models
from django.utils.timezone import now

class Event(models.Model):
    GlobalEventID = models.IntegerField()
    Day = models.IntegerField(null=True)
    MonthYear = models.IntegerField(null=True)
    Year = models.IntegerField(null=True)
    FractionDate = models.FloatField(null=True)
    Actor1Code = models.CharField(max_length=255, null=True)
    Actor1Name = models.CharField(max_length=255, null=True)
    Actor1CountryCode = models.CharField(max_length=255, null=True)
    Actor1KnownGroupCode = models.CharField(max_length=255, null=True)
    Actor1EthnicCode = models.CharField(max_length=255, null=True)
    Actor1Religion1Code = models.CharField(max_length=255, null=True)
    Actor1Religion2Code = models.CharField(max_length=255, null=True)
    Actor1Type1Code = models.CharField(max_length=255, null=True)
    Actor1Type2Code = models.CharField(max_length=255, null=True)
    Actor1Type3Code = models.CharField(max_length=255, null=True)
    Actor2Code = models.CharField(max_length=255, null=True)
    Actor2Name = models.CharField(max_length=255, null=True)
    Actor2CountryCode = models.CharField(max_length=255, null=True)
    Actor2KnownGroupCode = models.CharField(max_length=255, null=True)
    Actor2EthnicCode = models.CharField(max_length=255, null=True)
    Actor2Religion1Code = models.CharField(max_length=255, null=True)
    Actor2Religion2Code = models.CharField(max_length=255, null=True)
    Actor2Type1Code = models.CharField(max_length=255, null=True)
    Actor2Type2Code = models.CharField(max_length=255, null=True)
    Actor2Type3Code = models.CharField(max_length=255, null=True)
    IsRootEvent = models.IntegerField(null=True)
    EventCode = models.CharField(max_length=255, null=True)
    EventBaseCode = models.CharField(max_length=255, null=True)
    EventRootCode = models.CharField(max_length=255, null=True)
    QuadClass = models.IntegerField(null=True)
    GoldsteinScale = models.FloatField(null=True)
    NumMentions = models.IntegerField(null=True)
    NumSources = models.IntegerField(null=True)
    NumArticles = models.IntegerField(null=True)
    AvgTone = models.FloatField(null=True)
    Actor1Geo_Type = models.IntegerField(null=True)
    Actor1Geo_Fullname = models.CharField(max_length=255, null=True)
    Actor1Geo_CountryCode = models.CharField(max_length=255, null=True)
    Actor1Geo_ADM1Code = models.CharField(max_length=255, null=True)
    Actor1Geo_ADM2Code = models.CharField(max_length=255, null=True)
    Actor1Geo_Lat = models.FloatField(null=True)
    Actor1Geo_Long = models.FloatField(null=True)
    Actor1Geo_FeatureID = models.CharField(max_length=255, null=True)
    Actor2Geo_Type = models.IntegerField(null=True)
    Actor2Geo_Fullname = models.CharField(max_length=255, null=True)
    Actor2Geo_CountryCode = models.CharField(max_length=255, null=True)
    Actor2Geo_ADM1Code = models.CharField(max_length=255, null=True)
    Actor2Geo_ADM2Code = models.CharField(max_length=255, null=True)
    Actor2Geo_Lat = models.FloatField(null=True)
    Actor2Geo_Long = models.FloatField(null=True)
    Actor2Geo_FeatureID = models.CharField(max_length=255, null=True)
    ActionGeo_Type = models.IntegerField(null=True)
    ActionGeo_Fullname = models.CharField(max_length=255, null=True)
    ActionGeo_CountryCode = models.CharField(max_length=255, null=True)
    ActionGeo_ADM1Code = models.CharField(max_length=255, null=True)
    ActionGeo_ADM2Code = models.CharField(max_length=255, null=True)
    ActionGeo_Lat = models.FloatField(null=True)
    ActionGeo_Long = models.FloatField(null=True)
    ActionGeo_FeatureID = models.CharField(max_length=255, null=True)
    DateAdded = models.CharField(max_length=255, null=True)
    SourceURL = models.TextField(blank=True, null=True, unique=True)
    DataMapCountry = models.CharField(max_length=255, null=True)
    EventDate = models.DateTimeField(default=now, editable=False)

def __str__(self):
    return self.GlobalEventID
