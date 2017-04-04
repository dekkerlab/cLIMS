'''
Created on Oct 28, 2016

@author: nanda
'''

from django.forms.models import ModelForm
from wetLab.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from wetLab.wrapper import add_related_field_wrapper, SelectWithPop,\
    MultipleSelectWithPop
from organization.models import Publication
from dryLab.models import ImageObjects

class ModificationForm(ModelForm):
    use_required_attribute = False
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop,required=False)
    
    class Meta:
        model = Modification
        exclude = ('userOwner','constructs','modification_genomicRegions','target','dcic_alias')
        fields = ['modification_name','modification_type','modification_vendor','modification_gRNA','references','document','url','dbxrefs','modification_description']
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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False, label="Construct Map", help_text="Map of the construct - document")
    class Meta:
        model = Construct
        exclude = ('dcic_alias',)
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
        exclude = ('dcic_alias',)
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
    targeted_region = forms.ModelChoiceField(GenomicRegions.objects.all(), widget=SelectWithPop, required=False)
    
    class Meta:
        model = Target
        exclude = ('dcic_alias',)
        fields = ['name','targeted_genes','targeted_region','references','document','url','dbxrefs']
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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    
    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        #add_related_field_wrapper(self, 'documents')
    class Meta:
        model = Individual
        exclude = ('individual_fields','userOwner','dcic_alias')
        fields = ['individual_name','individual_vendor','individual_type','references','document','url','dbxrefs']
    

class SelectForm(forms.Form):
        use_required_attribute = False
        Individual = forms.ModelChoiceField(queryset=Individual.objects.all(), empty_label=None)
        Biosource = forms.ModelChoiceField(queryset=Biosource.objects.all(), empty_label=None)
        Biosample = forms.ModelChoiceField(queryset=Biosample.objects.all(), empty_label=None)

class DocumentForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Document
        exclude = ('dcic_alias',)
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
        exclude = ('protocol_fields','userOwner','dcic_alias',)
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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    protocol = forms.ModelChoiceField(Protocol.objects.all(), widget=SelectWithPop,required=False, label="Biosource SOP cell line", 
                                      help_text='Standard operation protocol for the cell line as determined by 4DN Cells Working Group' )
    modifications = forms.ModelMultipleChoiceField(Modification.objects.all(), widget=MultipleSelectWithPop, required=False,
                                                   help_text='Expression or targeting vectors stably transfected to generate Crispr\'ed or other genomic modification')
    
    
    class Meta:
        model = Biosource
        exclude = ('biosource_individual','dcic_alias',)
        fields = ['biosource_name','biosource_type','biosource_cell_line','biosource_cell_line_tier','protocol','biosource_vendor',
                  'cell_line_termid', 'modifications', 'biosource_tissue','references','document','url','dbxrefs','biosource_description']

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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    modifications = forms.ModelMultipleChoiceField(Modification.objects.all(), widget=MultipleSelectWithPop, required=False)
    protocol= forms.ModelChoiceField(Protocol.objects.all(), widget=SelectWithPop, required=False)
    biosample_TreatmentRnai = forms.ModelMultipleChoiceField(TreatmentRnai.objects.all(), widget=MultipleSelectWithPop, required=False)
    biosample_TreatmentChemical= forms.ModelMultipleChoiceField(TreatmentChemical.objects.all(), widget=MultipleSelectWithPop, required=False)
    biosample_OtherTreatment= forms.ModelMultipleChoiceField(OtherTreatment.objects.all(), widget=MultipleSelectWithPop, required=False)
    imageObjects = forms.ModelMultipleChoiceField (ImageObjects.objects.all(), widget=MultipleSelectWithPop, required=False)
    
    class Meta:
        model = Biosample
        exclude = ('biosample_fields','userOwner','biosample_biosource', 'biosample_individual','dcic_alias',)
        fields = ['biosample_name','modifications','protocol','biosample_TreatmentRnai',
                  'biosample_TreatmentChemical','biosample_OtherTreatment','imageObjects','biosample_type',
                  'references','document','url','dbxrefs','biosample_description']
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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    constructs = forms.ModelChoiceField(Construct.objects.all(), widget=SelectWithPop, required=False)
    treatmentRnai_target = forms.ModelChoiceField(Target.objects.all(), widget=SelectWithPop, required=False)
    
    class Meta:
        model = TreatmentRnai
        exclude = ('userOwner','dcic_alias',)
        fields = ['treatmentRnai_name','treatmentRnai_type','constructs','treatmentRnai_vendor','treatmentRnai_target','treatmentRnai_nucleotide_seq',
                  'references','document','url','dbxrefs','treatmentRnai_description']
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
    document = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    
    class Meta:
        model = TreatmentChemical
        exclude = ('userOwner','dcic_alias',)
        fields = ['treatmentChemical_name','treatmentChemical_chemical','treatmentChemical_concentration','treatmentChemical_concentration_units','treatmentChemical_duration','treatmentChemical_duration_units',
                  'treatmentChemical_temperature','references','document','url','dbxrefs','treatmentChemical_description']
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
    documents = forms.ModelChoiceField(Document.objects.all(), widget=SelectWithPop, required=False)
    references = forms.ModelChoiceField(Publication.objects.all(), widget=SelectWithPop, required=False)
    
    class Meta:
        model = OtherTreatment
        exclude = ('userOwner',)
        fields = ['name','references','documents','url','dbxrefs','description']
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
        exclude = ('',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
 
        self.helper.add_input(Submit('submit', 'Submit'))
        super(BarcodeForm, self).__init__(*args, **kwargs)
        
        