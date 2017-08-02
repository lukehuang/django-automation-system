from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from KUDZU import views

urlpatterns = [    
    url(r'^playbook/automation/', views.automation,name='automation'),
    url(r'^automation/update/(?P<history_id>[0-9]+)', views.automation_status_update,name='automation-status-update'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
