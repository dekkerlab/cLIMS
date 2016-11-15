from django.db import models
from django.contrib.postgres.fields import JSONField
 
# Create your models here.
 
class SequencingRun(models.Model):
    BARCODE_CHOICES = (
        ('addBarcode', 'Yes'),
        ('showProject', 'No'),
    )
    run_name = models.CharField(max_length=100, null=False, default="")
    run_project =  models.ForeignKey('organization.Project',related_name='runProject', on_delete=models.CASCADE,)
    run_Experiment = models.ManyToManyField('organization.Experiment',related_name='runExp')
    run_submission_date = models.DateField();
    run_retrieval_date = models.DateField(null=True, blank=True,);
    run_approved = models.BooleanField(default=False)
    run_submitted = models.BooleanField(default=False)
    run_Add_Barcode = models.CharField(
        max_length=11,
        choices=BARCODE_CHOICES,
        default='showProject',
    )
    def __str__(self):
        return self.run_name
 
class SeqencingFile(models.Model):
    sequencingFile_name = models.CharField(max_length=255, null=False, default="")
    sequencingFile_mainPath = models.CharField(max_length=500, null=False, default="")
    sequencingFile_backupPath = models.CharField(max_length=500, null=False, default="")
    sequencingFile_sha256sum = models.CharField(max_length=64, null=False, default="")
    sequencingFile_md5sum = models.CharField(max_length=32, null=False, default="")
    sequencingFile_run = models.ForeignKey(SequencingRun,related_name='fileRun', on_delete=models.CASCADE,)
    sequencingFile_exp = models.ForeignKey('organization.Experiment',related_name='fileExp', on_delete=models.CASCADE,)
    def __str__(self):
        return self.file_name

class FileSet(models.Model):
    fileSet_name = models.CharField(max_length=50, null=False, default="")
    fileset_type = models.CharField(max_length=100, null=False, default="")
    fileSet_file = models.ManyToManyField(SeqencingFile,related_name='fileSetFile')
    fileset_description =  models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.fileSet_name
 
class Analysis(models.Model):
    analysis_name = models.CharField(max_length=50, null=False, default="")
    analysis_type = models.ForeignKey('organization.JsonObjField',related_name='analysisType', on_delete=models.CASCADE, help_text="JsonObjField")
    analysis_fields = JSONField()
    analysis_file = models.ManyToManyField(SeqencingFile,related_name='analysisFile')
    analysis_exp = models.ForeignKey('organization.Experiment',related_name='analysisExp', on_delete=models.CASCADE,)
    def __str__(self):
        return self.analysis_type
    
    class Meta:
        verbose_name_plural = 'Analysis'
