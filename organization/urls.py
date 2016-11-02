'''
Created on Oct 18, 2016

@author: nanda
'''
from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from organization.views import *

urlpatterns = [
    url(r'^$', views.login,{'template_name': 'registration/login.html'},name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'registration/logout.html'}, name='logout'),
#     url(r'^$', RedirectView.as_view(pattern_name='login',permanent=False)),
    url(r'^home/$', HomeView.as_view(), name='home'),
    
    url(r'^addProject/$', AddProject.as_view(), name='addProject'),
    url(r'^showProject/$', ShowProject.as_view(), name='showProject'),
    url(r'^detailProject/(?P<pk>[0-9]+)/$', DetailProject.as_view(), name='detailProject'),
    
    url(r'^detailExperiment/(?P<pk>[0-9]+)/$', DetailExperiment.as_view(), name='detailExperiment'),
    
#     url(r'^addIndividual/$', AddIndividual.as_view(), name='addIndividual'),
#     url(r'^addIndividual/constructForm/$',  views.constructForm, name='constructIndividual'), 
#     
    url(r'^stepOne/$', AddIndividual.as_view(), name='stepOne'),
    url(r'^stepOne/constructForm/$', views.constructForm, name='constructForm'),
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 