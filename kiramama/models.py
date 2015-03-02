from django.db import models
from django.conf import settings


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
	
	def check_number_of_sent_valous(self, data):
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "You sent less variables than expected"
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "You sent more values than expected"
	def check_patient_id():
		pass
	def check_last_mestrual_periode():
		pass
	def check_second_appointement_date():
		pass
	def check_gravity():
		pass
	def check_parity():
		pass
	def check_previous_pregnancy():
		pass
	def check_current_symptoms():
		pass
	def check_location():
		pass
	def check_mother_weight():
		pass
	def check_mother_height():
		pass
	def check_toilet():
		pass
	def check_hand_washing():
		pass

	def check_report(self, data):
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return
		

class All_messages(models.Model):
	whole_sms = models.CharField(max_length=10)
	prefixe = models.ForeignKey(Prefixe)
	identifier = models.IntegerField()
