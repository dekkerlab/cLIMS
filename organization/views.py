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
from django.core.exceptions import ValidationError, PermissionDenied
from wetLab.forms import *
from dryLab.forms import *
from django.apps.registry import apps
from _collections import defaultdict, OrderedDict
import tarfile
import os
from cLIMS.base import WORKSPACEPATH
from organization.extractAnalysis import extractHiCAnalysis, extract5CAnalysis
import itertools
import re
from django.utils.html import escape
from django.template.context import RequestContext
from organization.decorators import class_login_required
from django.dispatch.dispatcher import receiver
from django.contrib.auth.signals import user_logged_in
# Create your views here.

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
        if('Member' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "member"
        elif('Collaborator' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "collaborator"
        elif ('Admin' in map(str, request.user.groups.all()) or 'Principal Investigator' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "admin"


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login (request, **kwargs)
        
            
        
@class_login_required
class HomeView(View):
    template_name = 'home.html'
    error_page = 'error.html'
    
    def get(self,request):
        context = {}
        context['currentUserName']= request.user.username
        if('Member' in map(str, request.user.groups.all())):
            request.session['currentGroup'] = "member"
            prj = Project.objects.filter((Q(project_owner=request.user.id) | Q(project_contributor=request.user.id)) , project_active="True").distinct()
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


@class_login_required
class ErrorView(View):
    error_page = 'accessError.html'
    def get(self,request):
        project_owner = User.objects.get(pk=request.session['project_ownerId'])
        context = {}
        context['project_owner']=project_owner
        return render(request, self.error_page, context)
        

@class_login_required 
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
            if(project_contributor):
                for contributor in project_contributor:
                    user = User.objects.get(pk=contributor)
                    result.project_contributor.add(user)
            return HttpResponseRedirect('/showProject/')
        else:
            return render(request, self.template_name,{'form':form})

@class_login_required
class ShowProject(View):
    template_name = 'showProject.html'
    error_page = 'error.html'
    
    def get(self,request):
        userType = request.session['currentGroup']
        userId = request.user.id
        if (userType == "member"):
            obj = Project.objects.filter(Q(project_owner=userId) |  Q(project_contributor=userId)).distinct()
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
    



@class_login_required
class DetailProject(View):
    template_name = 'detailProject.html'
    error_page = 'error.html'
    def get(self,request,pk):
        request.session['projectId'] = pk
        context = {}
        prj = Project.objects.get(pk=pk)
        request.session['project_ownerId']=prj.project_owner.id
    #     units = Lane.objects.filter(project=pk)
    #     files = DeepSeqFile.objects.filter(project=pk)
        experiments = Experiment.objects.filter(project=pk)
        sequencingRuns = SequencingRun.objects.filter(project=pk)
        experimentSets = ExperimentSet.objects.filter(project=pk)
        fileSets = FileSet.objects.filter(project=pk)
        tags = Tag.objects.filter(project=pk)
        
        for run in sequencingRuns:
            run.run_Add_Barcode = run.get_run_Add_Barcode_display()
        context['project']= prj
        context['sequencingRuns']= sequencingRuns
    #     context['files']= files
        context['experiments']= experiments
        context['experimentSets']= experimentSets
        context['fileSets']= fileSets
        context['tags']= tags
        return render(request, self.template_name, context)


@class_login_required
class DetailExperiment(View):
    template_name = 'detailExperiment.html'
    error_page = 'error.html'
    def get(self,request,pk):
        request.session['experimentId'] = pk
        context = {}
        experiment = Experiment.objects.get(pk=pk)
        individual = False
        biosource = False
        treatmentRnai = False
        treatmentChemical = False
        otherTreatment = False
        modification = False
        construct = False
        target = False
        genomicRegions = False
        seqencingFiles = False
        analysis = False
        
        if (Biosample.objects.get(expBio__pk=pk)):
            biosample = Biosample.objects.get(expBio__pk=pk)
            if(Biosource.objects.get(bioSource__pk=biosample.pk)):
                biosource = Biosource.objects.get(bioSource__pk=biosample.pk)
                if(Individual.objects.filter(sourceInd__pk=biosource.pk)):
                    individual = Individual.objects.filter(sourceInd__pk=biosource.pk)
            if(TreatmentRnai.objects.filter(biosamTreatmentRnai=biosample.pk)):
                treatmentRnai = TreatmentRnai.objects.filter(biosamTreatmentRnai=biosample.pk)
            if(TreatmentChemical.objects.filter(biosamTreatmentChemical=biosample.pk)):
                treatmentChemical = TreatmentChemical.objects.filter(biosamTreatmentChemical=biosample.pk)
            if(OtherTreatment.objects.filter(biosamOtherTreatment=biosample.pk)):
                otherTreatment = OtherTreatment.objects.filter(biosamOtherTreatment=biosample.pk)
            
        if((Modification.objects.filter(bioMod__pk=biosample.pk))):
            modification = Modification.objects.get(bioMod__pk=biosample.pk)
            if(Construct.objects.filter(modConstructs__pk=modification.pk)):
                construct = Construct.objects.filter(modConstructs__pk=modification.pk)
            if(Target.objects.filter(modTarget__pk=modification.pk)):
                target = Target.objects.filter(modTarget__pk=modification.pk)
            if(GenomicRegions.objects.filter(modGen__pk=modification.pk)):
                genomicRegions =GenomicRegions.objects.filter(modGen__pk=modification.pk)
        if((SeqencingFile.objects.filter(sequencingFile_exp=pk))):
            seqencingFiles = SeqencingFile.objects.filter(sequencingFile_exp=pk)
        if((Analysis.objects.filter(analysis_exp=pk))):
            analysis = Analysis.objects.filter(analysis_exp=pk)

        for i in individual:
            i.individual_fields = json.loads(i.individual_fields)
        if(biosample.biosample_fields):
            biosample.biosample_fields = json.loads(biosample.biosample_fields)    
           
        context['experiment']= experiment
        context['biosample']= biosample
        context['biosource']= biosource
        context['individuals']= individual
        context['treatmentRnai']= treatmentRnai
        context['treatmentChemical']= treatmentChemical
        context['otherTreatment']= otherTreatment
        context['modification']= modification
        context['constructs']= construct
        context['targets']= target
        context['genomicRegions']= genomicRegions
        context['seqencingFiles']= seqencingFiles
        context['analyses']= analysis
        return render(request, self.template_name, context)

@class_login_required
class DetailSequencingRun(View):
    template_name = 'detailRun.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        sequencingRun = SequencingRun.objects.get(pk=pk)
        barcodes = Barcode.objects.filter(barcode_run=pk)
        sequencingRun.run_Add_Barcode = sequencingRun.get_run_Add_Barcode_display()
        context['sequencingRun']= sequencingRun
        context['barcodes']= barcodes
        print(barcodes)
        return render(request, self.template_name, context)

@class_login_required
class DetailAnalysis(View):
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        analysis = Analysis.objects.get(pk=pk)
        images = Images.objects.filter(image_analysis=pk)
        analysis.analysis_fields = json.loads(analysis.analysis_fields)
        if (str(analysis.analysis_type) == "Hi-C Analysis" ):
            context['object']= analysis
            context['images'] = images
            template_name = 'detailAnalysisHiC.html'
        elif (str(analysis.analysis_type) == "5C Analysis" ):
            context['object']= analysis
            context['images'] = images
            template_name = 'detailAnalysis5C.html'
        
        return render(request, template_name, context)

@class_login_required
class DetailPublication(View):
    template_name = 'detailPublication.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        publication = Publication.objects.get(pk=pk)
        context['publication']= publication
        return render(request, self.template_name, context)

@class_login_required
class DetailProtocol(View):
    template_name = 'detailProtocol.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        protocol = Protocol.objects.get(pk=pk)
        if(protocol.protocol_fields):
            protocol.protocol_fields = json.loads(protocol.protocol_fields) 
            print(protocol.protocol_fields)
        context['protocol']= protocol
        return render(request, self.template_name, context)


@class_login_required
class DetailDocument(View):
    template_name = 'detailDocument.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        document = Document.objects.get(pk=pk)
        context['document']= document
        return render(request, self.template_name, context)


@class_login_required
class DetailEnzyme(View):
    template_name = 'detailEnzyme.html'
    error_page = 'error.html'
    def get(self,request,pk):
        context = {}
        enzyme = Enzyme.objects.get(pk=pk)
        context['enzyme']= enzyme
        return render(request, self.template_name, context)



def createJSON(request, fieldTypePk):
    json_object = JsonObjField.objects.get(pk=fieldTypePk).field_set
    data = {}
    for keys in json_object:
        formVal = request.POST.get(keys)
        data[keys] = formVal
    json_data = json.dumps(data)
    return(json_data)


@class_login_required
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


@class_login_required
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


@class_login_required
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
        
        form.fields["biosample_TreatmentRnai"].queryset = TreatmentRnai.objects.filter(userOwner=request.user.pk)
        form.fields["biosample_TreatmentChemical"].queryset = TreatmentChemical.objects.filter(userOwner=request.user.pk)
        form.fields["biosample_OtherTreatment"].queryset = OtherTreatment.objects.filter(userOwner=request.user.pk)
        form.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
        form.fields["imageObjects"].queryset = ImageObjects.objects.filter(project=request.session['projectId'])
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
                if(request.POST.get('biosample_type')):
                    biosample_type = request.POST.get('biosample_type')
                    biosample.biosample_fields = createJSON(request, biosample_type)
                biosample.save()
                request.session['biosamplePK'] = biosample.pk
                return HttpResponseRedirect('/addExperiment/')
            else:
                selectForm.fields["Biosample"].queryset = Biosample.objects.filter(biosample_biosource=request.session['biosourcePK'])
                isExisting = (selectForm.fields["Biosample"].queryset.count() > 0)
                existing = selectForm['Biosample']
                form.fields["biosample_TreatmentRnai"].queryset = TreatmentRnai.objects.filter(userOwner=request.user.pk)
                form.fields["biosample_TreatmentChemical"].queryset = TreatmentChemical.objects.filter(userOwner=request.user.pk)
                form.fields["biosample_OtherTreatment"].queryset = OtherTreatment.objects.filter(userOwner=request.user.pk)
                form.fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
                form.fields["imageObjects"].queryset = ImageObjects.objects.filter(project=request.session['projectId'])
                return render(request, self.template_name,{'form':form, 'form_class':"Biosample", 'existing':existing,'isExisting':isExisting})


@class_login_required        
class AddExperiment(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = ExperimentForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["imageObjects"].queryset = ImageObjects.objects.filter(project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"Experiment"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.project = Project.objects.get(pk=request.session['projectId'])
            form.experiment_biosample = Biosample.objects.get(pk=request.session['biosamplePK'])
            form.save()
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            form.fields["imageObjects"].queryset = ImageObjects.objects.filter(project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"Experiment"})


@class_login_required
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
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(modification._get_pk_val()), escape(modification)))
        else:
            form.fields["modification_type"].queryset = Choice.objects.filter(choice_type="modification_type")
            construct_form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
            regions_form.fields["genomicRegions_genome_assembly"].queryset = Choice.objects.filter(choice_type="genomicRegions_genome_assembly")
            regions_form.fields["genomicRegions_chromosome"].queryset = Choice.objects.filter(choice_type="genomicRegions_chromosome")
            return render(request, self.template_name,{'form':form, 'construct_form':construct_form,'regions_form':regions_form, 'target_form':target_form})

@class_login_required        
class AddConstruct(View): 
    form_class = ConstructForm
    field = "Construct"
    def get(self,request):
        form = self.form_class()
        form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save()
            
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
 
        else:
            form.fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)


@class_login_required        
class AddTarget(View): 
    form_class = TargetForm
    field = "Target"
    def get(self,request):
        form = self.form_class()
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save()
            
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)


@class_login_required
class AddProtocol(View): 
    form_class = ProtocolForm
    field = "Protocol"
    def get(self,request):
        form = self.form_class()
        form.fields["type"].queryset = JsonObjField.objects.filter(field_type="Protocol")
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save(commit= False)
                newObject.userOwner = User.objects.get(pk=request.user.pk)
                if(request.POST.get('type')):
                    protocol_type = request.POST.get('type')
                    newObject.protocol_fields = createJSON(request, protocol_type)
                newObject.save()
           
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            form.fields["type"].queryset = JsonObjField.objects.filter(field_type="Protocol")
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)

@class_login_required        
class AddTreatmentRnai(View): 
    form_class = TreatmentRnaiForm
    field = "TreatmentRNAi"
    def get(self,request):
        form = self.form_class()
        form.fields["treatmentRnai_rnai_type"].queryset = Choice.objects.filter(choice_type="treatmentRnai_rnai_type")
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save(commit= False)
                newObject.userOwner = User.objects.get(pk=request.user.pk)
                newObject.save()
           
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))

        else:
            form.fields["treatmentRnai_rnai_type"].queryset = Choice.objects.filter(choice_type="treatmentRnai_rnai_type")
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)

@class_login_required        
class AddTreatmentChemical(View): 
    form_class = TreatmentChemicalForm
    field = "TreatmentChemical"
    def get(self,request):
        form = self.form_class()
        form.fields["treatmentChemical_concentration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_concentration_units")
        form.fields["treatmentChemical_duration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_duration_units")
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save(commit= False)
                newObject.userOwner = User.objects.get(pk=request.user.pk)
                newObject.save()
            
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            form.fields["treatmentChemical_concentration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_concentration_units")
            form.fields["treatmentChemical_duration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_duration_units")
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)

@class_login_required        
class AddOther(View): 
    form_class = OtherForm
    field = "OtherTreatment"
    def get(self,request):
        form = self.form_class()
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save()
                
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)
        

@class_login_required
class AddDocument(View): 
    form_class = DocumentForm
    field = "Document"
    def get(self,request):
        form = self.form_class()
        form.fields["type"].queryset = Choice.objects.filter(choice_type="document_type")
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
     
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save()
                
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            form.fields["type"].queryset = Choice.objects.filter(choice_type="document_type")
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)
        

@class_login_required
class AddPublication(View): 
    form_class = PublicationForm
    field = "Publication"
    def get(self,request):
        form = self.form_class()
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save()
                
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))
        else:
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)

@class_login_required
class AddSequencingRun(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = SequencingRunForm
    
    def get(self,request):
       
        form = self.form_class()
        form.fields["run_Experiment"].queryset = Experiment.objects.filter(project=request.session['projectId'])
        form.fields["run_sequencing_platform"].queryset = Choice.objects.filter(choice_type="run_sequencing_platform")
        form.fields["run_sequencing_center"].queryset = Choice.objects.filter(choice_type="run_sequencing_center")
        return render(request, self.template_name,{'form':form, 'form_class':"SequencingRun"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.project = Project.objects.get(pk=request.session['projectId'])
            form.save()
            run_Experiment = request.POST.getlist('run_Experiment')
            for expsPk in run_Experiment:
                exp = Experiment.objects.get(pk=expsPk)
                form.run_Experiment.add(exp)
            request.session['runId'] = form.pk
            addBarcodeRedirect = form.run_Add_Barcode
            if(addBarcodeRedirect == "addBarcode"):
                return HttpResponseRedirect('/'+ addBarcodeRedirect)
            elif(addBarcodeRedirect == "detailProject"):
                return HttpResponseRedirect('/'+ addBarcodeRedirect +'/'+request.session['projectId'])
            else:
                return render(request, self.error_page, {})
        else:
            form.fields["run_Experiment"].queryset = Experiment.objects.filter(project=request.session['projectId'])
            form.fields["run_sequencing_platform"].queryset = Choice.objects.filter(choice_type="run_sequencing_platform")
            form.fields["run_sequencing_center"].queryset = Choice.objects.filter(choice_type="run_sequencing_center")
            return render(request, self.template_name,{'form':form, 'form_class':"SequencingRun"})

@class_login_required
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
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            for f in form:
                f.fields["barcode_name_1"].queryset = Choice.objects.filter(choice_type="barcode")
                f.fields["barcode_name_2"].queryset = Choice.objects.filter(choice_type="barcode")
                f.fields["barcode_exp"].queryset = Experiment.objects.filter(runExp__pk=request.session['runId'])
            return render(request, self.template_name,{'form':form, 'form_class':"Barcode"})

@class_login_required
class AddSeqencingFile(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = SeqencingFileForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["sequencingFile_run"].queryset = SequencingRun.objects.filter(project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"SeqencingFile"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = Project.objects.get(pk=request.session['projectId'])
            file.sequencingFile_backupPath = "/s4s/" + file.sequencingFile_mainPath
            file.sequencingFile_sha256sum = "diuwdiued788798"
            file.sequencingFile_md5sum = "hewifu9283ydhjhkj"
            file.sequencingFile_exp = Experiment.objects.get(pk = self.request.session['experimentId'] )
            file.save()
            return HttpResponseRedirect('/detailExperiment/'+self.request.session['experimentId'])
        else:
            form.fields["sequencingFile_run"].queryset = SequencingRun.objects.filter(project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"SeqencingFile"})

@class_login_required        
class AddFileSet(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = FileSetForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["fileset_type"].queryset = Choice.objects.filter(choice_type="fileset_type")
        form.fields["fileSet_file"].queryset = SeqencingFile.objects.filter(project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"FileSet"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            fileset = form.save(commit=False)
            fileset.project = Project.objects.get(pk=request.session['projectId'])
            fileset.save()
            fileSetFile = request.POST.getlist('fileSet_file')
            for file in fileSetFile:
                f = SeqencingFile.objects.get(pk=file)
                fileset.fileSet_file.add(f)
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            form.fields["fileset_type"].queryset = Choice.objects.filter(choice_type="fileset_type")
            form.fields["fileSet_file"].queryset = SeqencingFile.objects.filter(project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"FileSet"})

@class_login_required        
class AddExperimentSet(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = ExperimentSetForm
    
    def get(self,request):
        form = self.form_class()  
        form.fields["experimentSet_type"].queryset = Choice.objects.filter(choice_type="experimentSet_type")
        form.fields["experimentSet_exp"].queryset = Experiment.objects.filter(project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"ExperimentSet"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            expSet = form.save(commit=False)
            expSet.project = Project.objects.get(pk=request.session['projectId'])
            expSet.save()
            expSetExp = request.POST.getlist('experimentSet_exp')
            for exp in expSetExp:
                e = Experiment.objects.get(pk=exp)
                expSet.experimentSet_exp.add(e)
                
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            form.fields["experimentSet_type"].queryset = Choice.objects.filter(choice_type="experimentSet_type")
            form.fields["experimentSet_exp"].queryset = Experiment.objects.filter(project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"ExperimentSet"})

@class_login_required
class AddTag(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'   
    form_class = TagForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["tag_exp"].queryset = Experiment.objects.filter(project=request.session['projectId'])
        return render(request, self.template_name,{'form':form, 'form_class':"Tag"})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.tag_user = User.objects.get(pk=request.user.id)
            tag.project = Project.objects.get(pk=request.session['projectId'])
            tag.save()
            tagExp = request.POST.getlist('tag_exp')
            for exp in tagExp:
                e = Experiment.objects.get(pk=exp)
                tag.tag_exp.add(e)
                
            return HttpResponseRedirect('/detailProject/'+request.session['projectId'])
        else:
            form.fields["tag_exp"].queryset = Experiment.objects.filter(project=request.session['projectId'])
            return render(request, self.template_name,{'form':form, 'form_class':"Tag"})

@class_login_required
class AddImageObjects(View): 
    form_class = ImageObjectsForm
    field = "Images"
    def get(self,request):
        form = self.form_class()
        pageContext = {'form': form, 'field':self.field}
        return render(request, "popup.html", pageContext)
    
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            newObject = None
            try:
                newObject = form.save(commit=False)
                newObject.project = Project.objects.get(pk=request.session['projectId'])
                newObject.save()
            except(forms.ValidationError):
                newObject = None
                
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %(escape(newObject._get_pk_val()), escape(newObject)))

        else:
            pageContext = {'form': form, 'field':self.field}
            return render(request, "popup.html", pageContext)


def log_file(members):
    for tarinfo in members:
        fileExtension = os.path.splitext(tarinfo.name)[0]
        if ((fileExtension.split('.', 1))[-1] == "end.mappingLog" ):
            return tarinfo

def png_files(members, analysisPk):
    for tarinfo in members:
        if (os.path.splitext(tarinfo.name)[1] == ".png"):
            print(WORKSPACEPATH+"media/"+ tarinfo.name)
            Images.objects.create(image_path="/media/"+ tarinfo.name,image_analysis=Analysis.objects.get(pk=analysisPk) )
            yield tarinfo

def importAnalysisGZ(analysis, analysisTypePk):
    analysisTarGz = str(analysis.analysis_import)
    analysisPk = analysis.pk
    tar = tarfile.open(WORKSPACEPATH+"media/"+analysisTarGz, "r|gz")
    logFile = tar.extractfile(log_file(tar))
    content = logFile.read()
    analysisType = JsonObjField.objects.get(pk = analysisTypePk).field_name
    if(analysisType == "Hi-C Analysis"):
        json_data = extractHiCAnalysis(content, analysisTypePk)
    elif(analysisType == "5C Analysis"):
        json_data = extract5CAnalysis(content, analysisTypePk)
    tar.extractall(path=WORKSPACEPATH+"media/", members=png_files(tar, analysisPk))
    tar.close()
    os.remove(WORKSPACEPATH+"media/"+analysisTarGz)
    return json_data

@class_login_required
class AddAnalysis(View): 
    template_name = 'customForm.html'
    error_page = 'error.html'
    form_class = AnalysisForm
    
    def get(self,request):
        form = self.form_class()
        form.fields["analysis_type"].queryset = JsonObjField.objects.filter(field_type="Analysis")
        form.fields["analysis_file"].queryset = SeqencingFile.objects.filter(sequencingFile_exp=self.request.session['experimentId'] )
        return render(request, self.template_name,{'form':form, 'form_class':"Analysis"})
    
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis_type = request.POST.get('analysis_type')
            analysis.analysis_exp = Experiment.objects.get(pk = self.request.session['experimentId'] )
            analysis.save()
            analysis_file = request.POST.getlist('analysis_file')
            for files in analysis_file:
                file = SeqencingFile.objects.get(pk=files)
                analysis.analysis_file.add(file)
            json_data = importAnalysisGZ(analysis, analysis_type)
            analysis.analysis_import.delete()
            analysis.analysis_fields = json_data
            analysis.save()
            
            #analysis.analysis_fields = createJSON(request, analysis_type)
            return HttpResponseRedirect('/detailExperiment/'+self.request.session['experimentId'])
        else:
            form.fields["analysis_type"].queryset = JsonObjField.objects.filter(field_type="Analysis")
            form.fields["analysis_file"].queryset = SeqencingFile.objects.filter(sequencingFile_exp=self.request.session['experimentId'] )
            return render(request, self.template_name,{'form':form, 'form_class':"Analysis"})

            
@csrf_exempt                
def constructForm(request):
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get('pk')
        obj = JsonObjField.objects.get(pk=pk)
        return HttpResponse(json.dumps({'field_set': obj.field_set, 'model':obj.field_type}), content_type="application/json")
    else :
        return render_to_response('error.html', locals())
 

@login_required
def submitSequencingRun(request,pk):
    check= False
    projectId = request.session['projectId']
    if('Member' in map(str, request.user.groups.all())):
        user=User.objects.get(pk=request.user.id)
        projectObj = Project.objects.get(pk=projectId)
        prjOwner = projectObj.project_owner
        print(user)
        print(prjOwner)
        if(user ==  prjOwner):
            check = True
            print("User==Owner true")
        
    if ('Admin' in map(str, request.user.groups.all()) or 'Principal Investigator' in map(str, request.user.groups.all())):
        check = True
        print("Admin/PI")
        
    if (check== True):
        obj = SequencingRun.objects.get(pk=pk)
        obj.run_submitted=True
        obj.save()
        return HttpResponseRedirect('/detailProject/'+projectId)
    else:
        raise  PermissionDenied

@login_required
def approveSequencingRun(request,pk):
    obj = SequencingRun.objects.get(pk=pk)
    obj.run_approved=True
    obj.save()
    return redirect("/sequencingRunView")

@class_login_required
class SequencingRunView(View):
    template_name = 'sequencingRuns.html'
    
    def get(self,request):
        sequencingRuns = SequencingRun.objects.all().order_by('-run_submission_date')
        d = defaultdict(list)
        for run in sequencingRuns:
            run.run_Add_Barcode = run.get_run_Add_Barcode_display()
            d[run.project.project_name].append(run)
        context = {
            'sequencingRuns': OrderedDict(d),
        }
        return render(request, self.template_name, context)
    

@login_required
def searchView(request):
    context ={}
    if request.GET:
        for searchModelForm in [ProjectSearchForm,ExperimentSearchForm,SequencingRunSearchForm,SeqencingFileSearchForm]:
            form = searchModelForm(request.GET,request=request )
            if form.is_valid():
                results = form.get_result_queryset()
            else:
                results = []
            if ((results) and (searchModelForm == ProjectSearchForm)):
                context['projects']=results
            elif ((results) and (searchModelForm == ExperimentSearchForm)):
                context['experiments']=results
            elif ((results) and (searchModelForm == SequencingRunSearchForm)):
                context['runs']=results
            elif ((results) and (searchModelForm == SeqencingFileSearchForm)):
                context['files']=results
        if not bool(context):
            context['results']="No result"
    return render(request, 'searchResult.html', context)
