from django.db import models
from django.contrib.postgres.fields import JSONField
 
# Create your models here.
 
class SequencingRun(models.Model):
    BARCODE_CHOICES = (
        ('addBarcode', 'Yes'),
        ('detailProject', 'No'),
    )
    run_name = models.CharField(max_length=100, null=False, default="")
    run_project =  models.ForeignKey('organization.Project',related_name='runProject', on_delete=models.CASCADE,)
    run_Experiment = models.ManyToManyField('organization.Experiment',related_name='runExp')
    run_sequencing_platform = models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='runPlatChoice', help_text="Sequencing platform.")
    run_sequencing_center = models.ForeignKey('organization.Choice', on_delete=models.CASCADE, related_name='runCenterChoice', help_text="Where the sequencing has been done.")
    run_submission_date = models.DateField();
    run_retrieval_date = models.DateField(null=True, blank=True,);
    run_approved = models.BooleanField(default=False)
    run_submitted = models.BooleanField(default=False)
    run_Add_Barcode = models.CharField(
        max_length=13,
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
        return self.sequencingFile_name

class FileSet(models.Model):
    fileSet_name = models.CharField(max_length=50, null=False, default="")
    fileset_type = models.CharField(max_length=100, null=False, default="")
    fileSet_file = models.ManyToManyField(SeqencingFile,related_name='fileSetFile')
    fileset_description =  models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.fileSet_name



class Analysis(models.Model):
    analysis_name = models.CharField(max_length=50, null=False, default="")
    analysis_type = models.ForeignKey('organization.JsonObjField',related_name='analysisType', on_delete=models.CASCADE, help_text="AnalysisField")
    analysis_fields = JSONField( null=True, blank=True)
    analysis_file = models.ManyToManyField(SeqencingFile,related_name='analysisFile')
    analysis_exp = models.ForeignKey('organization.Experiment',related_name='analysisExp', on_delete=models.CASCADE,)
    analysis_import = models.FileField(upload_to='uploads/', null=True, blank=True, help_text="Import .gz file")
    
    def __str__(self):
        return self.analysis_name
    
    class Meta:
        verbose_name_plural = 'Analysis'

class Images(models.Model):
    image_path = models.FilePathField(max_length=500)
    image_analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    def __str__(self):
        return self.image_path
    class Meta:
        verbose_name_plural = 'Images'
