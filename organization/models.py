from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


# Create your models here.

class JsonObjField(models.Model):
    field_name = models.CharField(max_length=50, null=False, default="", db_index=True)
    field_type = models.CharField(max_length=50, null=False, default="")
    field_set = JSONField()
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
    project_owner = models.ForeignKey(User, related_name='ownerProject', on_delete=models.CASCADE,)
    project_contributor = models.ManyToManyField(User, related_name='memberProject')
    project_name = models.CharField(max_length=200, null=False, default="", unique=True,  db_index=True)
    project_notes = models.TextField( null=True, blank=True)
    project_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.project_name

class Experiment(models.Model):
    experiment_name = models.CharField(max_length=100, null=False, default="", db_index=True)
    experiment_type = models.ForeignKey(JsonObjField,related_name='expType', on_delete=models.CASCADE,)
    experiment_fields = JSONField()
    experiment_project = models.ForeignKey(Project,related_name='expProject', on_delete=models.CASCADE,)
    experiment_biosample = models.ForeignKey('wetLab.Biosample',related_name='expBio', on_delete=models.CASCADE,)
    experiment_protocol = models.ForeignKey('wetLab.Protocol',related_name='expPro', on_delete=models.CASCADE,)
    experiment_description = models.CharField(max_length=200,  null=True, blank=True)
    experiment_enzyme = models.ForeignKey('wetLab.Enzyme',related_name='expEnz', on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.exp_name

class ExperimentSet(models.Model):
    experimentSet_type = models.CharField(max_length=50, null=False, default="", db_index=True)
    experimentSet_exp = models.ManyToManyField(Experiment, related_name='setExp')
    experimentSet_description = models.CharField(max_length=200,  null=True, blank=True)

    def __str__(self):
        return self.experimentSet_type
    
class Publication(models.Model):
    publication_title = models.CharField(max_length=200, null=False, default="")
    publication_abstract = models.CharField(max_length=400,  null=True, blank=True)
    publication_authors = models.CharField(max_length=200, null=False, default="")
    publication_categories = models.CharField(max_length=200,  null=True, blank=True)
    publication_dataUsed = models.CharField(max_length=200,  null=True, blank=True)
    publication_datePublished = models.DateField()
    publication_dateRevised = models.DateField( null=True, blank=True)
    publication_issue = models.CharField(max_length=200, null=False, default="")
    publication_journal = models.CharField(max_length=200, null=False, default="")
    publication_supplementry = models.CharField(max_length=200,  null=True, blank=True)
    publication_exp = models.ManyToManyField(Experiment, related_name='pubExp')
    
    
    def __str__(self):
        return self.pub_title
    
    
class Award(models.Model):
    award_name = models.CharField(max_length=50, null=False, default="", db_index=True)
    award_exp = models.ManyToManyField(Experiment, related_name='awardExp')
    award_project = models.ManyToManyField(Project, related_name='awardPro')

    def __str__(self):
        return self.award_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100, null=False, default="", db_index=True)
    tag_color = models.CharField(max_length=50, null=False, default="Red")
    tag_exp = models.ManyToManyField(Experiment, related_name='tagExp')
    tag_user = models.ForeignKey(User, related_name='tagUser', on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.tag_name

 




    
     
    