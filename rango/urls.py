# handles remaining url string, the host portion is already
# stripped away
from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	#mapping the about view to rango/about
	url(r'^about/', views.about, name='about'),
	url(r'^index/', views.index, name='index'),
]