from rango.forms import CategoryForm
from django.shortcuts import render
# import HttpResponse object from django.http module
from django.http import HttpResponse
# Import the Category model
from rango.models import Category
# Import the Page model
from rango.models import Page
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

# create the one view, called index
def index(request):
    request.session.set_test_cookie()
    # Construct a dictionary to pass to the template engine as its context
    # The key, boldmessage, is the same as {{ boldmessage }} in <Workspace>/template/rango/index.html
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # Return a rendered response to send to the client
    # Make use of the shortcut function for efficiency
    # The first parameter is the template we wish to use
    # return render(request, 'rango/index.html', context=context_dict)
    # parameter is a HttpResponse object named as request
    # a link is provided to go to the about page
    #    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
	# return a HttpResponse object that takes a string 
	# representing the content of the page we wish to send to the
	# the client requesting the view

    # Query the database for a list of All categories
    # currently stored.
    # Order the categories by no. of likes in desc order
    # Retrieve the top 5 only or all if less than 5
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    viewed_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': viewed_list}
	
	
	# Call the helper function to handle the cookie
    #visitor_cookie_handler(request, response)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    # Obtain Response object early to add cookie info
    response = render(request, 'rango/index.html', context=context_dict)
	# Render the response and send it back
    #return render(request, 'rango/index.html', context_dict)
    return response

	
#Create a new view method called about
#A link is provided to go back to the index
def about(request):
    if request.session.test_cookie_worked():
	    print("TEST COOKIE WORKED!")
	    request.session.delete_test_cookie()
    
    visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context_dict)
    return response
	#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        # Try and find a category name slug with given name
        # If not possible, the .get() method raises a DoesNotExist
        # exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages
        pages = Page.objects.filter(category=category)

        # Add results list to the template context under name pages
        context_dict['pages'] = pages
        
        # Also add the category object from the database
        # to the context dictionary
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If not able to find specified category, don't do 
        # anything, the template will display a message
        context_dict['category'] = None
        context_dict['pages'] = None

    # render the response and return to teh client
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # Check if HTTP request was a POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # If provided with a valid form
        # save the new category to the database
        if form.is_valid():
            form.save(commit=True)
            # direct user back to index page after
            # category is saved
            return index(request)
        else:
            # If supplied form contains errors,
            # print these to the terminal
            print(form.errors)

        # Handle the bad form, new form or no form supplied cases
        # and render with error messages if any

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()
            return show_category(request, category_name_slug)

        else:
                print(form.errors)

    context_dict = {'form':form, 'category':category}
        
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # Boolean value to tell the template whether a registration was
    # successful. Initially set to false which can be changed when a 
    # registration is successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
            
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days>0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
    
    #def visitor_cookie_handler(request, response):
	# Get the number of visists to the site.
	# Use COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer
	# if the cookie does not exist, the default value of 1 is used
    # 
    #visits = int(request.COOKIES.get('visits', '1'))
	#
    #last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    #last_visit_time = datetime.strptime(last_visit_cookie[:7], '%Y-%m-%d %H:%M:%S')
    #
    #if (datetime.now() - last_visit_time).days > 0:
    #    visits = visits + 1
    #    response.set_cookie('last_visit', str(datetime.now()))
    #else:
        # set the last visit cookie
    #    response.set_cookie('last_visit', last_visit_cookie)
	# update/set the visits cookie
    #response.set_cookie('visits', visits)



