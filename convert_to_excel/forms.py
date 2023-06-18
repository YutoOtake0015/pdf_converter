import os
import random
import string

from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from upload_validator import FileTypeValidator


class UploadForm(forms.Form):
    '''
    機能: PDFアップロードフォーム
    '''
    document = forms.FileField(label="PDFアップロード",
           widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), 
           validators=[FileTypeValidator(allowed_types=[ 'application/pdf'])]
           )

    def save(self):
        upload_files = self.files.getlist('document')
        temp_dir = os.path.join(settings.MEDIA_ROOT, self.create_dir(10))
        for pdf in upload_files:
            default_storage.save(os.path.join(temp_dir, pdf.name), pdf)
        return temp_dir
    
    def create_dir(self, n):
        # 一時フォルダ名生成
        return os.path.join('pdf', ''.join(random.choices(string.ascii_letters + string.digits, k=n)))
        # return 'pdf\\' + ''.join(random.choices(string.ascii_letters + string.digits, k=n))