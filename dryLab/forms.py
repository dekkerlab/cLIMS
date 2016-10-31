'''
Created on Oct 31, 2016

@author: nanda
'''
from django.forms.models import ModelForm
from dryLab.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SequencingRunForm(ModelForm):
    class Meta:
        model = SequencingRun
        exclude = ('project_owner',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(SequencingRunForm, self).__init__(*args, **kwargs)

class SeqencingFileForm(ModelForm):
    class Meta:
        model = SeqencingFile
        exclude = ('project_owner',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(SeqencingFileForm, self).__init__(*args, **kwargs)

class FileSetForm(ModelForm):
    class Meta:
        model = FileSet
        exclude = ('project_owner',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(FileSetForm, self).__init__(*args, **kwargs)

class AnalysisForm(ModelForm):
    class Meta:
        model = Analysis
        exclude = ('project_owner',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(AnalysisForm, self).__init__(*args, **kwargs)
        
        

