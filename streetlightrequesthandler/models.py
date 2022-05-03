from django.db import models

# Create your models here.
class StreetLight(models.Model):
    ID=models.CharField(max_length=255,null=False)
    BV=models.FloatField(null=False)
    BI=models.FloatField(null=False)
    SV=models.FloatField(null=False)
    SI=models.FloatField(null=False)
    LV=models.FloatField(null=False)
    LI=models.FloatField(null=False)
    BA=models.FloatField(null=False)
    STATE=models.CharField(max_length=255,null=False)
    LAT=models.CharField(max_length=255,null=False)
    LON=models.CharField(max_length=255,null=False)
    DRY_BIN=models.CharField(max_length=255,null=False)
    WET_BIN=models.CharField(max_length=255,null=False)
    TIME_STAMP = models.DateTimeField(auto_now=True,null=False)