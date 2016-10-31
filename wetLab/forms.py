'''
Created on Oct 28, 2016

@author: nanda
'''

from django.forms.models import ModelForm
from wetLab.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ModificationForm(ModelForm):
    class Meta:
        model = Modification
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ModificationForm, self).__init__(*args, **kwargs)

class IndividualForm(ModelForm):
    class Meta:
        model = Individual
        exclude = ('individual_fields',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(IndividualForm, self).__init__(*args, **kwargs)

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DocumentForm, self).__init__(*args, **kwargs)

class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ProtocolForm, self).__init__(*args, **kwargs)

class BiosourceForm(ModelForm):
    class Meta:
        model = Biosource
        exclude = ('biosource_individual',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(BiosourceForm, self).__init__(*args, **kwargs)

class BiosampleForm(ModelForm):
    class Meta:
        model = Biosample
        exclude = ('biosample_fields','userOwner','biosample_biosource', 'biosample_individual',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(BiosampleForm, self).__init__(*args, **kwargs)

class TreatmentForm(ModelForm):
    class Meta:
        model = Treatment
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TreatmentForm, self).__init__(*args, **kwargs)

class BarcodeForm(ModelForm):
    class Meta:
        model = Barcode
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(BarcodeForm, self).__init__(*args, **kwargs)
        
        