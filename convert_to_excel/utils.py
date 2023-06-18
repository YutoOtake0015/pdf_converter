from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from glob import glob
from django.conf import settings
from .custmize import merge_excel
import os
import shutil
import openpyxl
import random, string
import time

def convert_pdf_to_txt(path):
    '''
    機能: PDFからデータを取得
    '''
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    fstr = ''
    for page in PDFPage.get_pages(fp, maxpages=maxpages):
        interpreter.process_page(page)

        str = retstr.getvalue()
        fstr += str

    fp.close()
    device.close()
    retstr.close()
    return fstr

def create_excel(upload_dir, user_name):
    '''
    機能: PDFのデータを持つExcelファイルを生成
    '''
    # アップロードファイルの取り込み
    upload_path = os.path.join(upload_dir, "*.pdf")    
    template_file = os.path.join(settings.MEDIA_ROOT, "template", "請求書一覧ファイル.xlsx")
    time_str = time.strftime("%Y%m%d-%H%M%S")
    work_file =os.path.join(settings.MEDIA_ROOT, "temp", "請求書一覧ファイル_" + time_str + ".xlsx")  
    user_dir = os.path.join(settings.MEDIA_ROOT , "excel", user_name) 
    file_list = glob(upload_path)
    shutil.copyfile(template_file, work_file)
    book = openpyxl.load_workbook(work_file)
    
    result_list =[]
    for pdf in file_list:
        result_txt = convert_pdf_to_txt(pdf)
        result_list.append(result_txt)
    
    err = merge_excel(book ,result_list, work_file) #Excelにデータをセット      
    if err:
        return err
    #個人ディレクトリへコピー
    shutil.move(work_file, user_dir)

