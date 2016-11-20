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
from dryLab.models import Analysis, SequencingRun, SeqencingFile
import json
from _collections import OrderedDict
from wetLab.models import Biosample


@login_required 
def exportExperiment(request):
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

def orderByNumber(jsonDict):
    jsonList = jsonDict.items()
    sorted_list = sorted(jsonList, key=lambda k: (int(k[1]['order'])))
    sorted_dict= OrderedDict(sorted_list)
    return sorted_dict

    
def export(analysisType,ws, projectId):
    dbdata = Analysis.objects.filter(analysis_exp__project=projectId)
    if (dbdata):
        row_num = 0
        for a in dbdata:
            field_names = [x.name for x in a._meta.local_fields]
            break
        columns = []
        for names in field_names:
            if(names == "analysis_fields"):
                jsonObj = JsonObjField.objects.get(field_name=analysisType)
                jsonFields = orderByNumber(jsonObj.field_set)
                for keys in jsonFields:
                    columns.append((keys, 4000))
            elif(names == "analysis_import"):
                pass
            else:
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
                if(field == "analysis_fields"):
                    json_data = json.loads(att)
                    for keys in jsonFields:
                        json_val = json_data[keys]
                        row.append(json_val)
                elif(field == "analysis_import"):
                    pass
                else:
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
    
    pros = list(set([x.experiment_protocol.protocol_type.field_name for x in pro]))
    

    for protocol in pros:
        if protocol == "Hi-C Protocol":
            analysisType = "Hi-C Analysis"
            ws = wb.add_sheet('Hi-C')
            export(analysisType,ws, projectId)
             
        elif protocol == "3C Protocol":
            analysisType = "3C Analysis"
            ws = wb.add_sheet('3C')
            export(analysisType,ws, projectId)
             
        elif protocol == "5C Protocol":
            analysisType = "5C Analysis"
            ws = wb.add_sheet('5C')
            export(analysisType,ws, projectId)
        
        elif protocol == "CaptureC Protocol":
            analysisType = "CaptureC Analysis"
            ws = wb.add_sheet('CaptureC')
            export(analysisType,ws, projectId)
             
        else:
            pass
    wb.save(response)
    return response


@login_required 
def exportGEO(request):
    projectId = request.session['projectId']
    prj = Project.objects.get(pk=projectId)
    runUnits = SequencingRun.objects.filter(project=projectId)
    files = SeqencingFile.objects.filter(sequencingFile_exp__project=projectId)
    experiments = Experiment.objects.filter(project=projectId)
    bioSample = Biosample.objects.filter(expBio__project=projectId)
    
    title = prj.project_name
    summary = prj.project_notes
    contributor1 = str(prj.project_owner)
    contributor2 = prj.project_contributor.all()
    membersList = []
    for values in contributor2:
        membersList.append(values)
    
 
     
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GEO.xlsx'
    file_path_new = WORKSPACEPATH+'/organization/static/siteWide/geo_template_new.xlsx'
 
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
     
         
    for sample in bioSample:
        insert_rows(ws, row_idx= sampleRowNo, cnt = 1, above=False, copy_style=False)
        ws.cell(row=sampleRowNo, column=1).value = "Sample " + str(count)
        ws.cell(row=sampleRowNo, column=2).value = str(sample.biosample_name)
        ws.cell(row=sampleRowNo, column=3).value = str(sample.biosample_biosource.biosource_tissue)
        ws.cell(row=sampleRowNo, column=4).value = str(sample.biosample_individual.individual_type)
        ws.cell(row=sampleRowNo, column=5).value = str(sample.biosample_protocol.protocol_type)
        ws.cell(row=sampleRowNo, column=6).value = str(sample.biosample_protocol.protocol_enzyme) 
        ws.cell(row=sampleRowNo, column=7).value = str(sample.biosample_biosource.biosource_cell_line)  
        ws.cell(row=sampleRowNo, column=8).value = str("DNA")
        ws.cell(row=sampleRowNo, column=9).value = str(sample.biosample_biosource.biosource_description)
         
        sampleRowNo += 1
        count += 1
     
    rowNo = ws.max_row
    for i in range (rowNo):
        if((ws.cell(row=i+1, column=1).value)=="RAW FILES"):
            rawFilesRowNo = i+3
            break
     
     
    for file in files:
        insert_rows(ws, row_idx= rawFilesRowNo, cnt = 1, above=True, copy_style=False)
        ws.cell(row=rawFilesRowNo, column=1).value = str(file.sequencingFile_name)
        ws.cell(row=rawFilesRowNo, column=3).value = str(file.sequencingFile_sha256sum)
#         ws.cell(row=rawFilesRowNo, column=5).value = str(file.number_of_reads)
         
        rawFilesRowNo += 1
 
    wb.save(response)
    return response
    