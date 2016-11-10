from django.contrib.auth.views import login as contrib_login
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from organization.models import *
from organization.forms import *
from django.forms.formsets import formset_factory
import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from wetLab.forms import *
from dryLab.forms import *
from django.apps.registry import apps
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
    template_name = 'customForm.html'
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
        request.session['experimentId'] = pk
        context = {}
        experiment = Experiment.objects.get(pk=pk)
        individual = False
        biosource = False
        treatment = False
        modification = False
        construct = False
        target = False
        genomicRegions = False
        
        if (Biosample.objects.get(expBio__pk=pk)):
            biosample = Biosample.objects.get(expBio__pk=pk)
            if(Biosource.objects.get(bioSource__pk=biosample.pk)):
                biosource = Biosource.objects.get(bioSource__pk=biosample.pk)
                if(Individual.objects.filter(sourceInd__pk=biosource.pk)):
                    individual = Individual.objects.filter(sourceInd__pk=biosource.pk)
        if(str(biosample.biosample_treatment)  != "None"):
            treatmentModel = apps.get_model('wetLab', str(biosample.biosample_treatment))
            print(treatmentModel)
            if(treatmentModel.objects.filter(biosample=biosample.pk)):
                treatment = treatmentModel.objects.filter(biosample=biosample.pk)
        if((Modification.objects.filter(bioMod__pk=biosample.pk))):
            modification = Modification.objects.get(bioMod__pk=biosample.pk)
            if(Construct.objects.filter(modConstructs__pk=modification.pk)):
                construct = Construct.objects.filter(modConstructs__pk=modification.pk)
            if(Target.objects.filter(modTarget__pk=modification.pk)):
                target = Target.objects.filter(modTarget__pk=modification.pk)
            if(GenomicRegions.objects.filter(modGen__pk=modification.pk)):
                genomicRegions =GenomicRegions.objects.filter(modGen__pk=modification.pk)

        for i in individual:
            i.individual_fields = json.loads(i.individual_fields)
        if(biosample.biosample_fields):
            biosample.biosample_fields = json.loads(biosample.biosample_fields)    
           
        context['experiment']= experiment
        context['biosample']= biosample
        context['biosource']= biosource
        context['individuals']= individual
        context['treatments']= treatment
        context['modification']= modification
        context['constructs']= construct
        context['targets']= target
        context['genomicRegions']= genomicRegions
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
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = IndividualForm
    selectForm_class = SelectForm
    
    def get(self,request):
        selectForm = self.selectForm_class()
        selectForm.fields["Individual"].queryset = Individual.objects.filter(userOwner=request.user.pk)
        isExisting = (selectForm.fields["Individual"].queryset.count() > 0)
        existing = selectForm['Individual']
        form = self.form_class()
        form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
        return render(request, self.template_name,{'form':form, 'form_class':"Individual", 'existing':existing,'isExisting':isExisting})
    
    def post(self,request):
        form = self.form_class(request.POST)
        selectForm = self.selectForm_class(request.POST)
        existingSelect = request.POST.get('selectForm')
        if existingSelect == "old":
            request.session['individualPK'] = selectForm['Individual'].value()
            return HttpResponseRedirect('/addBiosource/')
        else:   
            if form.is_valid():
                individual = form.save(commit= False)
                individual_type = request.POST.get('individual_type')
                individual.userOwner = User.objects.get(pk=request.user.pk)
                individual.individual_fields = createJSON(request, individual_type)  
                individual.save()
                request.session['individualPK'] = individual.pk
                print(individual.pk)
                return HttpResponseRedirect('/addBiosource/')
            else:
                existing = selectForm['Individual']
                selectForm.fields["Individual"].queryset = Individual.objects.filter(userOwner=request.user.pk)
                isExisting = (selectForm.fields["Individual"].queryset.count() > 0)
                form.fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
                return render(request, self.template_name,{'form':form, 'form_class':"Individual", 'existing':existing,'isExisting':isExisting})

class AddBiosource(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = BiosourceForm
    selectForm_class = SelectForm
    
    def get(self,request):
        selectForm = self.selectForm_class()
        selectForm.fields["Biosource"].queryset = Biosource.objects.filter(biosource_individual=request.session['individualPK'])
        isExisting = (selectForm.fields["Biosource"].queryset.count() > 0)
        existing = selectForm['Biosource']
        form = self.form_class()
        form.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
        form.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
        return render(request, self.template_name,{'form':form, 'form_class':"Biosource", 'existing':existing,'isExisting':isExisting})
    
    def post(self,request):
        form = self.form_class(request.POST)
        selectForm = self.selectForm_class(request.POST)
        existingSelect = request.POST.get('selectForm')
        if existingSelect == "old":
            request.session['biosourcePK'] =  selectForm['Biosource'].value()
            return HttpResponseRedirect('/addBiosample/')
        else:
            if form.is_valid():
                biosource = form.save(commit=False)
                individualPK = request.session['individualPK']
                biosource.biosource_individual = Individual.objects.get(pk=individualPK)
                biosource.save()
                request.session['biosourcePK'] = biosource.pk
                return HttpResponseRedirect('/addBiosample/')
            else:
                selectForm.fields["Biosource"].queryset = Biosource.objects.filter(biosource_individual=request.session['individualPK'])
                isExisting = (selectForm.fields["Biosource"].queryset.count() > 0)
                existing = selectForm['Biosource']
                form.fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
                form.fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
                return render(request, self.template_name,{'form':form, 'form_class':"Biosource", 'existing':existing,'isExisting':isExisting})

class AddBiosample(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = BiosampleForm
    selectForm_class = SelectForm
    
    def get(self,request):
        selectForm = self.selectForm_class()
        selectForm.fields["Biosample"].queryset = Biosample.objects.filter(biosample_biosource=request.session['biosourcePK'])
        isExisting = (selectForm.fields["Biosample"].queryset.count() > 0)
        existing = selectForm['Biosample']
        form = self.form_class()
        form.fields["biosample_treatment"].queryset = Choice.objects.filter(choice_type="biosample_treatment")
        form.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
        return render(request, self.template_name,{'form':form, 'form_class':"Biosample", 'existing':existing,'isExisting':isExisting})
    
    def post(self,request):
        form = self.form_class(request.POST)
        selectForm = self.selectForm_class(request.POST)
        existingSelect = request.POST.get('selectForm')
        if existingSelect == "old":
            request.session['biosamplePK'] =  selectForm['Biosample'].value()
            return HttpResponseRedirect('/addExperiment/')
        else:
            if form.is_valid():
                biosample = form.save(commit= False)
                biosample.userOwner = User.objects.get(pk=request.user.pk)
                individualPK = request.session['individualPK']
                biosourcePK = request.session['biosourcePK']
                biosample.biosample_biosource = Biosource.objects.get(pk=biosourcePK)
                biosample.biosample_individual = Individual.objects.get(pk=individualPK)
                treatmentModel = str(biosample.biosample_treatment)
                if(request.POST.get('biosample_type')):
                    biosample_type = request.POST.get('biosample_type')
                    biosample.biosample_fields = createJSON(request, biosample_type)
                biosample.save()
                request.session['biosamplePK'] = biosample.pk
                if (treatmentModel == "None"):
                    return HttpResponseRedirect('/addExperiment/')
                else:
                    return HttpResponseRedirect('/add'+treatmentModel)
            else:
                selectForm.fields["Biosample"].queryset = Biosample.objects.filter(biosample_biosource=request.session['biosourcePK'])
                isExisting = (selectForm.fields["Biosample"].queryset.count() > 0)
                existing = selectForm['Biosample']
                form.fields["biosample_treatment"].queryset = Choice.objects.filter(choice_type="biosample_treatment")
                form.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
                return render(request, self.template_name,{'form':form, 'form_class':"Biosample", 'existing':existing,'isExisting':isExisting})


        
class AddExperiment(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = ExperimentForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"Experiment"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.experiment_project = Project.objects.get(pk=request.session['projectId'])
            form.experiment_biosample = Biosample.objects.get(pk=request.session['biosamplePK'])
            form.save()
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"Experiment"})


class AddModification(View): 
    template_name = 'modificationForm.html'
    error_page = 'error.html'
    form_class = ModificationForm
    construct_form=ConstructForm
    regions_form= GenomicRegionsForm
    target_form = TargetForm
    
    def get(self,request):
        form = self.form_class()
        construct_form = self.construct_form()
        regions_form = self.regions_form()
        target_form = self.target_form()
        form.fields["modification_type"].queryset = Choice.objects.filter(choice_type="modification_type")
        construct_form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
        regions_form.fields["genomicRegions_genome_assembly"].queryset = Choice.objects.filter(choice_type="genomicRegions_genome_assembly")
        regions_form.fields["genomicRegions_chromosome"].queryset = Choice.objects.filter(choice_type="genomicRegions_chromosome")
        return render(request, self.template_name,{'form':form, 'construct_form':construct_form,'regions_form':regions_form, 'target_form':target_form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        construct_form =self.construct_form(request.POST)
        regions_form =self.regions_form(request.POST)
        target_form =self.target_form(request.POST)
        if all([form.is_valid(), construct_form.is_valid(),regions_form.is_valid(),target_form.is_valid()]):
            target = target_form.save()
            construct = construct_form.save()
            regions = regions_form.save()
            modification = form.save(commit= False)
            modification.userOwner = User.objects.get(pk=request.user.pk)
            modification.modification_constructs = construct
            modification.modification_genomicRegions = regions
            modification.modification_target = target
            modification.save()
            return HttpResponseRedirect('/addBiosample/')
        else:
            form.fields["modification_type"].queryset = Choice.objects.filter(choice_type="modification_type")
            construct_form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
            regions_form.fields["genomicRegions_genome_assembly"].queryset = Choice.objects.filter(choice_type="genomicRegions_genome_assembly")
            regions_form.fields["genomicRegions_chromosome"].queryset = Choice.objects.filter(choice_type="genomicRegions_chromosome")
            return render(request, self.template_name,{'form':form, 'construct_form':construct_form,'regions_form':regions_form, 'target_form':target_form})

        
class AddConstruct(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = ConstructForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
        return render(request, self.template_name,{'form':form, 'form_class':"Construct"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
            return render(request, self.template_name,{'form':form, 'form_class':"Construct"})


        
class AddTarget(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = TargetForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"Target"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"Target"})



class AddProtocol(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = ProtocolForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["protocol_type"].queryset = JsonObjField.objects.filter(field_type="Protocol")
        return render(request, self.template_name,{'form':form, 'form_class':"Protocol"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            protocol = form.save(commit= False)
            protocol.userOwner = User.objects.get(pk=request.user.pk)
            if(request.POST.get('protocol_type')):
                protocol_type = request.POST.get('protocol_type')
                protocol.biosample_fields = createJSON(request, protocol_type)
            protocol.save()
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["protocol_type"].queryset = JsonObjField.objects.filter(field_type="Protocol")
            return render(request, self.template_name,{'form':form, 'form_class':"Protocol"})

class AddTreatmentRnai(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = TreatmentRnaiForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["treatmentRnai_rnai_type"].queryset = Choice.objects.filter(choice_type="treatmentRnai_rnai_type")
        return render(request, self.template_name,{'form':form, 'form_class':"TreatmentRnai"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            treatment = form.save(commit= False)
            treatment.save()
            biosample = request.POST.getlist('biosample')
            for bioPk in biosample:
                bioSam = Biosample.objects.get(pk=bioPk)
                treatment.biosample.add(bioSam)
            return HttpResponseRedirect('/addExperiment/')
        else:
            form.fields["treatmentRnai_rnai_type"].queryset = Choice.objects.filter(choice_type="treatmentRnai_rnai_type")
            return render(request, self.template_name,{'form':form, 'form_class':"TreatmentRnai"})

class AddTreatmentChemical(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = TreatmentChemicalForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["treatmentChemical_concentration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_concentration_units")
        form.fields["treatmentChemical_duration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_duration_units")
        return render(request, self.template_name,{'form':form, 'form_class':"TreatmentChemical"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            treatment = form.save(commit= False)
            treatment.save()
            biosample = request.POST.getlist('biosample')
            for bioPk in biosample:
                bioSam = Biosample.objects.get(pk=bioPk)
                treatment.biosample.add(bioSam)
            return HttpResponseRedirect('/addExperiment/')
        else:
            form.fields["treatmentChemical_concentration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_concentration_units")
            form.fields["treatmentChemical_duration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_duration_units")
            return render(request, self.template_name,{'form':form, 'form_class':"TreatmentChemical"})
        
class AddOther(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = OtherForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"Others"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            biosample = request.POST.getlist('biosample')
            for bioPk in biosample:
                bioSam = Biosample.objects.get(pk=bioPk)
                form.biosample.add(bioSam)
            return HttpResponseRedirect('/addExperiment/')
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"Others"})



class AddDocument(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = DocumentForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["document_type"].queryset = Choice.objects.filter(choice_type="document_type")
        return render(request, self.template_name,{'form':form, 'form_class':"Document"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            document = form.save(commit= False)
            document.save()
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["document_type"].queryset = Choice.objects.filter(choice_type="document_type")
            return render(request, self.template_name,{'form':form, 'form_class':"Document"})

class AddPublication(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = PublicationForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"Publication"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"Publication"})


class AddSequencingRun(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = SequencingRunForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["run_Experiment"].queryset = Experiment.objects.filter(experiment_project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"SequencingRun"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.run_project = Project.objects.get(pk=request.session['projectId'])
            form.save()
            run_Experiment = request.POST.getlist('run_Experiment')
            for expsPk in run_Experiment:
                exp = Experiment.objects.get(pk=expsPk)
                form.run_Experiment.add(exp)
            request.session['runId'] = form.pk
            addBarcodeRedirect = form.run_Add_Barcode
            return HttpResponseRedirect('/'+addBarcodeRedirect)
        else:
            form.fields["run_Experiment"].queryset = Experiment.objects.filter(experiment_project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"SequencingRun"})

class AddBarcode(View): 
    template_name = 'barcodeForm.html'
    error_page = 'error.html'
    def get(self,request):
        countForms = Experiment.objects.filter(runExp__pk=request.session['runId']).count()
        formset= formset_factory(BarcodeForm,extra=countForms)
        form = formset()
        for f in form:
            f.fields["barcode_name_1"].queryset = Choice.objects.filter(choice_type="barcode")
            f.fields["barcode_name_2"].queryset = Choice.objects.filter(choice_type="barcode")
            f.fields["barcode_exp"].queryset = Experiment.objects.filter(runExp__pk=request.session['runId'])
        return render(request, self.template_name,{'form':form, 'form_class':"Barcode"})
    
    def post(self,request):
        countForms = Experiment.objects.filter(runExp__pk=request.session['runId']).count()
        formset= formset_factory(BarcodeForm,extra=countForms)
        form = formset(request.POST)
        if all([form.is_valid()]):
            for f in form: 
                barcode = f.save(commit=False)
                barcode.barcode_run = SequencingRun.objects.get(pk=request.session['runId'])
                barcode.save()
            return HttpResponseRedirect('/showProject/')
        else:
            for f in form:
                f.fields["barcode_name_1"].queryset = Choice.objects.filter(choice_type="barcode")
                f.fields["barcode_name_2"].queryset = Choice.objects.filter(choice_type="barcode")
                f.fields["barcode_exp"].queryset = Experiment.objects.filter(runExp__pk=request.session['runId'])
            return render(request, self.template_name,{'form':form, 'form_class':"Barcode"})


class AddSeqencingFile(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = SeqencingFileForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"SeqencingFile"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"SeqencingFile"})

        
class AddFileSet(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = FileSetForm
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form, 'form_class':"FileSet"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form, 'form_class':"FileSet"})

class AddAnalysis(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = AnalysisForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["analysis_type"].queryset = JsonObjField.objects.filter(field_type="Analysis")
        return render(request, self.template_name,{'form':form, 'form_class':"Analysis"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            if(request.POST.get('analysis_type')):
                analysis_type = request.POST.get('analysis_type')
                analysis.treatment_fields = createJSON(request, analysis_type)
            return HttpResponseRedirect('/showProject/')
        else:
            form.fields["analysis_type"].queryset = JsonObjField.objects.filter(field_type="Analysis")
            return render(request, self.template_name,{'form':form, 'form_class':"Analysis"})


            
@csrf_exempt                
def constructForm(request):
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get('pk')
        obj = JsonObjField.objects.get(pk=pk)
        return HttpResponse(json.dumps({'field_set': obj.field_set, 'model':obj.field_type}), content_type="application/json")
    else :
        return render_to_response('error.html', locals())
 
    