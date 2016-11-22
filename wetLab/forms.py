'''
Created on Oct 28, 2016

@author: nanda
'''

from django.forms.models import ModelForm
from wetLab.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

class ModificationForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Modification
        exclude = ('userOwner','modification_constructs','modification_genomicRegions','modification_target')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ModificationForm, self).__init__(*args, **kwargs)

class ConstructForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Construct
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ConstructForm, self).__init__(*args, **kwargs)

class GenomicRegionsForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = GenomicRegions
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(GenomicRegionsForm, self).__init__(*args, **kwargs)

class TargetForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Target
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TargetForm, self).__init__(*args, **kwargs)

class IndividualForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Individual
        exclude = ('individual_fields','userOwner')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(IndividualForm, self).__init__(*args, **kwargs)

class SelectForm(forms.Form):
        use_required_attribute = False
        Individual = forms.ModelChoiceField(queryset=Individual.objects.all(), empty_label=None)
        Biosource = forms.ModelChoiceField(queryset=Biosource.objects.all(), empty_label=None)
        Biosample = forms.ModelChoiceField(queryset=Biosample.objects.all(), empty_label=None)

class DocumentForm(ModelForm):
    use_required_attribute = False
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
    use_required_attribute = False
    class Meta:
        model = Protocol
        exclude = ('protocol_fields','userOwner')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ProtocolForm, self).__init__(*args, **kwargs)

class BiosourceForm(ModelForm):
    use_required_attribute = False
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
    use_required_attribute = False
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
 
class TreatmentRnaiForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = TreatmentRnai
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
  
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TreatmentRnaiForm, self).__init__(*args, **kwargs)

class TreatmentChemicalForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = TreatmentChemical
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
  
        self.helper.add_input(Submit('submit', 'Submit'))
        super(TreatmentChemicalForm, self).__init__(*args, **kwargs)

class OtherForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Other
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
  
        self.helper.add_input(Submit('submit', 'Submit'))
        super(OtherForm, self).__init__(*args, **kwargs)

class BarcodeForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Barcode
        exclude = ('barcode_run',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(BarcodeForm, self).__init__(*args, **kwargs)
        
        