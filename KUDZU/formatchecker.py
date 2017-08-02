from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        #print "\n\n"
        #print kwargs.get("content_types")
        lister=[ 'application/pdf', 
            'image/jpeg',
            'image/png',
            'image/gif',
            'text/plain',
            'application/vnd.ms-excel',
            'application/octet-stream',
            'application/vnd.ms-powerpoint',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',            
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.ms-outlook' ]
        self.content_types = kwargs.pop("content_types",lister)        
        self.max_upload_size = kwargs.pop("max_upload_size",['2621440', '5242880','10485760','20971520'])
    
        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)
    
    def clean(self, *args, **kwargs):        
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
    
        file = data.file
        
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
    
        return data