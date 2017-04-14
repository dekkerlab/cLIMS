from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from organization.validators import alphanumeric

 
# Create your models here.
class UserOwner (models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE,)
    class Meta:
        abstract = True

class Document(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True, help_text="Name of the document", validators=[alphanumeric])
    description = models.CharField(max_length=200, null=False, default="")
    type = models.ForeignKey('organization.Choice',related_name='docChoice',on_delete=models.CASCADE, help_text="The category that best describes the document.")
    attachment = models.FileField(upload_to='uploads/')
    references = models.ForeignKey('organization.Publication', null=True, blank=True, on_delete=models.CASCADE, help_text="The publications that provide more information about the object.")
    url = models.URLField(max_length=200,  null=True, blank=True, help_text="An external resource with additional information about the object")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.description
        
class References(models.Model):
    document = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, help_text="Documents that provide additional information (not data file).")
    references = models.ForeignKey('organization.Publication', null=True, blank=True, help_text="The publications that provide more information about the object.")
    url = models.URLField(max_length=200,  null=True, blank=True, help_text="An external resource with additional information about the object")
    dbxrefs = models.CharField(max_length=100, null=True, blank=True, help_text="Unique identifiers from external resources, enter as a database name:identifier eg. HGNC:PARK2")
    class Meta:
        abstract = True

 
class Vendor(models.Model):
    vendor_title = models.CharField(max_length=100, null=False, default="", unique=True, db_index=True, help_text="The complete name of the originating lab or vendor.", validators=[alphanumeric])
    vendor_description = models.CharField(max_length=100, null=False, default="", help_text="A plain text description of the source.")
    vendor_url =  models.URLField(max_length=200, help_text="An external resource with additional information about the source.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.vendor_title    
    
class Construct(models.Model):
    construct_name = models.CharField(max_length=50, null=False, default="", unique=True, db_index=True, help_text="Short name for construct - letters, numbers, hyphens or underscores allowed (no spaces)", validators=[alphanumeric])
    construct_type = models.ForeignKey('organization.Choice',related_name='conChoice', null=True, blank=True, on_delete=models.CASCADE, help_text="The categorization of the construct.")
    construct_vendor = models.ForeignKey(Vendor,related_name='conVendor',null=True, blank=True, help_text="The Lab or Vendor that provided the construct.")
    construct_designed_to_Target = models.CharField(max_length=200, null=True, blank=True, help_text="The gene or genomic region that this construct is designed to target")
    construct_insert_sequence = models.CharField(max_length=200, null=True, blank=True, help_text="Nucleotide Sequence of the Insert")
    document =  models.ForeignKey(Document,verbose_name="construct_map",related_name='conDoc',null=True, blank=True, on_delete=models.CASCADE, help_text="Map of the construct - document")
    construct_tag = models.CharField(max_length=200, null=True, blank=True, help_text="String describing tags the construct contains.")
    construct_vector_backbone = models.CharField(max_length=200, null=True, blank=True, help_text="The vector backbone for this construct")
    construct_description = models.CharField(max_length=200, null=True, blank=True, help_text="A plain text description of the construct.")
    references = models.ForeignKey('organization.Publication', null=True, blank=True, help_text="The publications that provide more information about the object.")
    url = models.URLField(max_length=200,  null=True, blank=True, help_text="An external resource with additional information about the object")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.construct_name
        

class  GenomicRegions(models.Model):
    name = models.CharField(max_length=50, null=False, default="", unique=True, db_index=True, help_text="Please give a name.", validators=[alphanumeric])
    genomicRegions_genome_assembly = models.ForeignKey('organization.Choice',related_name='genAsmChoice', null=False, default="", on_delete=models.CASCADE, help_text="The genome assembly from which the region was derived", validators=[alphanumeric])
    genomicRegions_chromosome = models.ForeignKey('organization.Choice',related_name='chrChoice',null=True, blank=True, help_text="The chromosome containing the region")
    genomicRegions_start_coordinate =  models.IntegerField(null=True, blank=True, help_text="The base position of the start coordinate of the region - start < end")
    genomicRegions_end_coordinate = models.IntegerField(null=True, blank=True, help_text="The base position of the end coordinate - end > start")
    genomicRegions_location_description = models.CharField(max_length=200, null=True, blank=True, help_text="If exact coordinates of the region are not available a description of the genome location")
    genomicRegions_start_location = models.CharField(max_length=200, null=True, blank=True, help_text="If the exact start coordinate is not know a description of the start location")
    genomicRegions_end_location = models.CharField(max_length=200, null=True, blank=True, help_text="If the exact end coordinate is not know a description of the start location")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.dcic_alias
    class Meta:
        verbose_name_plural = 'GenomicRegions'
    
class  Target(References):
    name = models.CharField(max_length=50, null=False, default="", unique=True, db_index=True, help_text="Please give a name.", validators=[alphanumeric])
    targeted_genes = models.CharField(max_length=200, null=True, blank=True, help_text="The genes that are specifically targeted - can also be derived from genomic region info.")
    targeted_region =  models.ForeignKey(GenomicRegions, null=True, blank=True, related_name='targetGenAsm', on_delete=models.CASCADE, help_text="The genome assembly, chromosome and coordinates of the region that is targeted")
    target_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A brief plain text description of the target.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.name

class Modification(UserOwner,References): 
    modification_name = models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    modification_type = models.ForeignKey('organization.Choice',related_name='modChoice',on_delete=models.CASCADE, help_text="The type of genomic modification.")
    constructs = models.ForeignKey(Construct,related_name='modConstructs', on_delete=models.CASCADE, null=True, blank=True,help_text="Recombinant constructs used to make modification.")
    modification_vendor = models.ForeignKey(Vendor,related_name='modVendor',on_delete=models.CASCADE, null=True, blank=True, help_text="Lab or Company that produced the modfication")
    modification_gRNA = models.CharField(max_length=200, null=True, blank=True, help_text="The guide RNA sequences used in Crispr targetting.")
    modification_genomicRegions = models.ForeignKey(GenomicRegions,related_name='modGen', on_delete=models.CASCADE, null=True, blank=True, help_text="The genomic regions being modified.")
    target = models.ForeignKey(Target,related_name='modTarget',null=True, blank=True, help_text="The targeted gene or genomic region that is targeted by the modification.")
    modification_description = models.CharField(max_length=200,  null=False, default="", help_text="A brief plain text description of the modification.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.") 
    def __str__(self):
        return self.modification_name
 

class Individual(References, UserOwner):
    individual_name = models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    individual_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='indVen',null=True, blank=True)
    individual_type = models.ForeignKey('organization.JsonObjField',related_name='indType',  help_text="JsonObjField")
    individual_fields = JSONField(null=True, blank=True)
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.individual_name
     
class Enzyme(References):
    enzyme_name = models.CharField(max_length=50, null=False, default="", unique=True, db_index=True, help_text="The name of the digestion enzyme.", validators=[alphanumeric])
    enzyme_recogSeq = models.CharField(max_length=20,  null=True, blank=True, help_text="The bases of the enzyme recognition sequence.")
    enzyme_siteLen =  models.IntegerField(null=True, blank=True, help_text="The length of the enzyme recognition sequence.")
    enzyme_cutPos = models.IntegerField(null=True, blank=True, help_text="The position in the provided recognition sequence at which the enzyme cuts AFTER - relative to base 1 of site.")
    enzyme_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, help_text="The Lab or Vendor that provided the enzyme.")
    enzyme_catalog_number = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    enzyme_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text description of the enzyme.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.enzyme_name

     
class Protocol(UserOwner):
    name =  models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    attachment = models.FileField(upload_to='uploads/', null=True, blank=True)
    enzyme = models.ForeignKey(Enzyme, on_delete=models.CASCADE, related_name='proEnzyme',null=True, blank=True)
    description = models.CharField(max_length=200,  null=True, blank=True)
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.name

 
class Biosource(References):
    biosource_name = models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    biosource_type =  models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='sourceChoice', help_text="The categorization of the biosource.")
    biosource_cell_line = models.CharField(max_length=200,  null=True, blank=True, help_text="Ontology term for the cell line used.")
    biosource_cell_line_tier = models.ForeignKey('organization.Choice', null=True, blank=True, on_delete=models.CASCADE, related_name='bioCellChoice', help_text="Tier into which the cell line has been classified")
    protocol = models.ForeignKey(Protocol, null=True, blank=True, on_delete=models.SET_NULL, related_name='bioProtocol', verbose_name="biosource_SOP_cell_line", help_text="Standard operation protocol for the cell line as determined by 4DN Cells Working Group")
    biosource_vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.SET_NULL, related_name='sourceVendor',help_text="The Lab or Vendor that provided the biosource.")
    cell_line_termid = models.CharField(max_length=100,  null=True, blank=True, help_text="EFO term ID for cell line.")
    biosource_individual = models.ForeignKey(Individual,on_delete=models.CASCADE, related_name='sourceInd', help_text="Information on donor or individual mouse or other organism.")
    modifications = models.ManyToManyField(Modification, blank=True, related_name='biosMod', 
                                      help_text="Expression or targeting vectors stably transfected to generate Crispr'ed or other genomic modification.")
    biosource_tissue  = models.CharField(max_length=100,  null=True, blank=True, help_text="Anatomy (UBERON) Ontology term for the tissue used.")
    biosource_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.biosource_name
 
     
class TreatmentRnai(References, UserOwner):
    treatmentRnai_name = models.CharField(max_length=50, null=False, default="", unique=True, db_index=True, validators=[alphanumeric])
    treatmentRnai_type = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, related_name='rnaiType')
    constructs= models.ForeignKey(Construct, on_delete=models.CASCADE, related_name='rnaiType',null=True, blank=True, verbose_name="treatmentRnai_constructs", help_text="Recombinant constructs used for RNAi")
    treatmentRnai_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='rnaiVendor',null=True, blank=True, help_text="RNAi center that provided the RNAi.")
    treatmentRnai_target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='rnaiTarget',null=True, blank=True, verbose_name="treatmentRnai_target", help_text="The targeted gene or genomic region that is targeted by the modification.")
    treatmentRnai_nucleotide_seq =  models.CharField(max_length=50, null=True, blank=True, default="", help_text="The nucleotide sequence of the target region.")
    treatmentRnai_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.treatmentRnai_name

class TreatmentChemical(References, UserOwner):
    treatmentChemical_name = models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    treatmentChemical_chemical = models.CharField(max_length=50, null=False, default="")
    treatmentChemical_concentration = models.FloatField(max_length=10, null=False,default=0)
    treatmentChemical_concentration_units = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, null=True, blank=True, related_name='conUnits')
    treatmentChemical_duration = models.FloatField(max_length=10,null=False,default=0) 
    treatmentChemical_duration_units = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, null=True, blank=True, related_name='timeUnits')
    treatmentChemical_temperature = models.FloatField(max_length=10,null=False, default=0)
    treatmentChemical_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.treatmentChemical_name 

class OtherTreatment(References, UserOwner):
    name = models.CharField(max_length=50, null=False, default="", validators=[alphanumeric])
    description = models.TextField()

    def __str__(self):
        return self.name

class Biosample(UserOwner, References):
    biosample_name = models.CharField(max_length=50, null=False, unique=True, db_index=True, default="", validators=[alphanumeric])
    biosample_biosource =  models.ForeignKey(Biosource, on_delete=models.CASCADE, related_name='bioSource', help_text="The cell lines or tissue types used in the experiment")
    biosample_individual =  models.ForeignKey(Individual,on_delete=models.CASCADE, related_name='bioIndi')
    modifications =  models.ManyToManyField(Modification, related_name='bioMod', blank=True, help_text="Expression or targeting vectors stably transfected to generate Crispr'ed or other genomic modification")
    protocol =  models.ForeignKey(Protocol, null=True, blank=True, on_delete=models.CASCADE, related_name='bioMod', help_text="Information about biosample preparation protocols.")
    biosample_TreatmentRnai =  models.ManyToManyField(TreatmentRnai, blank=True, related_name='biosamTreatmentRnai', help_text="Select previously created treatment")
    biosample_TreatmentChemical =  models.ManyToManyField(TreatmentChemical, blank=True, related_name='biosamTreatmentChemical', help_text="Select previously created treatment")
    biosample_OtherTreatment =  models.ManyToManyField(OtherTreatment, blank=True, related_name='biosamOtherTreatment', help_text="Select previously created treatment")
    biosample_type =  models.ForeignKey('organization.JsonObjField',on_delete=models.CASCADE, related_name='biotype', null=False, default="", verbose_name="BiosampleCellCulture Details",help_text="JsonObjField")
    biosample_fields = JSONField(  null=True, blank=True)
    imageObjects = models.ManyToManyField( 'dryLab.ImageObjects', related_name='bioImg', blank=True, help_text="Cell growth images")
    biosample_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A plain text for catalog description.")
    dcic_alias = models.CharField(max_length=500, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    def __str__(self):
        return self.biosample_name
     
class Barcode(models.Model):
    barcode_name = models.CharField(max_length=50, null=False, default="", validators=[alphanumeric])
    barcode_index = models.ForeignKey('organization.Choice',on_delete=models.CASCADE, related_name='barChoice')
    barcode_position = models.CharField(max_length=200,  null=True, blank=True, help_text="The 1-based start position of the barcode in 5->3 orientation.")
    
    def __str__(self):
        return (str(self.barcode_name))
    
    