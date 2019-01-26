from rango.forms import CategoryForm

from django.shortcuts import render
# import HttpResponse object from django.http module
from django.http import HttpResponse

# Import the Category model
from rango.models import Category
# Import the Page model
from rango.models import Page
from rango.forms import PageForm

# create the one view, called index
def index(request):
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


    # Render the response and send it back
    return render(request, 'rango/index.html', context_dict)

	
#Create a new view method called about
#A link is provided to go back to the index
def about(request):
	return render(request, 'rango/about.html')
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

