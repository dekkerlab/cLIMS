'''
Created on Oct 31, 2016

@author: nanda
'''
from django.forms.models import ModelForm
from dryLab.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.admin import widgets
from django import forms

class SequencingRunForm(ModelForm):
    class Meta:
        model = SequencingRun
        exclude = ('run_project','run_approved','run_submitted')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(SequencingRunForm, self).__init__(*args, **kwargs)
        self.fields['run_submission_date'].widget = widgets.AdminDateWidget()
        self.fields['run_retrieval_date'].widget = widgets.AdminDateWidget()

class SeqencingFileForm(ModelForm):
    class Meta:
        model = SeqencingFile
        exclude = ('sequencingFile_backupPath','sequencingFile_sha256sum','sequencingFile_md5sum','sequencingFile_exp',)
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
        exclude = ('',)
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
        exclude = ('analysis_exp','analysis_fields')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(AnalysisForm, self).__init__(*args, **kwargs)

        

