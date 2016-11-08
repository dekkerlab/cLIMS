'''
Created on Oct 25, 2016

@author: nanda
'''
from django.forms.models import ModelForm
from organization.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('project_owner',)

        
class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        exclude = ('experiment_project','experiment_biosample',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ExperimentForm, self).__init__(*args, **kwargs)

class ExperimentSetForm(ModelForm):
    class Meta:
        model = ExperimentSet
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ExperimentSetForm, self).__init__(*args, **kwargs)

class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(PublicationForm, self).__init__(*args, **kwargs)

class AwardForm(ModelForm):
    class Meta:
        model = Award
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(AwardForm, self).__init__(*args, **kwargs)

class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TagForm, self).__init__(*args, **kwargs)

