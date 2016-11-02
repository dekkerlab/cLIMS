from django.db import models
from django.contrib.postgres.fields import JSONField
from dryLab.models import SequencingRun
from django.contrib.auth.models import User
from django.contrib.admin.utils import help_text_for_field
 
# Create your models here.
class UserOwner (models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE,)
    class Meta:
        abstract = True

class Document(models.Model):
    document_description = models.CharField(max_length=200, null=False, default="")
    document_type = models.ForeignKey('organization.Choice',related_name='docChoice',on_delete=models.CASCADE, help_text="The category that best describes the document.")
    document_attachment = models.FileField(upload_to='uploads/')
    document_references = models.ForeignKey('organization.Publication', null=True, blank=True, on_delete=models.CASCADE, help_text="The publications that provide more information about the object.")
    document_url = models.URLField(max_length=200,  null=True, blank=True, help_text="An external resource with additional information about the object")

class References(models.Model):
    documents = models.ForeignKey(Document, null=True, blank=True, on_delete=models.CASCADE, help_text="Documents that provide additional information (not data file).")
    references = models.ForeignKey('organization.Publication', null=True, blank=True, on_delete=models.CASCADE, help_text="The publications that provide more information about the object.")
    url = models.URLField(max_length=200,  null=True, blank=True, help_text="An external resource with additional information about the object")
    dbxrefs = models.CharField(max_length=100, null=True, blank=True, help_text="Unique identifiers from external resources.")
    class Meta:
        abstract = True

 
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100, null=False, default="", help_text="The complete name of the originating lab or vendor. ")
    vendor_description = models.CharField(max_length=100, null=False, default="", help_text="A plain text description of the source.")
    vendor_url =  models.URLField(max_length=200, help_text="An external resource with additional information about the source.")
    def __str__(self):
        return self.vendor_name    
    
class Construct(References):
    construct_name = models.CharField(max_length=50, null=False, default="", help_text="Short name for construct - letters, numbers, hyphens or underscores allowed (no spaces)")
    construct_description = models.CharField(max_length=200, null=True, blank=True, help_text="A plain text description of the construct.")
    construct_type = models.ForeignKey('organization.Choice',related_name='conChoice', on_delete=models.CASCADE, help_text="The categorization of the construct.")
    construct_vendor = models.ForeignKey(Vendor,related_name='conVendor',null=True, blank=True, help_text="The Lab or Vendor that provided the construct.")
    construct_designed_to_target = models.CharField(max_length=200, null=True, blank=True, help_text="The gene or genomic region that this construct is designed to target")
    construct_insert_sequence = models.CharField(max_length=200, null=True, blank=True, help_text="Nucleotide Sequence of the Insert")
    construct_map =  models.ForeignKey(Document,related_name='conDoc',null=True, blank=True, on_delete=models.CASCADE, help_text="Map of the construct - document")
    construct_tag = models.CharField(max_length=200, null=True, blank=True, help_text="String describing tags the construct contains.")
    construct_vector_backbone = models.CharField(max_length=200, null=True, blank=True, help_text="The vector backbone for this construct")
    def __str__(self):
        return self.construct_name 

class  GenomicRegions(models.Model):
    genomicRegions_genome_assembly = models.ForeignKey('organization.Choice',related_name='genAssChoice', on_delete=models.CASCADE, help_text="The genome assembly from which the region was derived")
    genomicRegions_chromosome = models.ForeignKey('organization.Choice',related_name='chrChoice',null=True, blank=True, help_text="The chromosome containing the region")
    genomicRegions_start_coordinate =  models.IntegerField(null=True, blank=True, help_text="The base position of the start coordinate of the region - start < end")
    genomicRegions_end_coordinate = models.IntegerField(null=True, blank=True, help_text="The base position of the end coordinate - end > start")
    genomicRegions_location_description = models.CharField(max_length=200, null=True, blank=True, help_text="If exact coordinates of the region are not available a description of the genome location")
    genomicRegions_start_location = models.CharField(max_length=200, null=True, blank=True, help_text="If the exact start coordinate is not know a description of the start location")
    genomicRegions_end_location = models.CharField(max_length=200, null=True, blank=True, help_text="If the exact end coordinate is not know a description of the start location")
    
    
class  Target(References):
    target_genes = models.CharField(max_length=200,  null=False, default="", help_text="The genes that are specifically targeted - can also be derived from genomic region info")
    target_region = models.ForeignKey(GenomicRegions, null=True, blank=True, on_delete=models.CASCADE, help_text="The genome assembly, chromosome and coordinates of the region that is targeted")

class Modification(UserOwner,References): 
    modification_name = models.CharField(max_length=50, null=False, default="")
    modification_type = models.ForeignKey('organization.Choice',related_name='modChoice',on_delete=models.CASCADE, help_text="The type of genomic modification.")
    modification_constructs = models.ForeignKey(Construct,related_name='modConstructs', on_delete=models.CASCADE, help_text="Recombinant constructs used to make modification.")
    modification_vendor = models.ForeignKey(Vendor,related_name='modVendor',on_delete=models.CASCADE, null=True, blank=True, help_text="Lab or Company that produced the modfication")
    modification_gRNA = models.CharField(max_length=200, null=True, blank=True, help_text="The guide RNA sequences used in Crispr targetting.")
    modification_genomicRegions = models.ForeignKey(GenomicRegions,related_name='modGen', on_delete=models.CASCADE, null=True, blank=True, help_text="The genomic regions being modified.")
    modification_target = models.ForeignKey(Target,related_name='modTarget',null=True, blank=True, help_text="The targeted gene or genomic region that is targeted by the modification.")
    modification_description = models.CharField(max_length=200,  null=False, default="", help_text="A brief plain text description of the modification.")
     
    def __str__(self):
        return self.modification_name
 

class Individual(References):
    individual_name = models.CharField(max_length=50, null=False, default="")
    individual_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='indVen',null=True, blank=True)
    individual_type = models.ForeignKey('organization.JsonObjField',related_name='indType')
    individual_fields = JSONField(null=True, blank=True)
    def __str__(self):
        return self.individual_name 
     
class Enzyme(References):
    enzyme_name = models.CharField(max_length=50, null=False, default="", help_text="The name of the digestion enzyme.")
    enzyme_recogSeq = models.CharField(max_length=20,  null=True, blank=True, help_text="The bases of the enzyme recognition sequence.")
    enzyme_siteLen =  models.IntegerField(null=True, blank=True, help_text="The length of the enzyme recognition sequence.")
    enzyme_cutPos = models.IntegerField(null=True, blank=True, help_text="The position in the provided recognition sequence at which the enzyme cuts AFTER - relative to base 1 of site.")
    enzyme_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, help_text="The Lab or Vendor that provided the enzyme.")
    enzyme_catalog_number = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    enzyme_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text description of the enzyme.")
    def __str__(self):
        return self.enzyme_name

     
class Protocol(UserOwner):
    protocol_name =  models.CharField(max_length=50, null=False, default="")
    protocol_type = models.ForeignKey('organization.JsonObjField',on_delete=models.CASCADE, related_name='proType')
    protocol_fields = JSONField()
    protocol_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='proDoc',null=True, blank=True)
    protocol_enzyme = models.ForeignKey(Enzyme, on_delete=models.CASCADE, related_name='proEnzyme',null=True, blank=True)
    protocol_variation = models.TextField( null=True, blank=True)
    protocol_description = models.CharField(max_length=200,  null=True, blank=True)
    
    def __str__(self):
        return self.protocol_name

 
class Biosource(References):
    biosource_name = models.CharField(max_length=50, null=False, default="")
    biosource_type =  models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='bioChoice', help_text="The categorization of the biosource.")
    biosource_cell_line = models.CharField(max_length=200,  null=True, blank=True, help_text="Ontology term for the cell line used.")
    biosource_cell_line_tier = models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='bioCellChoice', help_text="Tier into which the cell line has been classified")
    biosource_SOP_cell_line = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='bioProtocol', help_text="Standard operation protocol for the cell line as determined by 4DN Cells Working Group")
    biosource_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, help_text="The Lab or Vendor that provided the biosource.")
    biosource_individual = models.ForeignKey(Individual,on_delete=models.CASCADE, related_name='docChoice', help_text="Information on donor or individual mouse or other organism.")
    biosource_tissue  = models.CharField(max_length=100,  null=True, blank=True, help_text="Anatomy (UBERON) Ontology term for the tissue used.")
    biosource_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    
    def __str__(self):
        return self.biosource_name
 
class Biosample(UserOwner, References):
    biosample_name = models.CharField(max_length=50, null=False, default="")
    biosample_biosource =  models.ForeignKey(Biosource, on_delete=models.CASCADE, related_name='bioSource', help_text="The cell lines or tissue types used in the experiment")
    biosample_individual =  models.ForeignKey(Individual,on_delete=models.CASCADE, related_name='bioIndi')
    biosample_modification =  models.ForeignKey(Modification,on_delete=models.CASCADE, related_name='bioMod', help_text="Expression or targeting vectors stably transfected to generate Crispr'ed or other genomic modification")
    biosample_protocol =  models.ForeignKey(Protocol,on_delete=models.CASCADE, related_name='bioMod', help_text="Information about biosample preparation protocols.")
    biosample_type =  models.ForeignKey('organization.JsonObjField',on_delete=models.CASCADE, related_name='biotype', null=True, blank=True)
    biosample_fields = JSONField(  null=True, blank=True)
    
    def __str__(self):
        return self.biosample_name
     
     
class Treatment(References):
    treatment_name = models.CharField(max_length=50, null=False, default="")
    treatment_type = models.ForeignKey('organization.JsonObjField',related_name='treatType',on_delete=models.CASCADE)
    treatment_fields = JSONField()
    treatment_biosample = models.ForeignKey(Biosample,on_delete=models.CASCADE,related_name='treatBio')
    treatment_description = models.CharField(max_length=200,  null=True, blank=True)
    
    def __str__(self):
        return self.treatment_name 
     
class Barcode(models.Model):
    barcode_name_1 = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, related_name='barChoice1')
    barcode_name_2 = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, related_name='barChoice2')
    barcode_run = models.ForeignKey('dryLab.SequencingRun',on_delete=models.CASCADE, related_name='barRun')
    barcode_exp = models.ForeignKey('organization.Experiment',on_delete=models.CASCADE, related_name='barRun')
    
    