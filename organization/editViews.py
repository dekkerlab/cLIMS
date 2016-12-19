'''
Created on Nov 10, 2016

@author: nanda
'''
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse
from organization.models import *
from wetLab.forms import *
from dryLab.forms import *
from organization.forms import *
import json
from organization.decorators import *
from django.utils.decorators import method_decorator


class EditProject(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.kwargs.get(self.pk_url_kwarg, None)
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditProject , self).get_context_data(**kwargs)
        context['action'] = reverse('editProject',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    
class DeleteProject(DeleteView):
    model = Project
    template_name = 'delete.html'
    def get_success_url(self):
        return reverse('showProject')
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class EditExperiment(UpdateView):
    form_class = ExperimentForm
    model = Experiment
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditExperiment , self).get_context_data(**kwargs)
        context['action'] = reverse('editProject',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteExperiment(DeleteView):
    model = Experiment
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

def createJSON(request, fieldTypePk):
    json_object = JsonObjField.objects.get(pk=fieldTypePk).field_set
    data = {}
    for keys in json_object:
        formVal = request.POST.get(keys)
        data[keys] = formVal
    json_data = json.dumps(data)
    return(json_data)

class EditIndividual(UpdateView):
    form_class = IndividualForm
    model = Individual
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        individual = Individual.objects.get(pk=self.get_object().id)
        individual_type = self.request.POST.get('individual_type')
        individual.individual_fields = createJSON(self.request, individual_type)
        individual.save()
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditIndividual , self).get_context_data(**kwargs)
        context['form'].fields["individual_type"].queryset = JsonObjField.objects.filter(field_type="Individual")
        obj = Individual.objects.get(pk=self.get_object().id)
        if (obj.individual_fields):
            context['jsonObj']= json.loads(obj.individual_fields)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteIndividual(DeleteView):
    model = Individual
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditBiosource(UpdateView):
    form_class = BiosourceForm
    model = Biosource
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditBiosource , self).get_context_data(**kwargs)
        context['form'].fields["biosource_type"].queryset = Choice.objects.filter(choice_type="biosource_type")
        context['form'].fields["biosource_cell_line_tier"].queryset = Choice.objects.filter(choice_type="biosource_cell_line_tier")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteBiosource(DeleteView):
    model = Biosource
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class EditBiosample(UpdateView):
    form_class = BiosampleForm
    model = Biosample
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        biosample = Biosample.objects.get(pk=self.get_object().id)
        if(self.request.POST.get('biosample_type')):
            biosample_type = self.request.POST.get('biosample_type')
            biosample.biosample_fields = createJSON(self.request, biosample_type)
            biosample.save()
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    
    def get_context_data(self, **kwargs):
        context = super(EditBiosample , self).get_context_data(**kwargs)
        obj = Biosample.objects.get(pk=self.get_object().id)
        if(obj.biosample_fields):
            context['jsonObj']= json.loads(obj.biosample_fields)
        context['form'].fields["biosample_treatment"].queryset = Choice.objects.filter(choice_type="biosample_treatment")
        context['form'].fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
        context['form'].fields["biosample_imageObjects"].queryset = ImageObjects.objects.filter(project=self.request.session['projectId'])
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    
    

class DeleteBiosample(DeleteView):
    model = Biosample
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class EditTreatmentRnai(UpdateView):
    form_class = TreatmentRnaiForm
    model = TreatmentRnai
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditTreatmentRnai , self).get_context_data(**kwargs)
        context['form'].fields["treatmentRnai_rnai_type"].queryset = Choice.objects.filter(choice_type="treatmentRnai_rnai_type")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteTreatmentRnai(DeleteView):
    model = TreatmentRnai
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditTreatmentChemical(UpdateView):
    form_class = TreatmentChemicalForm
    model = TreatmentChemical
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditTreatmentChemical , self).get_context_data(**kwargs)
        context['form'].fields["treatmentChemical_concentration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_concentration_units")
        context['form'].fields["treatmentChemical_duration_units"].queryset = Choice.objects.filter(choice_type="treatmentChemical_duration_units")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteTreatmentChemical(DeleteView):
    model = TreatmentChemical
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    
    
class EditOther(UpdateView):
    form_class = OtherForm
    model = OtherTreatment
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditOther , self).get_context_data(**kwargs)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
     

class DeleteOther(DeleteView):
    model = OtherTreatment
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class EditModification(UpdateView):
    form_class = ModificationForm
    model = Modification
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditModification , self).get_context_data(**kwargs)
        context['form'].fields["modification_type"].queryset = Choice.objects.filter(choice_type="modification_type")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteModification(DeleteView):
    model = Modification
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)      

class EditConstruct(UpdateView):
    form_class = ConstructForm
    model = Construct
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditConstruct , self).get_context_data(**kwargs)
        context['form'].fields["construct_type"].queryset = Choice.objects.filter(choice_type="construct_type")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)  

class DeleteConstruct(DeleteView):
    model = Construct
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class EditGenomicRegions(UpdateView):
    form_class = GenomicRegionsForm
    model = GenomicRegions
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditGenomicRegions , self).get_context_data(**kwargs)
        context['form'].fields["genomicRegions_genome_assembly"].queryset = Choice.objects.filter(choice_type="genomicRegions_genome_assembly")
        context['form'].fields["genomicRegions_chromosome"].queryset = Choice.objects.filter(choice_type="genomicRegions_chromosome")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)    

class DeleteGenomicRegions(DeleteView):
    model = GenomicRegions
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditTarget(UpdateView):
    form_class = TargetForm
    model = Target
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditTarget , self).get_context_data(**kwargs)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteTarget(DeleteView):
    model = Target
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditSequencingRun(UpdateView):
    form_class = SequencingRunForm
    model = SequencingRun
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditSequencingRun , self).get_context_data(**kwargs)
        context['form'].fields["run_Experiment"].queryset = Experiment.objects.filter(project=self.request.session['projectId'])
        context['form'].fields["run_sequencing_platform"].queryset = Choice.objects.filter(choice_type="run_sequencing_platform")
        context['form'].fields["run_sequencing_center"].queryset = Choice.objects.filter(choice_type="run_sequencing_center")
        context['action'] = reverse('detailProject',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteSequencingRun(DeleteView):
    model = SequencingRun
    template_name = 'delete.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditSequencingFile(UpdateView):
    form_class = SeqencingFileForm
    model = SeqencingFile
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditSequencingFile , self).get_context_data(**kwargs)
        context['form'].fields["sequencingFile_run"].queryset = SequencingRun.objects.filter(project=self.request.session['projectId'])
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteSequencingFile(DeleteView):
    model = SeqencingFile
    template_name = 'delete.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    


class EditAnalysis(UpdateView):
    form_class = AnalysisForm
    model = Analysis
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        analysis = Analysis.objects.get(pk=self.get_object().id)
        analysis_type = self.request.POST.get('analysis_type')
        analysis.analysis_fields = createJSON(self.request, analysis_type)
        analysis.save()
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditAnalysis , self).get_context_data(**kwargs)
        context['form'].fields["analysis_type"].queryset = JsonObjField.objects.filter(field_type="Analysis")
        context['form'].fields["analysis_file"].queryset = SeqencingFile.objects.filter(sequencingFile_exp=self.request.session['experimentId'] )
        obj = Analysis.objects.get(pk=self.get_object().id)
        if(obj.analysis_fields):
            context['jsonObj']= json.loads(obj.analysis_fields)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    
    

class DeleteAnalysis(DeleteView):
    model = Analysis
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)


class EditTag(UpdateView):
    form_class = TagForm
    model = Tag
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditTag , self).get_context_data(**kwargs)
        context['form'].fields["tag_exp"].queryset = Experiment.objects.filter(project=self.request.session['projectId'])
        context['action'] = reverse('detailProject',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteTag(DeleteView):
    model = Tag
    template_name = 'delete.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class EditExperimentSet(UpdateView):
    form_class = ExperimentSetForm
    model = ExperimentSet
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditExperimentSet , self).get_context_data(**kwargs)
        context['form'].fields["experimentSet_type"].queryset = Choice.objects.filter(choice_type="experimentSet_type")
        context['form'].fields["experimentSet_exp"].queryset = Experiment.objects.filter(project=self.request.session['projectId'])
        context['action'] = reverse('detailProject',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
      

class DeleteExperimentSet(DeleteView):
    model = ExperimentSet
    template_name = 'delete.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})

class EditFileSet(UpdateView):
    form_class = FileSetForm
    model = FileSet
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditFileSet , self).get_context_data(**kwargs)
        context['form'].fields["fileset_type"].queryset = Choice.objects.filter(choice_type="fileset_type")
        context['form'].fields["fileSet_file"].queryset = SeqencingFile.objects.filter(project=self.request.session['projectId'])
        context['action'] = reverse('detailProject',
                                kwargs={'pk': self.get_object().id})
        return context  
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)  

class DeleteFileSet(DeleteView):
    model = FileSet
    template_name = 'delete.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})


class EditProtocol(UpdateView):
    form_class = ProtocolForm
    model = Protocol
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        protocol = Protocol.objects.get(pk=self.get_object().id)
        if(self.request.POST.get('protocol_type')):
            protocol_type = self.request.POST.get('protocol_type')
            protocol.protocol_fields = createJSON(self.request, protocol_type)
            protocol.save()
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditProtocol , self).get_context_data(**kwargs)
        obj = Protocol.objects.get(pk=self.get_object().id)
        if(obj.protocol_fields):
            context['jsonObj']= json.loads(obj.protocol_fields)
        print(json.loads(obj.protocol_fields))
        context['form'].fields["protocol_type"].queryset = JsonObjField.objects.filter(field_type="Protocol")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context  
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
      

class DeleteProtocol(DeleteView):
    model = Protocol
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class EditDocument(UpdateView):
    form_class = DocumentForm
    model = Document
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditDocument , self).get_context_data(**kwargs)
        context['form'].fields["document_type"].queryset = Choice.objects.filter(choice_type="document_type")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class DeleteDocument(DeleteView):
    model = Document
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)

class EditPublication(UpdateView):
    form_class = PublicationForm
    model = Publication
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditPublication , self).get_context_data(**kwargs)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeletePublication(DeleteView):
    model = Publication
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})

class EditImageObjects(UpdateView):
    form_class = ImageObjectsForm
    model = ImageObjects
    template_name = 'editForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditImageObjects , self).get_context_data(**kwargs)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    

class DeleteImageObjects(DeleteView):
    model = ImageObjects
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    @method_decorator(require_permission)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,  *args, **kwargs)
    
    
    













    