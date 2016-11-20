'''
Created on Oct 25, 2016

@author: nanda
'''
from django.forms.models import ModelForm
from organization.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from organization.simple_search import BaseSearchForm

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('project_owner',)

class ProjectSearchForm(BaseSearchForm):
    formName = 'ProjectSearchForm'
    class Meta:
        base_qs = Project.objects
        search_fields = ('project_name', 'project_notes',) 

        # assumes a fulltext index has been defined on the fields
        # 'name,description,specifications,id'
        fulltext_indexes = (
            ('experiment_name', 2), # name matches are weighted higher
            ('experiment_name,experiment_description', 1),
        )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProjectSearchForm, self).__init__(*args, **kwargs)

        
class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        exclude = ('project','experiment_biosample',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ExperimentForm, self).__init__(*args, **kwargs)

class ExperimentSearchForm(BaseSearchForm):
    formName = 'ExperimentSearchForm'
    class Meta:
        base_qs = Experiment.objects
        search_fields = ('experiment_name', 'experiment_description',) 

        # assumes a fulltext index has been defined on the fields
        # 'name,description,specifications,id'
        fulltext_indexes = (
            ('experiment_name', 2), # name matches are weighted higher
            ('experiment_name,experiment_description', 1),
        )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ExperimentSearchForm, self).__init__(*args, **kwargs)

class ExperimentSetForm(ModelForm):
    class Meta:
        model = ExperimentSet
        exclude = ('project',)
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
        exclude = ('tag_user','project',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TagForm, self).__init__(*args, **kwargs)

