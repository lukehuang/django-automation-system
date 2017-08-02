# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.forms import Textarea, TextInput
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from concurrency.fields import IntegerVersionField
from django.db.models.signals import post_save
#these are required by gana's choice to insert a form here and need to be moved.
import datetime
from django import forms
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save
from Custom.helper import dbpull, dbwrite
#from Utilities.models import Utility_Providers
from KUDZU.formatchecker import ContentTypeRestrictedFileField
import time
####################
##Special Field Types
class MyTextField(models.TextField):
#A more reasonably sized textarea
    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':2, 'cols':120})}
         )
         return super(MyTextField, self).formfield(**kwargs)


class ShortCharField(models.CharField):
#A small TextInput field
    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": TextInput(attrs={'size':5})}
         )
         return super(ShortCharField, self).formfield(**kwargs)

##################################### 
class MyUser(AbstractBaseUser):
    some_extra_data = models.CharField(max_length=100, blank=True)

def filee(self,filename):
    url = "uploads/%s/%s" % (self.uniqueid.uniqueid,filename)
    return url

#Automation History 
class AutomationHistory(models.Model):    
                              
    #uniqueid = models.ForeignKey('Pml', null=True, blank=True, db_column="UniqueID", verbose_name = 'Unique ID')
    playbook = models.ForeignKey(PlayBook, db_column="PlayBookID", verbose_name = 'PlayBook')
    history_id = models.AutoField(primary_key=True, db_column="HistoryID", verbose_name = 'History ID')
    initiated_date = models.DateTimeField(auto_now_add=True, db_column="initiatedDate", verbose_name = 'Initiated')
    updated_date = models.DateTimeField(auto_now=True, db_column="updatedDate", verbose_name = 'Updated')
    history_status = models.CharField(max_length=50,null=True, blank=True, db_column="historyStatus", verbose_name = 'History Status')
    senderId = models.CharField(max_length=50,null=True, blank=True, db_column="senderid", verbose_name = 'Sender ID')
    contactPersonalId = models.CharField(max_length=50,null=True, blank=True, db_column="contact_personal_id", verbose_name = 'Contact Personal ID')

    class Meta:
        managed = False
        db_table = 'Automation_History'
        verbose_name = 'Automation History'
        verbose_name_plural = verbose_name + 's'
        

#Automation History Projects
class AutomationHistoryProjects(models.Model):    
                              
    #aid = models.AutoField(primary_key=True,db_column="aid", verbose_name = 'ID', default=1)
    history = models.ForeignKey(AutomationHistory, db_column="history", verbose_name = 'History')
    #playbook_project_id = models.CharField(max_length=50, db_column="PlaybookProjectID", verbose_name = 'Playbook Project ID',default=1)
    playbook_project_id = models.AutoField(primary_key=True, db_column="PlaybookProjectID", verbose_name = 'PlayBookPorject ID')
    
    playbookId = models.CharField(max_length=50, db_column="playbookId", verbose_name = 'playbookId',default=1)
    
    previous_project_status = models.CharField(max_length=50, db_column="previousProjectStatus", verbose_name = 'Previous Project Status')    
    new_project_status = models.CharField(max_length=50, db_column="newProjectStatus", verbose_name = 'New Project Status')
    
    previous_scheduled_completion_date = models.DateField(null=True, blank=True, db_column="previousScheduledCompletionDate", verbose_name = 'Previous Scheduled Completion')
    new_scheduled_completion_date = models.DateField(null=True, blank=True, db_column="newScheduledCompletionDate", verbose_name = 'New Scheduled Completion')    
    
    previous_start_date = models.DateField(null=True, blank=True, db_column="previousStartDate", verbose_name = 'Previous Start Date')
    new_start_date = models.DateField(null=True, blank=True, db_column="newStartDate", verbose_name = 'New Start Date')
    
    previous_completion_date = models.DateField(null=True, blank=True, db_column="previousCompletionDate", verbose_name = 'Previous Completion Date')
    new_completion_date = models.DateField(null=True, blank=True, db_column="newCompletionDate", verbose_name = 'New Completion Date')
    
    class Meta:
        managed = False
        db_table = 'Automation_History_Projects'
        verbose_name = 'Automation History Project' 
        verbose_name_plural = verbose_name + 's' 