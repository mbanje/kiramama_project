from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

'''This function will receive requests sent by RapidPro when a new sms repport is received by RapidPro'''
def receive_report(request):
	print("It's ok!!!!!!!!!!!!!!!!!!")
	return HttpResponse("It is ok")