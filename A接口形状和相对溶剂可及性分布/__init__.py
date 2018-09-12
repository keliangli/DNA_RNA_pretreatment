import re
import os
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy


def Match_PDB_CA_ATOM(pdb_content):
    shape_m = re.match('.{82}Shape:(\w+)\s+racc:\s?(\S+)\s+',pdb_content)
    if shape_m == None:
        return 0
    else:
        shape_content = (shape_m.group(1),shape_m.group(2))
    return  shape_content

def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def excel_write(row, column, content):
    rb = open_workbook("E:\数据实验区\DNA_interface_溶剂可及性结果\相对溶剂可及性分布.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save("E:\数据实验区\DNA_interface_溶剂可及性结果\相对溶剂可及性分布.xls")



print("please input the shape path：")
shape_Path = input()
os.chdir(shape_Path)
print("you input shape path is :" ,os.getcwd())
shape_Path_listdir = os.listdir(shape_Path)

row_num = 0
for shape_file_name in shape_Path_listdir:
    # 读取pdb的文件的名字
    shape_handle = RE_PDB_content(shape_file_name)
    # 返回pdb文件的句柄，准备对于文件内容进行处理
    valley_number = 0
    flat_number   = 0
    peak_number   = 0
    valley_racc   = 0
    flat_racc     = 0
    peak_racc     = 0
    AA_interface_num = 0
    print(shape_file_name)
    for shape_content in shape_handle:
        shape = Match_PDB_CA_ATOM(shape_content)
        racc_num = float(shape[1])
        if shape[0] == 'valley':
            valley_racc = valley_racc + racc_num
            valley_number = valley_number + 1
        if shape[0] == 'flat':
            flat_racc = flat_racc + racc_num
            flat_number = flat_number + 1
        if shape[0] == 'peak':
            peak_racc   = peak_racc + racc_num
            peak_number = peak_number + 1


    if valley_number:
        valley_racc_result = valley_racc/valley_number
    else:
        valley_racc_result = 0
    if flat_number:
        flat_racc_result = flat_racc/flat_number
    else:
        flat_racc_result = 0

    if peak_number:
        peak_racc_result = peak_racc / peak_number
    else:
        peak_racc_result = 0


    #peak
    excel_write(row_num, 0, peak_racc_result)
    #flat
    excel_write(row_num, 1, flat_racc_result)
    #peak
    excel_write(row_num, 2, valley_racc_result)

    row_num = row_num + 1


