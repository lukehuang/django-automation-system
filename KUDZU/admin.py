from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models
from django.forms import CheckboxInput,NumberInput,ModelMultipleChoiceField,ModelChoiceField
from django.contrib.admin.filters import AllValuesFieldListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from KUDZU.models import *
from django.core.urlresolvers import reverse
from decimal import *
from concurrency.admin import ConcurrentModelAdmin
from django.db.models import Q    
from KUDZU.forms import *
from KUDZU.supportactions import TIPS_export_xlsx,CloneTips
import re
import time
from django.utils.html import format_html_join,format_html
from django.forms.models import BaseInlineFormSet
from django.db.models import Max
from django.http import Http404


#Automation History  
class AutomationHistoryProjectsInline(admin.TabularInline):
    max_num = 5000
    extra = 2
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    model=AutomationHistoryProjects
    
    #readonly_fields = ('playbookId','previous_project_status','new_project_status','previous_scheduled_completion_date','new_scheduled_completion_date','previous_start_date','new_start_date','previous_completion_date','new_completion_date')
    #readonly_fields = (['playbookId'])
    readonly_fields = (['show_pr_names','show_previous_project_status','show_new_project_status','previous_scheduled_completion_date','new_scheduled_completion_date','previous_start_date','new_start_date','previous_completion_date','new_completion_date'])
    
    fields = ('show_pr_names','show_previous_project_status','show_new_project_status','previous_scheduled_completion_date','new_scheduled_completion_date','previous_start_date','new_start_date','previous_completion_date','new_completion_date')
    
    def show_previous_project_status(self, obj):
        project_status_choices1 =(('1', 'Scheduled'), 
                               ('2', 'In Progress'), 
                               ('3', 'Completed'), 
                               ('4', 'On Hold'))       

        d = dict(project_status_choices1)       
        return d.get(obj.previous_project_status,None)
        
    show_previous_project_status.admin_order_field  = 'Previous Project Status'  
    show_previous_project_status.short_description = 'Previous Project Status'
    
    def show_new_project_status(self, obj):
        project_status_choices1 =(('1', 'Scheduled'), 
                               ('2', 'In Progress'), 
                               ('3', 'Completed'), 
                               ('4', 'On Hold'))       

        d = dict(project_status_choices1)       
        return d.get(obj.new_project_status,None)
        
    show_new_project_status.admin_order_field  = 'New Project Status'  
    show_new_project_status.short_description = 'New Project Status'
    
    def show_pr_names(self, obj):
        try:
            z=PlayBookProjects.objects.get(project_id=obj.playbookId)
            project_category_choices =(('1', 'Building Envelope'),
                                    ('2', 'Domestic Water'),
                                    ('3', 'EMS'),
                                    ('4', 'Exterior Water'),
                                    ('5', 'HVAC'),
                                    ('6', 'HVAC Controls'),
                                    ('7', 'Lighting - Exterior'),
                                    ('8', 'Lighting - Interior'),
                                    ('9', 'Lighting - Interior/Exterior'),
                                    ('10', 'Lighting Controls'),
                                    ('11', 'Mechanical'),
                                    ('12', 'Metering'),
                                    ('13', 'Operations'),
                                    ('14', 'Value Added'),
                                    ('15', 'Waste'),
                                    ('16', 'Water'),
                                    ('17', 'Other'))
                                    
            
           
            d = dict(project_category_choices)       
            return d.get(z.category,None)
        except:
            return None
        
    show_pr_names.admin_order_field  = 'Category'  
    show_pr_names.short_description = 'Category'
    
    extra = 0
    max_num=0
    can_delete=False


class AutomationHistoryAdmin(admin.ModelAdmin):
    
    model = AutomationHistory    
    list_display = ('get_playbook_property','get_sender_name','get_contact_name','history_status','initiated_date','show_updated_date')
    class Media:
        js = ('/static/admin/js/admin.js',)
       
    def get_contact_name(self, obj):
        try:
            z=LogMContactinfoDetails.objects.filter(personnel_id=obj.contactPersonalId)
            nameEmail=z[0].personsname + " ("+z[0].emailaddress+")"
        except:
            nameEmail=''
        return nameEmail
    get_contact_name.admin_order_field  = 'Received By'  
    get_contact_name.short_description = 'Received By'
    
    def show_updated_date(self, obj):  
        repDate=''
        if obj.history_status=='Replied':            
            #repDate = parser.parse(str(obj.updated_date)).strftime('%M %d, %Y, %h:%i %a')
            #repDate = '{%M %d, %Y, %h:%i}'.format(obj.updated_date)
            repDate = obj.updated_date.strftime('%B %d, %Y, %H:%M %p')
        return repDate
    show_updated_date.admin_order_field  = 'Replied On'  
    show_updated_date.short_description = 'Replied On'
    
    def get_sender_name(self, obj):
        try:
            z=AuthUser.objects.filter(id=obj.senderId)
            nameEmail=z[0].first_name + " ("+z[0].email+")"
        except:
            nameEmail=''
        return nameEmail
        
    get_sender_name.admin_order_field  = 'Sent By'  
    get_sender_name.short_description = 'Sent By' 
    
    def get_playbook_property(self, obj):
        return str(obj.playbook.uniqueid.nametouse)
    get_playbook_property.admin_order_field  = 'Playbook Property'  
    get_playbook_property.short_description = 'Playbook Property' 
         
    inlines = [AutomationHistoryProjectsInline]
    
    readonly_fields = ('get_playbook_property','initiated_date','get_sender_name','get_contact_name','history_status','show_updated_date')
    exclude = ('senderId','contactPersonalId','playbook')            
              
#############################
admin.site.register(AutomationHistory, AutomationHistoryAdmin)