#from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from KUDZU.downloadscripts import runner ,add_to_history
from django.template import RequestContext, loader
import os
import sys
from KUDZU.models import Pml,UtilityPrograms,Tips,LogMContactinfo,PlayBook,Log_m_Notes,Consultants
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import CheckboxSelectMultiple
from KUDZU.forms import *
import django_tables2 as tables
import pandas as pd
from django.utils.html import format_html_join,format_html
from django.db.models import Q, Max
from operator import itemgetter
from Custom.helper import dbwrite
from django.conf import settings
from django.core.files.base import ContentFile
import win32com.client
from django.contrib import messages
from django.contrib.messages import get_messages

lib_path = os.path.abspath('C:\\Interface\\Custom')
sys.path.append(lib_path)
import PropertySustainabilityData_Final_Class as PT

lurl='/admin/'

@login_required(login_url=lurl)
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")      


#Button that runs the script to generate the download for the allocation reviews
@login_required(login_url=lurl)
def chump(request):
    a=runner()
    return HttpResponse(a, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')                                   

#Automation views
@login_required(login_url=lurl)
def automation(request):
    
    import KUDZU.automation_process as am 
    emailValues={}    
    site_url = settings.CURRENT_SITE_URL  
    try:
        pids=request.GET.get('pls')
        pls = pids.split(',')
    except Exception as inst:
        messages.error(request, "Invalid Request parameters")
    
    for x in pls:
        playbook_id=x
        try:
            playbook = PlayBook.objects.get(playbook_id=playbook_id)  
            try:
                playbookProjects = PlayBookProjects.objects.filter(playbook_id=playbook_id)         
                pml = playbook.uniqueid 
                try:                  
                    mainContact=LogMContactinfo.objects.filter(uniqueid=pml.uniqueid,contact='MC')[0]  
                    playbookHistory = AutomationHistory(playbook=playbook,history_status='Initiated',senderId=request.user.id,contactPersonalId=mainContact.personnel.personnel_id)                
                    playbookHistory.save()  
                    newHistory=playbookHistory.history_id
                    
                              
                    #Loggedin User/JDM Employee
                    emailValues['userEmail']=request.user.email
                    emailValues['userName']=request.user.first_name
                    #Property Side Manager
                    emailValues['toEmail']=mainContact.personnel.emailaddress
                    emailValues['toName']=mainContact.personnel.personsname            
                    #Property Details
                    emailValues['propertyName']=pml.nametouse
                    emailValues['linkToUpdate']=str(site_url)+"KUDZU/automation/update/"+str(newHistory)
                    emailStatus=am.sendAutomationEmail(emailValues)
                    if emailStatus==True:                    
                        try:                        
                            for project in playbookProjects:
                                try:
                                    playbookHistoryProjects = AutomationHistoryProjects(history=playbookHistory,previous_project_status=project.project_status,previous_scheduled_completion_date=project.scheduled_completion_date,previous_start_date=project.start_date,previous_completion_date=project.completion_date,playbookId=project.project_id)
                                    playbookHistoryProjects.save()                                  
                                except Exception as e:                                                     
                                    messages.error(request, str(e))                        
                            messages.success(request, pml.nametouse+ " :   Email sent to "+str(mainContact.personnel.emailaddress)+".")
                        except Exception as e: 
                            messages.error(request, str(e))                        
                    else:                    
                        messages.error(request, pml.nametouse+ ' :  Email is not sending to '+str(mainContact.personnel.emailaddress))
                except Exception as e:             
                    messages.error(request, 'No Main Contact Found For: '+pml.nametouse)                                   
            except Exception as e:                  
                messages.error(request, 'Sorry there is no project for this playbook '+playbook)
        except:        
            messages.error(request, 'Sorry Invalid Property or Access Denied for this playbook '+playbook_id)
            
    return HttpResponseRedirect('/admin/KUDZU/playbook/')    
        
#Automation Status Update
def automation_status_update(request,history_id):
    import KUDZU.automation_process as am 
    emailValues={}      
    playbookHistoryProjects = AutomationHistoryProjects.objects.filter(history=history_id)
    
    try:        
        playbookHistory = AutomationHistory.objects.get(history_id=history_id) 
        getPlaybookId=playbookHistory.playbook.playbook_id 
        senderID=playbookHistory.senderId
        personalId=playbookHistory.contactPersonalId
        try:
            try: pml = playbookHistory.playbook.uniqueid
            except: return HttpResponse("Sorry Invalid Property or Access Denied")
        except:
            return HttpResponse("Sorry Invalid Playbook or Project")
    except:        
        return HttpResponse("Sorry there is no tracking history")

    if request.POST:  
        try:                     
            playbookHistory.history_status='Replied'
            playbookHistory.save()            
            for value in request.POST.getlist('project_id[]'):         
                try:
                    pr = PlayBookProjects.objects.get(project_id=value)                    
                    pr.project_status = request.POST['project_status['+value+']'] 
                    
                    playbookHistoryProjects = AutomationHistoryProjects.objects.get(history=playbookHistory,playbookId=value) 
                    playbookHistoryProjects.new_project_status=pr.project_status
                    
                    if request.POST['scheduled_completion_date['+value+']']!='':
                        pr.scheduled_completion_date = request.POST['scheduled_completion_date['+value+']']   
                        playbookHistoryProjects.new_scheduled_completion_date=pr.scheduled_completion_date
                    if request.POST['start_date['+value+']']!='':    
                        pr.start_date = request.POST['start_date['+value+']'] 
                        playbookHistoryProjects.new_start_date=pr.start_date
                    if request.POST['completion_date['+value+']']!='':    
                        pr.completion_date = request.POST['completion_date['+value+']']  
                        playbookHistoryProjects.new_completion_date=pr.completion_date 
                    pr.save()                                       
                    playbookHistoryProjects.save()
                    
                except Exception as e:                
                    messages.error(request, str(e))
                
            if len(get_messages(request))==0:  
            
                
                mainContact=LogMContactinfo.objects.filter(uniqueid=pml,contact='MC')[0]
                getSenderInfo=AuthUser.objects.get(id=senderID)                  
                
                emailValues['userEmail']=getSenderInfo.email
                emailValues['userName']=getSenderInfo.first_name
                #Property Side Manager
                emailValues['toEmail']=mainContact.personnel.emailaddress
                emailValues['toName']=mainContact.personnel.personsname            
                #Property Details
                emailValues['propertyName']=pml.nametouse                
                emailStatus=am.sendAutomationUpdateNotificationEmail(emailValues)
                
                
                           
                emailValues['userEmail']=mainContact.personnel.emailaddress
                emailValues['userName']=mainContact.personnel.personsname
                #Property Side Manager
                emailValues['toEmail']=getSenderInfo.email
                emailValues['toName']=getSenderInfo.first_name 
                #Property Details
                emailValues['propertyName']=pml.nametouse                
                emailStatus=am.sendAutomationNotificerToSender(emailValues)
                                    
                #successMsg=format_html('''Thansk for the Project Update.<br/><a href="/admin/KUDZU/playbook/'''+str(getPlaybookId)+'/change">Go the Project</a>')
                #messages.success(request, successMsg)
                d=format_html('''Thank you for updating your Playbook data. You will receive an email containing your updated Playbook report once JDM Associates has reviewed your changes.                     
                    <br/>                                    
                    If you have any questions, please email <a href="mailto:PRPIplaybooks@gmail.com">PRPIplaybooks@gmail.com</a>''')                
                rendered = render_to_string('message.html', {'title':"Playbook data update was successful",'message': d})     
                return(HttpResponse(rendered))
        
        except Exception as e:                                 
            messages.error(request, str(e))
        
    table = ProjectsTable(PlayBookProjects.objects.filter(playbook=getPlaybookId),history_id)        
    context = {'project':table,'messages':get_messages(request),'property':pml.nametouse}
    return render(request, "admin/KUDZU/automationupdate.html",context) 
    
    
class ProjectsTable(tables.Table):   
    
    project_status_choices1 =( ('1', 'Scheduled'), 
                               ('2', 'In Progress'), 
                               ('3', 'Completed'), 
                               ('4', 'On Hold'))

    projectStatusTemplates = "<select name='project_status[{{record.project_id}}]' class='projectStatus'>"
    for row in project_status_choices1:
        projectStatusTemplates+= "<option value='"+row[0]+"'  {% if record.project_status == '"+row[0]+"'%} selected {% endif %} >"+row[1]+"</option>"          
    projectStatusTemplates+= "</select>"
    
     
    project_status = tables.Column(verbose_name= 'Status (Current)',orderable=False,order_by=('project_status'))    
    new_project_status = tables.TemplateColumn(projectStatusTemplates,verbose_name= 'Status (Update)')    
    scheduledtemplate = """<input type="text" name="scheduled_completion_date[{{record.project_id}}]" class="vDateField" />"""    
    scheduled_completion_date = tables.Column(verbose_name= 'Scheduled Completion Date (Current)' )    
    new_scheduled_completion_date = tables.TemplateColumn(scheduledtemplate,verbose_name= 'Scheduled Completion Date (Update)') 

    startdatetemplate = """<input type="text" name="start_date[{{record.project_id}}]" class="vDateField" />"""   
    start_date = tables.Column(verbose_name= 'Start Date (Current)' )    
    new_start_date = tables.TemplateColumn(startdatetemplate,verbose_name= 'Start Date (Update)')
    
    completeDateTemplate = """<input type="text" name="completion_date[{{record.project_id}}]" class="vDateField" />""" 
    completion_date = tables.Column(verbose_name= 'End Date (Current)' )    
    new_completion_date = tables.TemplateColumn(completeDateTemplate,verbose_name= 'End Date (Update)')
      
    project_id=tables.Column()
    def render_project_id(self, value, record):
        return format_html('{} <input type="hidden" name="project_id[]" value="{}" />', value, record.project_id)
        
    class Meta:
        model = PlayBookProjects
        fields=("category", "project_desc", "project_status","new_project_status","scheduled_completion_date","new_scheduled_completion_date","start_date","new_start_date",'completion_date','new_completion_date')
        sequence = ("category", "project_desc", "project_status","new_project_status","scheduled_completion_date","new_scheduled_completion_date","start_date","new_start_date","completion_date",'new_completion_date')
        #exclude = ('project_id')
 

def email_playbook_report(request):     
    import KUDZU.playbook_report as pr  
    import mimetypes
    import email
    import email.mime.application
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import re
    import smtplib

    try:
        pids=request.GET.get('ids')
        plist = pids.split(',')
    except Exception as inst:
        messages.error(request, "Invalid Request parameters")
    
    for p in plist:  
        z = None 
        table1 = None
        table2 = None
        table3 = None
        dats = None
        tiptable1 = None
        tiptable2 = None 
        allowToSend=True
        
        try:
            playbook = PlayBook.objects.get(playbook_id=p)             
            pml=playbook.uniqueid
            propname = pml.nametouse           
            
            mainContact=LogMContactinfo.objects.filter(uniqueid=pml,contact='MC')[0]        
            toEmail=mainContact.personnel.emailaddress            
            fromEmail='PRPIPlaybooks@gmail.com'
            
            
        except Exception as inst:
            allowToSend=False
            messages.error(request, "Invalid Property or Contact") 
            
        if allowToSend==True:    
            try:
                response = HttpResponse(content_type='application/pdf')     

                styles, HeaderText,tiaalightblue, tiaadarkblue,Gutter,GreenText,LightBlue,DarkRed, highlight, basecolor2, highlightdark, red,llGutter, tsbase, tsupper, tstotal= \
                    pr.setstyles()
                    
                filer=pr.runpdf(pml, propname, styles, HeaderText,tiaalightblue, tiaadarkblue,Gutter,GreenText,LightBlue,DarkRed, highlight, basecolor2, highlightdark, red,llGutter, tsbase, tsupper, tstotal)                
                response=pr.createqbr(propname, filer, response,LightBlue,Gutter,'source')        
                propname = propname.replace("\\n", "")
                propname = re.sub(r'\W+', '', propname)
                msg = MIMEMultipart()
                msg['Subject'] = 'Playbook Report'
                msg['From'] = 'PRPIplaybooks@gmail.com'
                msg['To'] = toEmail
                
                #body = MIMEText("""Here is the updated playbook report""")
                enQuiryEmail='PRPIplaybooks@gmail.com'
                
                           
                emailContent+='<table width="100%" cellpadding="5">'               
                emailContent+='<tr><td>Dear '+mainContact.personnel.personsname+', <br/><br/>Thank you for updating the Playbook projects for <b>'+pml.nametouse+'</b>. Please find a revised Playbook report attached to this email which incorporates your most recent updates.</td></tr>'     
                emailContent+='<tr><td>If you have any questions or need assistance, please email <a href="mailto:'+enQuiryEmail+'">'+enQuiryEmail+'.</a></td></tr>'                    
                emailContent+='</table>'                
                emailContent+='<br/>'                
                emailContent+='<table width="100%" cellpadding="5">' 
                emailContent+='<tr><td>'
                emailContent+='Thank you,<br/>'
                emailContent+='The PRPI Team<br/>'
                emailContent+='<i>on behalf of</i><br/>'
                emailContent+='<img src="principal.jpg">'
                emailContent+='</td></tr>'
                emailContent+='</table>'
                
                body = MIMEText(emailContent, 'html')
                
                
                msg.attach(body)
                filename=propname+".pdf"            
                att = email.mime.application.MIMEApplication(response,_subtype="pdf")            
                att.add_header('Content-Disposition','attachment',filename=filename)
                msg.attach(att)
                s = smtplib.SMTP('***************')
                s.starttls()
                s.login('***************','***************')
                s.sendmail(fromEmail,[toEmail], msg.as_string())
                s.quit()  
                messages.success(request, "'"+pml.nametouse+ "' playbook report sent to "+toEmail) 
            except Exception as inst:
                messages.error(request, "unable to send '"+pml.nametouse+ "' playbook report due to: "+str(inst))   
        
    return HttpResponseRedirect("/admin/KUDZU/playbook/")