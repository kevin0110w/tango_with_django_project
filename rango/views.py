from django.shortcuts import render
# import HttpResponse object from django.http module
from django.http import HttpResponse

# create the one view, called index
def index(request):
    # Construct a dictionary to pass to the template engine as its context
    # The key, boldmessage, is the same as {{ boldmessage }} in <Workspace>/template/rango/index.html
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # Return a rendered response to send to the client
    # Make use of the shortcut function for efficiency
    # The first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)
# parameter is a HttpResponse object named as request
# a link is provided to go to the about page
#    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
	# return a HttpResponse object that takes a string 
	# representing the content of the page we wish to send to the
	# the client requesting the view
	
#Create a new view method called about
#A link is provided to go back to the index
def about(request):
	return render(request, 'rango/about.html')
	#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
	