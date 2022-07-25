from django.db import models

# Create your models here.
class data_Russian(models.Model):
    seq = models.IntegerField()
    id = models.CharField(primary_key=True, unique=True, null=False, max_length=200)
    date = models.CharField(max_length=200)
    time_length = models.IntegerField()
    gender = models.CharField(max_length=200)
    medium = models.CharField(max_length=200)
    text_type = models.CharField(max_length=200)
    text = models.TextField()

class data_output(models.Model):
    text = models.TextField()
    Text_POS = models.TextField()
    Only_POS = models.TextField()
    Text_Lemma = models.TextField()