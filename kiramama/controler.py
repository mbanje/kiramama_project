from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from models import *


#This function will be used to respond to a report through RapidPro
#def respond(All the necessary parameters):
#	pass


def send_sms_via_rapidpro(args):
	'''This function is used to send an sms via RapidPro'''
	print("I will put here a code to send ==>")
	print(args['response'])

def check_prefixe(args):
	'''This function check if the passed object has a valid prefixe'''
	if args['text'].split('+')[0] in getattr(settings,'KNOWN_PREFIXES',''):
		args['valide'] = True
		args['model_name'] = getattr(settings,'KNOWN_PREFIXES','')[args['text'].split('+')[0]]
	else:
		args['valide'] = False
	
	




@csrf_exempt
def receive_report(request):
	'''This function will receive requests sent by RapidPro when a new sms repport is received by RapidPro'''
	incoming_data = {}
	list_of_data = request.body.split("&")
	for i in list_of_data:
		incoming_data[i.split("=")[0]] = i.split("=")[1]

	#check if an incoming message has a valide prefixe
	check_prefixe(incoming_data)
	if not incoming_data['valide']:#If the prefix is not known, we inform the user and we stop to deal with this message
		incoming_data['response']="The prefix of your message is not valide"
		send_sms_via_rapidpro(incoming_data)
		resp = 0
		return HttpResponse(resp)

	#Let's create an instance of the concerned model
	try:
		related_object = globals()[incoming_data['model_name']]()
	except:
		print("There is an exception due to the model which doesn't exist...")
		resp = "00"
		return HttpResponse(resp)

	#Let's call the check_report() function of the  object
	related_object.check_report(incoming_data)
	

	resp = 1
	return HttpResponse(resp)

