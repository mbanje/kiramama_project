from django.conf.urls import *
from kiramama.views import home
from kiramama.controlers import receive_report, test

urlpatterns = patterns('',
                       # dashboard view for viewing all poll reports in one place
						url(r'^$', home, name="home"),
						url(r'^report$', receive_report, name = "report"),
						url(r'^test$', test, name = "test"),
						
)
