from django.db import models

# Create your models here.
class AverageVolumeDaily(models.Model):
	scriptCode = models.CharField(max_length=50)
	timeCode = models.IntegerField()
	averageVolume = models.FloatField()
	lastDayVolume = models.IntegerField()
	percentChange = models.FloatField()

	def __str__(self):
		return self.scriptCode + " - " +str(self.timeCode)

class bluechip(models.Model):
	scriptCode = models.CharField(max_length=50)

	def __str__(self):
		return self.scriptCode


class tradingDay(models.Model):
	tradingYear = models.IntegerField()
	tradingMonth = models.IntegerField()
	tradingDay = models.IntegerField()

	def __str__(self):
		return self.tradingYear + " - " +str(self.tradingMonth) + " - " +str(self.tradingDay) 