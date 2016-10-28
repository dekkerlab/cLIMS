from django.db import models
from django.contrib.postgres.fields import JSONField
from organization.models import Choice
from dryLab.models import SequencingRun
from django.contrib.auth.models import User
 
# Create your models here.
class UserOwner (models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE,)
    class Meta:
        abstract = True
    

class Modification(UserOwner):
    modification_name = models.CharField(max_length=50, null=False, default="")
    modification_type = models.ForeignKey('organization.JsonObjField',related_name='modType', on_delete=models.CASCADE,)
    modification_fields = JSONField()
    modification_description = models.CharField(max_length=200,  null=True, blank=True)
     
    def __str__(self):
        return self.modification_name
 
 
class Individual(models.Model):
    individual_name = models.CharField(max_length=50, null=False, default="")
    individual_type = models.ForeignKey('organization.JsonObjField',related_name='indType', on_delete=models.CASCADE,)
    individual_fields = JSONField()
    def __str__(self):
        return self.individual_type 
 
 
class Document(models.Model):
    document_description = models.CharField(max_length=200, null=False, default="")
    document_type = models.ForeignKey('organization.Choice',related_name='docChoice', on_delete=models.CASCADE,)
    document_attachment = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.document_type
 
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100, null=False, default="")
    vendor_description = models.CharField(max_length=100, null=False, default="")
    vendor_url =  models.URLField(max_length=200)
    def __str__(self):
        return self.vendor_name
     
class Enzyme(models.Model):
    enzyme_name = models.CharField(max_length=50, null=False, default="")
    enzyme_recogSeq = models.CharField(max_length=20,  null=True, blank=True)
    enzyme_siteLen =  models.CharField(max_length=20,  null=True, blank=True)
    enzyme_cutPos = models.CharField(max_length=20,  null=True, blank=True)
    enzyme_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,)
    def __str__(self):
        return self.enzyme_name

     
class Protocol(UserOwner):
    protocol_name =  models.CharField(max_length=50, null=False, default="")
    protocol_type = models.ForeignKey('organization.JsonObjField',related_name='proType', on_delete=models.CASCADE,)
    protocol_fields = JSONField()
    protocol_document = models.ForeignKey(Document,related_name='proDoc', on_delete=models.CASCADE,)
    protocol_enzyme = models.ForeignKey(Enzyme,related_name='proEnzyme', on_delete=models.CASCADE,)
    protocol_variation = models.TextField()
    protocol_description = models.CharField(max_length=200,  null=True, blank=True)
    
    def __str__(self):
        return self.protocol_name
 


 
class Biosource(models.Model):
    biosource_name = models.CharField(max_length=50, null=False, default="")
    biosource_type =  models.ForeignKey('organization.Choice',related_name='bioChoice', on_delete=models.CASCADE,)
    biosource_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,)
    biosource_individual = models.ForeignKey(Individual,related_name='docChoice', on_delete=models.CASCADE,)
    biosource_tissue  = models.CharField(max_length=100,  null=True, blank=True)
    biosource_url = models.URLField(max_length=200,  null=True, blank=True)
    biosource_description = models.CharField(max_length=200,  null=True, blank=True)
    def __str__(self):
        return self.biosource_name
 
class Biosample(UserOwner):
    biosample_name = models.CharField(max_length=50, null=False, default="")
    biosample_biosource =  models.ForeignKey(Biosource,related_name='bioSource', on_delete=models.CASCADE,)
    biosample_individual =  models.ForeignKey(Individual,related_name='bioIndi', on_delete=models.CASCADE,)
    biosample_modification =  models.ForeignKey(Modification,related_name='bioMod', on_delete=models.CASCADE,)
    biosample_protocol =  models.ForeignKey(Protocol,related_name='bioMod', on_delete=models.CASCADE,)
    biosample_type =  models.ForeignKey('organization.JsonObjField',related_name='biotype', on_delete=models.CASCADE,  null=True, blank=True)
    biosample_fields = JSONField(  null=True, blank=True)
    biosample_references = models.CharField(max_length=200,  null=True, blank=True)
    biosample_dbxrefs = models.CharField(max_length=200,  null=True, blank=True)
    
    def __str__(self):
        return self.biosample_name
     
     
class Treatment(models.Model):
    treatment_name = models.CharField(max_length=50, null=False, default="")
    treatment_type = models.ForeignKey('organization.JsonObjField',related_name='treatType', on_delete=models.CASCADE,)
    treatment_fields = JSONField()
    treatment_biosample = models.ForeignKey(Biosample,related_name='treatBio', on_delete=models.CASCADE)
    treatment_description = models.CharField(max_length=200,  null=True, blank=True)
    
    def __str__(self):
        return self.treatment_name 
     
class Barcode(models.Model):
    barcode_name_1 = models.ForeignKey('organization.Choice',related_name='barChoice1', on_delete=models.CASCADE)
    barcode_name_2 = models.ForeignKey('organization.Choice',related_name='barChoice2', on_delete=models.CASCADE)
    barcode_run = models.ForeignKey('dryLab.SequencingRun',related_name='barRun', on_delete=models.CASCADE)
    barcode_exp = models.ForeignKey('organization.Experiment',related_name='barRun', on_delete=models.CASCADE)
    
    