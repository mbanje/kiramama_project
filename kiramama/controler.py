import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from models import *
import json

#This function will be used to respond to a report through RapidPro
#def respond(All the necessary parameters):
#	pass


def send_sms_via_rapidpro(args):
	'''This function is used to send an sms via RapidPro'''
	print("args['run']")
	print(args['run'])
	print("args['phone']")
	print(args['phone'])
	print("args['text']")
	print(args['text'])


	data_to_send = {
  					"urn": ["tel:+25779278861"],
  					"text": "My first SMS message to Mbanje",
  					"relayer": 156
					}
	message_url = 'https://rapidpro.io/api/v1/messages.json'
	token = 'c2195bdeeca5819f1ded643f0152c0e8bf9a8474'
	#token = raw_input('Enter your token: ')
	response = requests.post(message_url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data_to_send))
	#print("response")
	#print(response)
	#print("response.body")
	#import ipdb; ipdb.set_trace();	
	print(args['response'])

def check_prefixe(args):
	'''This function check if the passed object has a valid prefixe.
	If the prefixe is valid, this function determine also the related model name.
	'''
	if args['text'].split('+')[0] in getattr(settings,'KNOWN_PREFIXES',''):
		args['valide'] = True
		args['model_name'] = getattr(settings,'KNOWN_PREFIXES','')[args['text'].split('+')[0]]
	else:
		args['valide'] = False
	
	




@csrf_exempt
def receive_report(request):
	'''This function will receive requests sent by RapidPro when a new sms repport is received by RapidPro'''
	incoming_data = {}
	incoming_data['valide'] = True
	incoming_data['response']="The default response..."
	resp = 0
	print("111")
	list_of_data = request.body.split("&")
	for i in list_of_data:
		incoming_data[i.split("=")[0]] = i.split("=")[1]
	print("222")
	#check if an incoming message has a valide prefixe
	check_prefixe(incoming_data)
	if not incoming_data['valide']:#If the prefix is not known, we inform the user and we stop to deal with this message
		incoming_data['response']="The prefix of your message is not valide"
		send_sms_via_rapidpro(incoming_data)
		resp = 0
		return HttpResponse(resp)
	print("333")
	#Let's create an instance of the concerned model
	try:
		related_object = globals()[incoming_data['model_name']]()
	except:
		print("There is an exception due to the model which doesn't exist...")
		resp = 0
		return HttpResponse(resp)
	print("444")
	#Let's call the check_report() function of the object
	related_object.check_report(incoming_data)
	if not incoming_data['valide']:
		send_sms_via_rapidpro(incoming_data)
		return HttpResponse(resp)

	''' We will put here code to save data '''

	incoming_data['response'] = "Your message is well written. Thank you."
	send_sms_via_rapidpro(incoming_data)
	print("FIN...")
	return HttpResponse(resp)


	print("555")
	
	resp = 1
	return HttpResponse(resp)

