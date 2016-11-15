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
    
class DeleteProject(DeleteView):
    model = Project
    template_name = 'delete.html'
    def get_success_url(self):
        return reverse('showProject')

class EditExperiment(UpdateView):
    form_class = ExperimentForm
    model = Experiment
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    
    def get_context_data(self, **kwargs):
        context = super(EditExperiment , self).get_context_data(**kwargs)
        context['action'] = reverse('editProject',
                                kwargs={'pk': self.get_object().id})
        return context    

class DeleteExperiment(DeleteView):
    model = Experiment
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})

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
        context['jsonObj']= json.loads(obj.individual_fields)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    

class DeleteIndividual(DeleteView):
    model = Individual
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})


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

class DeleteBiosource(DeleteView):
    model = Biosource
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})

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
        context['jsonObj']= json.loads(obj.biosample_fields)
        context['form'].fields["biosample_treatment"].queryset = Choice.objects.filter(choice_type="biosample_treatment")
        context['form'].fields["biosample_type"].queryset = JsonObjField.objects.filter(field_type="Biosample")
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    

class DeleteBiosample(DeleteView):
    model = Biosample
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        projectId = self.request.session['projectId']
        return reverse('detailProject', kwargs={'pk': projectId})
    

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

class DeleteTreatmentRnai(DeleteView):
    model = TreatmentRnai
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})


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

class DeleteTreatmentChemical(DeleteView):
    model = TreatmentChemical
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
class EditOther(UpdateView):
    form_class = OtherForm
    model = Other
    template_name = 'customForm.html/'
    
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})
    
    def get_context_data(self, **kwargs):
        context = super(EditOther , self).get_context_data(**kwargs)
        context['action'] = reverse('detailExperiment',
                                kwargs={'pk': self.get_object().id})
        return context    

class DeleteOther(DeleteView):
    model = Other
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})   

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

class DeleteModification(DeleteView):
    model = Modification
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})      

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

class DeleteConstruct(DeleteView):
    model = Construct
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})

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

class DeleteGenomicRegions(DeleteView):
    model = GenomicRegions
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})


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

class DeleteTarget(DeleteView):
    model = Target
    template_name = 'deleteExperiment.html'
    def get_success_url(self):
        experimentId = self.request.session['experimentId']
        return reverse('detailExperiment', kwargs={'pk': experimentId})












    