'''
Created on Jun 17, 2016

@author: Jack Yu - ITJDM
'''
# -*- coding: UTF-8 -*-
import os
from mysite.settings import BASE_DIR
import datetime
from django.core.mail import EmailMessage



def sendAutomationEmail(emailValues):
    enQuiryEmail='PRPIplaybooks@jdmgmt.com'

    #subject=emailValues['propertyName']+': Quarterly Playbook Status Update – Action Required'
    subject='PRPI Playbooks: Status Update Required for '+emailValues['propertyName']
    
    #emailContent='<table width="100%" cellpadding="5">'
    #emailContent+='<tr><td>Dear '+emailValues['toName']+',</td></tr>'
    #emailContent+='</table>' 
    emailContent='<table width="100%" cellpadding="5">'
    emailContent+='<tr><td>Dear '+emailValues['toName']+',<br/><br/>Please review and report on the status of your Playbook projects for '+emailValues['propertyName']+' by clicking on this link: <a href="'+emailValues['linkToUpdate']+'">'+emailValues['linkToUpdate']+'</a>. If your project statuses have not changed, you have the option to select “no change” in the online form.</td></tr>'    
    emailContent+='<tr><td>If you have any questions or need assistance, please email <a href="mailto:'+enQuiryEmail+'">'+enQuiryEmail+'.</a></td></tr>'
    emailContent+='</table>'
    
    emailContent+='<br/>'
    
    emailContent+='<table width="100%" cellpadding="5">' 
    emailContent+='<tr><td>'
    emailContent+='Thank you,<br/>'
    emailContent+='The PRPI Team<br/>'
    emailContent+='<i>on behalf of</i><br/>'
    emailContent+='<img src="https://data.jdmgmt.com/static/performancereport/resources/principal.jpg">'
    emailContent+='</td></tr>'
    
    #emailContent+='<tr><td>The PRPI Team</td></tr>'    
    #emailContent+='<tr><td>on behalf of</td></tr>'    
    #emailContent+='<tr><td><img src="https://data.jdmgmt.com/static/performancereport/resources/principal.jpg"></td></tr>'    
    emailContent+='</table>'
    
    #emailValues['toEmail']='developerfordevelopment@gmail.com'
           
    try:
        email = EmailMessage(subject, emailContent, to=[emailValues['toEmail']])
        email.content_subtype = "html"  
        email.send()
        return True
    except Exception as e:          
        return str(e)   
        
def sendAutomationNotificerToSender(emailValues):  

    subject=emailValues['propertyName']+': Quarterly Playbook Status Update – Complete'
    enQuiryEmail='PRPIplaybooks@jdmgmt.com'
    
    
    
    
    
    emailContent='<table width="100%" cellpadding="5">'
    emailContent+='<tr><td>Dear '+emailValues['toName']+', <br/> <br/>The Playbook project status for <b>'+emailValues['propertyName']+'</b> has been updated.</td></tr>'    
    #emailContent+='<tr><td>Thank you for updating the Playbook projects for <b>'+emailValues['propertyName']+'</b>. Please find an updated Playbook report attached to this email which incorporates your most recent updates.</td></tr>'
    #emailContent+='<tr><td>If you have any questions or need assistance, please email <a href="mailto:'+enQuiryEmail+'">'+enQuiryEmail+'.</a></td></tr>'    
    emailContent+='</table>'
    
    #emailValues['toEmail']='developerfordevelopment@gmail.com'
    
    emailContent+='<br/>'   
    try:
        email = EmailMessage(subject, emailContent, to=[emailValues['toEmail']],cc=['PRPIplaybooks@jdmgmt.com']) 
        email.content_subtype = "html"  
        email.send()
        return True
    except:
        return False  
        
def sendAutomationUpdateNotificationEmail(emailValues):    
    enQuiryEmail='PRPIplaybooks@jdmgmt.com'
    subject=emailValues['propertyName']+': Quarterly Playbook Status Update – Complete'
      
  
    emailContent='<table width="100%" cellpadding="5">'
    #emailContent+='<tr><td>Thank you for updating the Playbook project status for <b>'+emailValues['propertyName']+'</b>. Your submission has been received by JDM Associates</td></tr>'
    #emailContent+='<tr><td>If you have any questions or need assistance, please email <a href="mailto:'+emailValues['userEmail']+'">'+emailValues['userEmail']+'.</a></td></tr>'
    emailContent+='<tr><td>Dear '+emailValues['toName']+',<br/><br/>Thank you for updating the Playbook project status for <b>'+emailValues['propertyName']+'</b>. Your submission has been received by JDM Associates.</td></tr>'
    #emailContent+='<tr><td>If you have any questions or need assistance, please email <a href="mailto:'+enQuiryEmail+'">'+enQuiryEmail+'.</a></td></tr>'
    emailContent+='</table>'
    
    emailContent+='<br/>'
    
    emailContent+='<table width="100%" cellpadding="5">' 
    emailContent+='<tr><td>'
    emailContent+='Thank you,<br/>'
    emailContent+='The PRPI Team<br/>'
    emailContent+='<i>on behalf of</i><br/>'
    emailContent+='<img src="https://data.jdmgmt.com/static/performancereport/resources/principal.jpg">'
    emailContent+='</td></tr>' 
    emailContent+='</table>'
    #emailValues['toEmail']='developerfordevelopment@gmail.com'
    try:
        email = EmailMessage(subject, emailContent, to=[emailValues['toEmail']])
        email.content_subtype = "html"  
        email.send()
        return True
    except:
        return False