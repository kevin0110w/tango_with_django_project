# import HttpResponse object from django.http module
from django.http import HttpResponse

# create the one view, called index
def index(request):
# parameter is a HttpResponse object named as request
# a link is provided to go to the about page
    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
	# return a HttpResponse object that takes a string 
	# representing the content of the page we wish to send to the
	# the client requesting the view
	
#Create a new view method called about
#A link is provided to go back to the index
def about(request):
	return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
	