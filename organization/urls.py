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
from organization.editViews import *

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
    url(r'^addIndividual/$', AddIndividual.as_view(), name='addIndividual'),
    url(r'^constructForm/$', views.constructForm, name='constructForm'),
    
    url(r'^addBiosource/$', AddBiosource.as_view(), name='addBiosource'),
    url(r'^addBiosample/$', AddBiosample.as_view(), name='addBiosample'),
    url(r'^addModification/$', AddModification.as_view(), name='addModification'),
    url(r'^addTarget/$', AddTarget.as_view(), name='addTarget'),
    url(r'^addConstruct/$', AddConstruct.as_view(), name='addConstruct'),
    url(r'^addProtocol/$', AddProtocol.as_view(), name='addProtocol'),
    url(r'^addDocument/$', AddDocument.as_view(), name='addDocument'),
    url(r'^addTreatmentRnai/$', AddTreatmentRnai.as_view(), name='addTreatmentRnai'),
    url(r'^addTreatmentChemical/$', AddTreatmentChemical.as_view(), name='addTreatmentChemical'),
    url(r'^addOther/$', AddOther.as_view(), name='addOther'),
    url(r'^addPublication/$', AddPublication.as_view(), name='addPublication'),
    url(r'^addExperiment/$', AddExperiment.as_view(), name='addExperiment'),
    url(r'^addSequencingRun/$', AddSequencingRun.as_view(), name='addSequencingRun'),   
    url(r'^addBarcode/$', AddBarcode.as_view(), name='addBarcode'),
    
    url(r'^editProject/(?P<pk>[0-9]+)/$', EditProject.as_view(), name='editProject'),
    url(r'^deleteProject/(?P<pk>[0-9]+)/$', DeleteProject.as_view(), name='deleteProject'),
    url(r'^editExperiment/(?P<pk>[0-9]+)/$', EditExperiment.as_view(), name='editExperiment'),
    url(r'^deleteExperiment/(?P<pk>[0-9]+)/$', DeleteExperiment.as_view(), name='deleteExperiment'),
    url(r'^editIndividual/(?P<pk>[0-9]+)/$', EditIndividual.as_view(), name='editIndividual'),
    url(r'^deleteIndividual/(?P<pk>[0-9]+)/$', DeleteIndividual.as_view(), name='deleteIndividual'),
    url(r'^editBiosource/(?P<pk>[0-9]+)/$', EditBiosource.as_view(), name='editBiosource'),
    url(r'^deleteBiosource/(?P<pk>[0-9]+)/$', DeleteBiosource.as_view(), name='deleteBiosource'),
    url(r'^editBiosample/(?P<pk>[0-9]+)/$', EditBiosample.as_view(), name='editBiosample'),
    url(r'^deleteBiosample/(?P<pk>[0-9]+)/$', DeleteBiosample.as_view(), name='deleteBiosample'),
    url(r'^editTreatmentRnai/(?P<pk>[0-9]+)/$', EditTreatmentRnai.as_view(), name='editTreatmentRnai'),
    url(r'^deleteTreatmentRnai/(?P<pk>[0-9]+)/$', DeleteTreatmentRnai.as_view(), name='deleteTreatmentRnai'),
    url(r'^editTreatmentChemical/(?P<pk>[0-9]+)/$', EditTreatmentChemical.as_view(), name='editTreatmentChemical'),
    url(r'^deleteTreatmentChemical/(?P<pk>[0-9]+)/$', DeleteTreatmentChemical.as_view(), name='deleteTreatmentChemical'),
    url(r'^editOther/(?P<pk>[0-9]+)/$', EditOther.as_view(), name='editOther'),
    url(r'^deleteOther/(?P<pk>[0-9]+)/$', DeleteOther.as_view(), name='deleteOther'),
    url(r'^editModification/(?P<pk>[0-9]+)/$', EditModification.as_view(), name='editModification'),
    url(r'^deleteModification/(?P<pk>[0-9]+)/$', DeleteModification.as_view(), name='deleteModification'),
    url(r'^editConstruct/(?P<pk>[0-9]+)/$', EditConstruct.as_view(), name='editConstruct'),
    url(r'^deleteConstruct/(?P<pk>[0-9]+)/$', DeleteConstruct.as_view(), name='deleteConstruct'),
    url(r'^editGenomicRegions/(?P<pk>[0-9]+)/$', EditGenomicRegions.as_view(), name='editGenomicRegions'),
    url(r'^deleteGenomicRegions/(?P<pk>[0-9]+)/$', DeleteGenomicRegions.as_view(), name='deleteGenomicRegions'),
    url(r'^editTarget/(?P<pk>[0-9]+)/$', EditTarget.as_view(), name='editTarget'),
    url(r'^deleteTarget/(?P<pk>[0-9]+)/$', DeleteTarget.as_view(), name='deleteTarget'),
    
    
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 