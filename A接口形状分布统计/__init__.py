import re
import os
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy


def Match_PDB_CA_ATOM(pdb_content):
    shape_m = re.match('.{82}Shape:(\w+)',pdb_content)
    if shape_m == None:
        return 0
    else:
        shape_content = shape_m.group(1)
    return  shape_content

def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def excel_write(row, column, content):
    rb = open_workbook(r"E:\12.3\PDB_EXCEL\接口形状向量表\DNA接口形状向量表\接口形状向量表.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save(r"E:\12.3\PDB_EXCEL\接口形状向量表\DNA接口形状向量表\接口形状向量表.xls")



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
    AA_interface_num = 0
    print(shape_file_name)
    for shape_content in shape_handle:
        shape = Match_PDB_CA_ATOM(shape_content)
        AA_interface_num = AA_interface_num + 1
        if shape == 'valley':
            valley_number = valley_number + 1
        if shape == 'flat':
            flat_number = flat_number + 1
        if shape == 'peak':
            peak_number = peak_number + 1

    print(valley_number/AA_interface_num)
    print(flat_number/AA_interface_num)
    print(peak_number/AA_interface_num)

    #peak
    excel_write(row_num, 0, peak_number/AA_interface_num)
    #flat
    excel_write(row_num, 1, flat_number/AA_interface_num)
    #peak
    excel_write(row_num, 2, valley_number/AA_interface_num)

    row_num = row_num + 1


