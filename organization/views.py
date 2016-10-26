from django.contrib.auth.views import login as contrib_login
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from organization.models import *
from organization.forms import ProjectForm, ExperimentForm
from django.forms.formsets import formset_factory
# Create your views here.

def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login (request, **kwargs)



def home(request):
    return render(request, 'home.html')


class HomeView(View):
    template_name = 'home.html'
    error_page = 'error.html'
    
    def get(self,request):
        context = {}
        context['currentUserName']= request.user.username
        if('Member' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "member"
            prj = Project.objects.filter((Q(project_owner=request.user.id) | Q(project_contributor=request.user.id)) , project_active="True") 
            context['projects']= prj
            return render(request, self.template_name, context)
         
        elif ('Admin' in map(str, request.user.groups.all()) or 'Principal Investigator' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "admin"
            prj = Project.objects.filter(project_active="True")
            context['projects']= prj
            return render(request, self.template_name, context)
        else:
            return render(request, self.error_page)


class AddProject(View): 
    template_name = 'form1.html'
    error_page = 'error.html'
    form_class = ProjectForm
    ChoiceForm_set = formset_factory(ExperimentForm, extra=0, min_num=1, validate_min=True)
    
    def get(self,request):
        form = self.form_class()
        formset = self.ChoiceForm_set()
       
        return render(request, self.template_name,{'form':form,'formset':formset})
    
    def post(self,request):
        form = self.form_class(request.POST)
        formset = self.ChoiceForm_set(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            project = form.save()
            for inline_form in formset:
                experiment = inline_form.save(commit=False)
                experiment.exp_project = project
                experiment.save()
                return redirect(project)
        
        else:
            return render(request, self.error_page, {})
        
        
            
                
def getJson(request, pk):
    obj = JsonObjField.objects.get(pk=pk)
    context = {
        'object': obj,
    }
    return render(request, 'form1.html', context)
 
    