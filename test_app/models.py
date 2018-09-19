""" Create jobs model """

from django.db import models

class JobSeeker(models.Model):

    """ Create jobs model """

    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    title_id = models.CharField(max_length=100)
    normalized_title = models.CharField(max_length=100)
    skills = models.CharField(max_length=50000)
    score = models.IntegerField(default=True)

    class Meta:
        """ Create class to changes model name in database"""
        db_table = 'jobs'

    def __str__(self):
        return self.title
