from django.db import models

# Create your models here.

class Player(models.Model):
	score = models.IntegerField()

	def __str__(self):
		return self.score

class Scenario(models.Model):
	text = models.CharField(max_length=3000)
	scenario_id = models.IntegerField()
	order_n = models.IntegerField()

	def __str__(self):
		return self.text 

class Input(models.Model):
	scenario = models.ForeignKey(Scenario, on_delete = models.CASCADE)
	question = models.CharField(max_length=500)
	answers = models.CharField(max_length=500)
	chosen_answer = models.CharField(max_length=500, blank=True)
	
	def __str__(self):
		return self.question
