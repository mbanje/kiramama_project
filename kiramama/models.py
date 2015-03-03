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
		'''This function checks if the phone user sent the expected number of values'''
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
		#Let's split the text and put the result in data object
		data['splited_object'] = data['text'].split('+')

		data['valide'] = True

		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		'''Let's check if the phone user sent a valid id of a pregnant mother or a baby.
			A valid id is made of 3 parts of numbers. There is no space or any other caracter between two parts.
			.The first part is made of last five numbers of the identity card of the mother if she has it, if not,
			it is made of last five numbers of the identity card of the CHW.
			.The second part is made of two number for the current date followed by two number of the current month followed by
			two number of the current year(two last. eg: 030315 for 03/03/2015).
			.The last part is made of two numbers. eg : 01, 02, 03 ...
			01 is for the first person without an identity card registered by that CHW in a day. 02 is for the second on
			the same day.
		'''
		
		

class All_messages(models.Model):
	whole_sms = models.CharField(max_length=10)
	prefixe = models.ForeignKey(Prefixe)
	identifier = models.IntegerField()
