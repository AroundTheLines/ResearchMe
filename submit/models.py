from django.db import models

class Resume(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    cover_letter = models.CharField(max_length=2000)
    skills = models.CharField(max_length=3000)
    experience = models.CharField(max_length=3000)
    score = models.CharField(max_length=100,default="")
    rank = models.CharField(max_length=10,default="")
    sentiment_rank = models.CharField(max_length=10,default="")
    sub_date = models.DateTimeField("Submit time")
    def __str__(self):
        return " ".join([self.first_name, self.last_name])

class RunningTotal(models.Model):
    current_top = models.CharField(max_length=100)
	def __str__(self):
		return self.current_top
    
class KeyWord(models.Model):
    word = models.CharField(max_length=1000)
    weight = models.CharField(max_length=100)
	def __str__(self):
		return self.word