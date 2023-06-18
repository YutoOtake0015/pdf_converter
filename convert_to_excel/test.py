import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views import generic

from .forms import UploadForm
from .utils import create_excel


def top(request):
    return render(request, 'convert_to_excel/top.html')

class UploadView(LoginRequiredMixin, generic.FormView):
    form_class = UploadForm
    template_name = 'convert_to_excel/upload_form.html'
    
    def form_valid(self, form):
        user_name = self.request.user.username
        user_dir = os.path.join(settings.MEDIA_ROOT, "excel", user_name) 
        
        # ユーザディレクトリ生成
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)
        
        # ランダムに生成されたフォルダ名を取得
        temp_dir = form.save() 
        
        # PDF -> Excelデータ生成
        err = create_excel(temp_dir, user_name)  #PDF->Excelデータ生成
        if err:
            shutil.rmtree(temp_dir)  #upload一時フォルダの削除
            context = {
                'err': err,
            }
            return render(self.request, 'pdfmr/complete.html', context)

        
        shutil.rmtree(temp_dir)
        
        # excelファイル一覧取得
        _, file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", user_name))
        message = "正常終了しました。"
        context = {
            'file_list': file_list,
            'user_name':user_name,
            'message': message,
        }
        return render(self.request, 'convert_to_excel/complete.html', context)

    def form_invalid(self, form):
        return render(self.request, 'convert_to_excel/upload_form.html', {'form': form})

class ListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'convert_to_excel/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 自分の作成したExcelファイルを一覧表示
        login_user_name = self.request.user.username
        
        # ファイル未作成時、エラーメッセージを返却
        if not default_storage.exists(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name)):
            warning_message = "このユーザでは一度もファイル作成が行われていません"
            context = {
                'warning_message': warning_message,
            }
            return context
        
        # 作成済みファイルを返却s
        file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name))[1]
        context = {
            'file_list': file_list, 
            'login_user_name': login_user_name,
        }
        return context

@login_required
def del_file(request):
    check_value = request.POST.getlist('checks')
    login_user_name = request.user.username
    
    if check_value:
        for file in check_value:
            path = os.path.join(settings.MEDIA_ROOT, "excel", login_user_name, file)
            default_storage.delete(path)
            
        return render(request, 'convert_to_excel/delete.html', {'check_value': check_value})
    else:
        login_user_name = request.user.username
        file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name))[1]
        warning_message = "削除対象ファイルが選択されていません。"
        
        context = { 
            'file_list': file_list,
            'login_user_name':login_user_name,
            'warning_message': warning_message,
        }
        return render(request, 'convert_to_excel/list.html',context)
    