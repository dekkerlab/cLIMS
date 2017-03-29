from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from wetLab.models import References


# Create your models here.

class JsonObjField(models.Model):
    field_name = models.CharField(max_length=50, null=False, default="", db_index=True)
    field_type = models.CharField(max_length=50, null=False, default="")
    field_set = JSONField(null=True, blank=True)
    jsonField_description = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.field_name

class Choice(models.Model):
    choice_name = models.CharField(max_length=50, null=False, default="", db_index=True)
    choice_type = models.CharField(max_length=50, null=False, default="")
    choice_description =  models.CharField(max_length=200,  null=True, blank=True,)
    
    def __str__(self):
        return self.choice_name
    
class Project(models.Model):
    project_name = models.CharField(max_length=200, null=False, default="", unique=True,  db_index=True, help_text="Name of the project")
    project_owner = models.ForeignKey(User, related_name='ownerProject', on_delete=models.CASCADE,)
    project_contributor = models.ManyToManyField(User, related_name='memberProject', blank=True,)
    project_notes = models.TextField( null=True, blank=True, help_text="Notes for the project.")
    project_active = models.BooleanField(default=True, help_text="Is project currently in progress?")
    dcic_alias = models.CharField(max_length=10, null=False, unique=True, db_index=True, default="", help_text="Provide an alias name for the object for DCIC submission.")
    
    def __str__(self):
        return self.project_name

class Experiment(References):
    UNIT_CHOICES = (
        ('', ''),
        ('g', 'g'),
        ('mg', 'mg'),
        ('μg', 'μg'),
        ('ml', 'ml'),
        ('cells', 'cells'),
    )
    experiment_name = models.CharField(max_length=100, null=False, default="", db_index=True)
    project = models.ForeignKey(Project,related_name='expProject', on_delete=models.CASCADE,)
    experiment_biosample = models.ForeignKey('wetLab.Biosample',related_name='expBio', on_delete=models.CASCADE,help_text="Starting biological material.")
    biosample_quantity = models.FloatField(null=False, default="0")
    biosample_quantity_units= models.CharField(
        max_length=5,
        choices=UNIT_CHOICES,
        default='',
    )
    protocol = models.ForeignKey('wetLab.Protocol',related_name='expPro', on_delete=models.CASCADE,)
    type = models.ForeignKey('organization.JsonObjField', on_delete=models.CASCADE, related_name='expType', help_text="JsonObjField")
    experiment_fields = JSONField(null=True, blank=True)
    variation = models.TextField( null=True, blank=True, verbose_name="protocol_variations")
    experiment_enzyme = models.ForeignKey('wetLab.Enzyme',related_name='expEnz', on_delete=models.CASCADE,help_text="The enzyme used for digestion of the DNA.")
    experiment_description = models.CharField(max_length=200,  null=True, blank=True, help_text="A short description of the experiment")
    imageObjects = models.ManyToManyField( 'dryLab.ImageObjects', related_name='expImg' , blank=True, help_text="Lab gel and fragment analyzer images")
    dcic_alias = models.CharField(max_length=10, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    
    def __str__(self):
        return self.experiment_name
    

class ExperimentSet(models.Model):
    experimentSet_name = models.CharField(max_length=100, null=False, default="")
    project =  models.ForeignKey('organization.Project',related_name='expSetProject', on_delete=models.CASCADE,)
    experimentSet_type = models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='setChoice', help_text="The categorization of the set of experiments.")
    experimentSet_exp = models.ManyToManyField(Experiment, related_name='setExp')
    document = models.ForeignKey('wetLab.Document', on_delete=models.CASCADE, related_name='setDoc',null=True, blank=True)
    description =  models.CharField(max_length=200, null=False, default="")
    dcic_alias = models.CharField(max_length=10, null=False,  default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    
    def __str__(self):
        return self.experimentSet_name
    
class Publication(models.Model):
    publication_title = models.CharField(max_length=200, null=False, default="", help_text="Title of the publication or communication.")
    publication_id = models.CharField(max_length=200,  null=False, default="", help_text="PMID or doi for the publication.")
    attachment = models.FileField(upload_to='uploads/')
    exp_sets_prod_in_pub = models.ForeignKey(ExperimentSet,related_name='pubProdSet', null=True, blank=True, on_delete=models.SET_NULL, help_text="List of experiment sets that are produced by this publication.")
    exp_sets_used_in_pub = models.ForeignKey(ExperimentSet,related_name='pubUsedSet', null=True, blank=True, on_delete=models.SET_NULL, help_text="List of experiment sets that are used (not produced) by this publication.")
    publication_categories = models.ForeignKey('organization.Choice', null=True, on_delete=models.SET_NULL, related_name='pubCatChoice', help_text="The categorization of publications.")
    publication_published_by = models.ForeignKey('organization.Choice', null=True, on_delete=models.SET_NULL, related_name='pubByChoice', help_text="Publication publisher.")
    dcic_alias = models.CharField(max_length=10, null=False, default="", unique=True, db_index=True, help_text="Provide an alias name for the object for DCIC submission.")
    
    def __str__(self):
        return self.publication_title
    
    
class Award(models.Model):
    award_name = models.CharField(max_length=50, null=False, default="", db_index=True)
    award_exp = models.ManyToManyField(Experiment, related_name='awardExp')
    award_project = models.ManyToManyField(Project, related_name='awardPro')
    
    def __str__(self):
        return self.award_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100, null=False, default="", db_index=True)
    project =  models.ForeignKey('organization.Project',related_name='tagProject', on_delete=models.CASCADE,)
    tag_exp = models.ManyToManyField(Experiment, related_name='tagExp')
    tag_user = models.ForeignKey(User, related_name='tagUser', on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.tag_name

 




    
     
    