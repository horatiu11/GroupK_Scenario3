import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ReferenceList(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length=200)
	createdAt = models.DateTimeField('date published')


class Reference(models.Model):
	reference_list = models.ForeignKey(ReferenceList, on_delete = models.CASCADE)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	website = models.CharField(max_length=1000)
	source = models.CharField(max_length=100)
	notes = models.CharField(max_length=5000)
