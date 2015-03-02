from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


#This function will be used to respond to a report through RapidPro
#def respond(All the necessary parameters):
#	pass




def check_prefixe(args):
	'''This function check if the passed object has a valid prefixe'''
	if args['text'].split('+')[0] in getattr(settings,'KNOWN_PREFIXES',''):
		args['valide'] = True
	else:
		args['valide'] = False
	
	



'''This function will receive requests sent by RapidPro when a new sms repport is received by RapidPro'''
@csrf_exempt
def receive_report(request):
	incoming_data = {}
	list_of_data = request.body.split("&")
	for i in list_of_data:
		incoming_data[i.split("=")[0]] = i.split("=")[1]
	check_prefixe(incoming_data)
	

	resp = "1"
	return HttpResponse(resp)

