from django.db import models

# Create your models here.
class TodoModel(models.Model):
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  created_date = models.DateTimeField(auto_now_add=True)
  completed_date = models.DateTimeField(null=True)