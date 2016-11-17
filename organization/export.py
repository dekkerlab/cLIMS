'''
Created on Nov 15, 2016

@author: nanda
'''
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from organization.models import *
import csv
import xlwt
from xlwt.compat import xrange
from openpyxl.reader.excel import load_workbook
from organization.excelRow import insert_rows
from openpyxl.styles import Color, Fill
from cLIMS.base import WORKSPACEPATH


@login_required 
def exportSample(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="meta_data_sample.csv"'
    projectId = request.session['projectId']
    dbdata = Experiment.objects.filter(project=projectId)
    writer = csv.writer(response)
    for a in dbdata:
        field_names = [x.name for x in a._meta.local_fields]
        break
    writer.writerow(field_names)
    for obj in dbdata:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

def export(formData,ws, projectId):
    dbdata = formData.objects.filter(sample__project=projectId)
    if (dbdata):
        row_num = 0
        for a in dbdata:
            field_names = [x.name for x in a._meta.local_fields]
            break
        columns = []
        for names in field_names:
            columns.append((names, 4000))
    
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
    
        for col_num in xrange(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]
    
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        
        
        for obj in dbdata:
            row_num += 1
            row = []
            for field in field_names:
                att = getattr(obj, field)
                if ((type(att) != int) and (type(att) != str)):
                    att = str(att)
                row.append(att)
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    else:
        pass
    
         
@login_required 
def exportAnalysis(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    
    projectId = request.session['projectId']
    pro = Experiment.objects.filter(project=projectId)
    
    pros = list(set([x.experiment_protocol.name for x in pro]))

#     for protocol in pros:
#         if protocol == "Hi-C":
#             formData = HiCAnalysis
#             ws = wb.add_sheet('Hi-C')
#             export(formData,ws, projectId)
#             
#         elif protocol == "3C":
#             formData = ThreeCAnalysis
#             ws = wb.add_sheet('3C')
#             export(formData,ws, projectId)
#             
#         elif protocol == "5C":
#             formData = FiveCAnalysis
#             ws = wb.add_sheet('5C')
#             export(formData,ws, projectId)
#             
#         else:
#             pass
    wb.save(response)
    return response


@login_required 
def exportGEO(request):
    
    projectId = request.session['projectId']
    prj = Project.objects.get(pk=projectId)
#     #units = Lane.objects.filter(project=projectId)
#     files = DeepSeqFile.objects.filter(project=projectId)
#     samples = Sample.objects.filter(project=projectId)
    
    title = prj.name
    summary = prj.notes
    contributor1 = str(prj.owner)
    contributor2 = prj.members.all()
    membersList = []
    for values in contributor2:
        membersList.append(values)
    

    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GEO.xlsx'
    file_path_new = WORKSPACEPATH+'/organization/static/siteWide/geo_template_new.xlsx'
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #file_path_new = os.path.join(BASE_DIR, '/USys/main/static/main/geo_template_new.xlsx'),

    wb = load_workbook(file_path_new)
    ws = wb.worksheets[0]
    ws.insert_rows = insert_rows
    
    ws.cell(row=9, column=2).value = title
    ws.cell(row=10, column=2).value = summary
    ws.cell(row=12, column=2).value = contributor1
    
    memberRowNo = 13
    for members in membersList:
        insert_rows(ws, row_idx= memberRowNo, cnt = 1, above=True, copy_style=True)
        ws.cell(row=memberRowNo, column=1).value = "contributor"
        ws.cell(row=memberRowNo, column=2).value = str(members)
        
        memberRowNo +=1
    
    rowNo = ws.max_row
    for i in range (rowNo):
        if((ws.cell(row=i+1, column=1).value)=="Sample name"):
            sampleRowNo = i+2
            break
    
    count = 1
    
#         
#     for sample in samples:
#         insert_rows(ws, row_idx= sampleRowNo, cnt = 1, above=False, copy_style=False)
#         ws.cell(row=sampleRowNo, column=1).value = "Sample " + str(count)
#         ws.cell(row=sampleRowNo, column=2).value = str(sample.name)
#         ws.cell(row=sampleRowNo, column=4).value = str(sample.organism)
#         ws.cell(row=sampleRowNo, column=5).value = str(sample.protocol)
#         ws.cell(row=sampleRowNo, column=6).value = str(sample.enzyme) 
#         ws.cell(row=sampleRowNo, column=7).value = str(sample.cell_line)  
#         ws.cell(row=sampleRowNo, column=8).value = str(sample.molecule)
#         ws.cell(row=sampleRowNo, column=9).value = str(sample.notes)
#         
#         sampleRowNo += 1
#         count += 1
#     
#     rowNo = ws.max_row
#     for i in range (rowNo):
#         if((ws.cell(row=i+1, column=1).value)=="RAW FILES"):
#             rawFilesRowNo = i+3
#             break
#     
#     
#     for file in files:
#         insert_rows(ws, row_idx= rawFilesRowNo, cnt = 1, above=True, copy_style=False)
#         ws.cell(row=rawFilesRowNo, column=1).value = str(file.name)
#         ws.cell(row=rawFilesRowNo, column=3).value = str(file.sha256sum)
#         ws.cell(row=rawFilesRowNo, column=5).value = str(file.number_of_reads)
#         
#         rawFilesRowNo += 1

    wb.save(response)
    return response
    