from django.conf.urls import *
from kiramama.views import home
from kiramama.controler import receive_report

urlpatterns = patterns('',
                       # dashboard view for viewing all poll reports in one place
						url(r'^$', home, name="home"),
						url(r'^report$', receive_report, name = "report"),
						
)