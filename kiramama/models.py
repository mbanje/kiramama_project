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
	
	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "You sent less variables than expected"
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "You sent more values than expected"

	def check_patient_id(self, data):
		'''This function checks if the id of the patient is valid'''
		expression = r'^[0-9]{5}((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{4}$'
		if re.search(expression, data['splited_text'][1]) is None:
			data['valide'] = False
			data['response'] = "The patient id you sent is not valide"
					
 
	def check_last_menstrual_periode(self, data):
		'''This function checks if the id of the menstrual periode is valid'''
		expression = r'^((0[1-9])|([1-2][0-9])|(3[01])).((0[1-9])|(1[0-2])).[0-9]{4}$'
		if re.search(expression, data['splited_text'][2]) is None:
			data['valide'] = False
			data['response'] = "The last menstrual date you sent is not valide"
		
	def check_second_appointement_date(self, data):
		'''This function checks if the second ANC appointement date is valid'''
		expression = r'^((0[1-9])|([1-2][0-9])|(3[01])).((0[1-9])|(1[0-2])).[0-9]{4}$'
		if re.search(expression, data['splited_text'][3]) is None:
			data['valide'] = False
			data['response'] = "The second ANC appointement date you sent is not valide"
	def check_gravity(self, data):
		''' This function checks if the gravity code sent by a CHW is valid '''
		expression = r'^[0-9]{2}$'
		if re.search(expression, data['splited_text'][4]) is None:
			data['valide'] = False
			data['response'] = "The gravity you sent is not valide"
	def check_parity(self, data):
		''' This function checks if the parity code sent by a CHW is valid '''
		expression = r'^[0-9]{2}$'
		if re.search(expression, data['splited_text'][5]) is None:
			data['valide'] = False
			data['response'] = "The parity you sent is not valide"
	def check_previous_pregnancy(self, data):
		''' This function checks if the previous pregnancy code sent by a CHW is valid '''
		#expression = r'^GS|NR|KX|YJ|LZ|HD$'
		#if re.search(expression, data['splited_text'][6]) is None:
		allowed_codes = ['GS','NR','KX','YJ','LZ','HD']
		previous_pregnancy_code = data['splited_text'][6]
		if previous_pregnancy_code not in allowed_codes:
			data['valide'] = False
			data['response'] = "The previous pregnancy code you sent is not valide"
	def check_current_symptoms(self, data):
		''' This function checks if the previous pregnancy code sent by a CHW is valid 
			Codes are separated by '.' in case of multiple codes
		'''
		#expression = r'^[(NP)(MU)(RM)(OL)(YG)](.[(NP)(MU)(RM)(OL)(YG)]){0,4}$'
		#expression = r'[^NP|^MU|^RM|^OL|^YG|^.NP|^.MU|^.RM|^.OL|^.YG]'
		#expression = r'[(NP)(MU)(RM)(OL)(YG)(.NP)(.MU)(.RM)(.OL)(.YG)]'
		allowed_words = ['NP','MU','RM','OL','YG']
		splited_symptoms = data['splited_text'][7].split('.')
		for symptom in splited_symptoms:
			if symptom not in allowed_words:
				data['valide'] = False
				data['response'] = "The current symptom(s) code(s) you sent is/are not valide"
				#It will be good to put here an instruction to stop the iteration
	def check_location(self, data):
		''' This function checks if the location code sent by a CHW is valid '''
		allowed_locations = ['HP','HO','CL','OR']
		location_code = data['splited_text'][8]
		if location_code not in allowed_locations:
			data['valide'] = False
			data['response'] = "The location code you sent is not valide"

	def check_mother_weight(self, data):
		''' This function checks if weight sent by a CHW is valid '''
		expression = r'^WT[0-9]{2,3}.[0-9]$'
		if re.search(expression, data['splited_text'][9]) is None:
			data['valide'] = False
			data['response'] = "The weight you sent is not valide"

	def check_mother_height(self, data):
		''' This function checks if height sent by a CHW is valid 
			Height must be made of two parts separated by '.' The last one
			is is made by on number
		'''
		expression = r'^HT[0-9]{2,3}.[0-9]$'
		if re.search(expression, data['splited_text'][10]) is None:
			data['valide'] = False
			data['response'] = "The height you sent is not valide"

	def check_toilet(self, data):
		pass
	def check_hand_washing(self, data):
		pass

	def check_report(self, data):
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True

		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return
		

		'''Let's check if the phone user sent a valid id of a pregnant mother or a baby.
			A valid id is made of 3 parts of numbers. There is no space or any other caracter between two parts.
			.The first part is made of last five numbers of the identity card of the mother if she has it, if not,
			it is made of last five numbers of the identity card of the CHW.
			.The second part is made of two numbers for the current date followed by two numbers of the current month followed by
			two numbers of the current year(two last. eg: 030315 for 03/03/2015).
			.The last part is made of two numbers. eg : 01, 02, 03 ...
			01 is for the first person without an identity card registered by that CHW in a day. 02 is for the second on
			the same day.
		'''
		self.check_patient_id(data)
		if not data['valide']:
			return


		'''Let's check if the last menstrual date sent by a CHW is valid'''
		self.check_last_menstrual_periode(data)
		if not data['valide']:
			return

		'''Let's check if the second ANC appointment date is valide'''
		self.check_second_appointement_date(data)
		if not data['valide']:
			return

		'''Let's check if the gravity code sent by a CHW is valid'''
		self.check_gravity(data)
		if not data['valide']:
			return

		'''Let's check if the parity code sent by a CHW is valid'''
		self.check_parity(data)
		if not data['valide']:
			return

		'''Let's check if the previous pregnancy code sent by a CHW is valid'''
		self.check_previous_pregnancy(data)
		if not data['valide']:
			return

		'''Let's check if the current symptom(s) code(s) sent by a CHW is/are valid'''
		self.check_current_symptoms(data)
		if not data['valide']:
			return

		'''Let's check if the location code sent by a CHW is valid'''
		self.check_location(data)
		if not data['valide']:
			return

		'''Let's check if the weight sent by a CHW is valid'''
		self.check_mother_weight(data)
		if not data['valide']:
			return

		'''Let's check if the height sent by a CHW is valid'''
		self.check_mother_height(data)
		if not data['valide']:
			return



			
		

class All_messages(models.Model):
	whole_sms = models.CharField(max_length=10)
	prefixe = models.ForeignKey(Prefixe)
	identifier = models.IntegerField()
