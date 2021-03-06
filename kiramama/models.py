from django.db import models
from django.conf import settings
import re


#NB : Multiple valous of one column must be separated by '*'

class PersonToTrack(models.Model):
	person_id = models.CharField(max_length=30,primary_key=True)
	name = models.CharField(max_length=20)

class CHW(models.Model):
	name = models.CharField(max_length=20)
	tracked_persons = models.ForeignKey(PersonToTrack)

class Prefixe(models.Model):
	prefixe = models.CharField(max_length=3)
	table_name = models.CharField(max_length=50)

class PregnancyConfirmation(models.Model):
	last_menstrual_period = models.CharField(max_length=10)
	second_appointment_date = models.CharField(max_length=10)
	gravidity = models.CharField(max_length=2)
	parity = models.CharField(max_length=2)
	previous_pregnancy = models.CharField(max_length=2)
	current_symptoms = models.CharField(max_length=17)
	location = models.CharField(max_length=2)
	mother_weight = models.CharField(max_length=6)
	mother_height = models.CharField(max_length=5)
	toilet = models.CharField(max_length=2)
	hand_washing = models.CharField(max_length=2)
	

			
		

class All_messages(models.Model):
	whole_sms = models.CharField(max_length=10)
	prefixe = models.ForeignKey(Prefixe)
	identifier = models.IntegerField()
