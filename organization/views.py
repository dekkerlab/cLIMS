from django.contrib.auth.views import login as contrib_login
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from organization.models import *
from organization.forms import ProjectForm, ExperimentForm
from django.forms.formsets import formset_factory
import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from wetLab.forms import *
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
        elif('Collaborator' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "collaborator"
            prj = Project.objects.filter((Q(project_contributor=request.user.id)) , project_active="True") 
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
    template_name = 'form.html'
    error_page = 'error.html'
    form_class = ProjectForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = form.save(commit= False)
            result.project_owner = request.user
            result.save()
            project_contributor = request.POST.getlist('project_contributor')
            for contributor in project_contributor:
                user = User.objects.get(pk=contributor)
                result.project_contributor.add(user)
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form})

class ShowProject(View):
    template_name = 'showProject.html'
    error_page = 'error.html'
    
    def get(self,request):
        userType = request.session['currentGroup']
        userId = request.user.id
        if (userType == "member"):
            obj = Project.objects.filter(Q(project_owner=userId) |  Q(project_contributor=userId))
        elif (userType == "collaborator"):
            obj = Project.objects.filter(Q(project_contributor=userId))
        elif (userType == "admin"):
            obj = Project.objects.all()
        else:
            raise ValidationError
        context = {
            'object': obj,
        }
        return render(request, self.template_name, context)
    



# class AddProject(View): 
#     template_name = 'stepOneForm.html'
#     error_page = 'error.html'
#     form_class = ExperimentForm
#     ChoiceForm_set = formset_factory(ExperimentForm, extra=0, min_num=1, validate_min=True)
#     
#     def get(self,request):
#         form = self.form_class()
#         return render(request, self.template_name,{'form':form})
#     
#     def post(self,request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             result = form.save(commit= False)
#             result.project_owner = request.user
#             result.save()
#             project_contributor = request.POST.getlist('project_contributor')
#             for contributor in project_contributor:
#                 user = User.objects.get(pk=contributor)
#                 result.project_contributor.add(user)
#             return HttpResponseRedirect('/showProject/')
#         else:
#             return render(request, self.error_page, {})
    


class DetailProject(View):
    template_name = 'detailProject.html'
    error_page = 'error.html'
    def get(self,request,pk):
        request.session['projectId'] = pk
        context = {}
        prj = Project.objects.get(pk=pk)
    #     units = Lane.objects.filter(project=pk)
    #     files = DeepSeqFile.objects.filter(project=pk)
        experiments = Experiment.objects.filter(experiment_project=pk)
        context['project']= prj
    #     context['units']= units
    #     context['files']= files
        context['experiments']= experiments
        return render(request, self.template_name, context)


class DetailExperiment(View):
    template_name = 'detailExperiment.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        experiment = Experiment.objects.get(pk=pk)
        context['experiment']= experiment
        return render(request, self.template_name, context)








def createJSON(request, fieldTypePk):
    json_object = JsonObjField.objects.get(pk=fieldTypePk).field_set
    data = {}
    for keys in json_object:
        formVal = request.POST.get(keys)
        data[keys] = formVal
    json_data = json.dumps(data)
    return(json_data)

# 
# class StepOne(View): 
#     template_name = 'stepOneForm.html'
#     error_page = 'error.html'
#     form_class = IndividualForm
#     biosourceForm_set = formset_factory(BiosourceForm)
#     biosampleForm_set = formset_factory(BiosampleForm)
#     
#     def get(self,request):
#         form = self.form_class()
#         biosourceFormset = self.biosourceForm_set()
#         biosampleFormset = self.biosampleForm_set()
#         form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
#         for f in biosourceFormset:
#             f.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
#         return render(request, self.template_name,{'form':form,'biosourceFormset':biosourceFormset,'biosampleFormset':biosampleFormset})
#     
#     def post(self,request):
#         form = self.form_class(request.POST)
#         biosourceFormset = self.biosourceForm_set(request.POST)
#         biosampleFormset = self.biosampleForm_set(request.POST)
#         if all([form.is_valid(), biosourceFormset.is_valid(),biosampleFormset.is_valid()]):
#             result = form.save(commit= False)
#             individual_type = request.POST.get('individual_type')
#             result.individual_fields = createJSON(request, individual_type)
#             result.save()
#             for inline_form in biosourceFormset:
#                 biosource = inline_form.save(commit=False)
#                 biosource.biosource_individual = result
#                 biosource.save()
#             return HttpResponseRedirect('/showProject/')

class AddIndividual(View): 
    template_name = 'addIndividual.html'
    error_page = 'error.html'
    form_class = IndividualForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
        return render(request, self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            individual = form.save(commit= False)
            individual_type = request.POST.get('individual_type')
            individual.individual_fields = createJSON(request, individual_type)
            individual.save()
            request.session['individualPK'] = individual.pk
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
            return render(request, self.template_name,{'form':form})

class AddBiosource(View): 
    template_name = 'stepBiosource.html'
    error_page = 'error.html'
    form_class = BiosourceForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
        return render(request, self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            biosource = form.save(commit=False)
            individualPK = request.session['individualPK']
            biosource.biosource_individual = Individual.objects.get(individualPK)
            biosource.save()
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
            return render(request, self.template_name,{'form':form})


class StepOne(View): 
    template_name = 'stepOneForm.html'
    error_page = 'error.html'
    form_class = IndividualForm
    biosourceForm_class = BiosourceForm
    biosampleForm_class  = BiosampleForm
    selectForm_class = SelectForm
    
    def get(self,request):
        form = self.form_class()
        biosourceForm = self.biosourceForm_class()
        biosampleForm = self.biosampleForm_class()
        selectForm = self.selectForm_class()
        form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
        biosourceForm.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
        biosourceForm.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
        biosampleForm.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
        return render(request, self.template_name,{'form':form,'biosourceForm':biosourceForm,'biosampleForm':biosampleForm,'selectForm':selectForm})
    
    def post(self,request):
        form = self.form_class(request.POST)
        biosourceForm = self.biosourceForm_class(request.POST)
        biosampleForm = self.biosampleForm_class(request.POST)
        selectForm = self.selectForm_class(request.POST)
        check_individual = request.POST.get('check_individual')
        check_biosource = request.POST.get('check_biosource')
        check_sample = request.POST.get('check_biosource')

        if (check_individual):
            individual = selectForm['individual']

        elif(form.is_valid()):
            individual = form.save(commit= False)
            individual_type = request.POST.get('individual_type')
            individual.individual_fields = createJSON(request, individual_type)
            individual.save()
        else:
            form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
            biosourceForm.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
            biosourceForm.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
            biosampleForm.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
            return render(request, self.template_name,{'form':form,'biosourceForm':biosourceForm,'biosampleForm':biosampleForm,'selectForm':selectForm})
        
        if (check_biosource):
            biosource = selectForm['biosource']

        elif(biosourceForm.is_valid()):
            biosource = biosourceForm.save(commit=False)
            biosource.biosource_individual = individual
            biosource.save()
        else:
            form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
            biosourceForm.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
            biosourceForm.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
            biosampleForm.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
            return render(request, self.template_name,{'form':form,'biosourceForm':biosourceForm,'biosampleForm':biosampleForm,'selectForm':selectForm})
           
        if (check_sample):
            biosample = selectForm['biosample']
        
        elif(biosampleForm.is_valid()):
            biosample = biosampleForm.save(commit= False)
            biosample.userOwner = User.objects.get(pk=request.user.pk)
            biosample.biosample_biosource = biosource
            biosample.biosample_individual = individual
            if(request.POST.get('biosample_type')):
                biosample_type = request.POST.get('biosample_type')
                biosample.biosample_fields = createJSON(request, biosample_type)
            biosample.save()
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
            biosourceForm.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
            biosourceForm.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
            biosampleForm.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
            return render(request, self.template_name,{'form':form,'biosourceForm':biosourceForm,'biosampleForm':biosampleForm,'selectForm':selectForm})
        
        
        
            
@csrf_exempt                
def constructForm(request):
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get('pk')
        obj = JsonObjField.objects.get(pk=pk)
        return HttpResponse(json.dumps({'field_set': obj.field_set, 'model':obj.field_type}), content_type="application/json")
    else :
        return render_to_response('error.html', locals())
 
    