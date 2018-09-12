import re
import os
import shape_statistics.calu_pdb_shape as  calu_pdb_shape
import pdb_feature_caclu.pdb_feature_caclu as pdb_feature_caclu
import excel.PDB_excel_module as excel
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy
import numpy as np
import pandas as pd
import excel.PDB_excel_module as PDB_excel_module
from  sklearn import cross_validation
import sklearn.svm as svm

aaindex_attribute_dict = {'ALA': 0.83, 'ARG': 0.93, 'ASN': 0.89, 'ASP': 0.54,
                          'CYS': 1.19, 'GLN': 1.10, 'GLU': 0.37, 'GLY': 0.75,
                          'HIS': 0.87, 'ILE': 1.60, 'LEU': 1.30, 'LYS': 0.74,
                          'MET': 1.05, 'PHE': 1.38, 'PRO': 0.55, 'SER': 0.75,
                          'THR': 1.19, 'TRP': 1.37, 'TYR': 1.47, 'VAL': 1.70}

aaindex_predict_result_dict = {}


def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def aaindex_list_to_dict(aaindex_attribute_list, aaindex_attribute_dict):
    aaindex_attribute_dict['ALA'] = str(aaindex_attribute_list[0])
    aaindex_attribute_dict['ARG'] = str(aaindex_attribute_list[1])
    aaindex_attribute_dict['ASN'] = str(aaindex_attribute_list[2])
    aaindex_attribute_dict['ASP'] = str(aaindex_attribute_list[3])

    aaindex_attribute_dict['CYS'] = str(aaindex_attribute_list[4])
    aaindex_attribute_dict['GLN'] = str(aaindex_attribute_list[5])
    aaindex_attribute_dict['GLU'] = str(aaindex_attribute_list[6])
    aaindex_attribute_dict['GLY'] = str(aaindex_attribute_list[7])

    aaindex_attribute_dict['HIS'] = str(aaindex_attribute_list[8])
    aaindex_attribute_dict['ILE'] = str(aaindex_attribute_list[9])
    aaindex_attribute_dict['LEU'] = str(aaindex_attribute_list[10])
    aaindex_attribute_dict['LYS'] = str(aaindex_attribute_list[11])

    aaindex_attribute_dict['MET'] = str(aaindex_attribute_list[12])
    aaindex_attribute_dict['PHE'] = str(aaindex_attribute_list[13])
    aaindex_attribute_dict['PRO'] = str(aaindex_attribute_list[14])
    aaindex_attribute_dict['SER'] = str(aaindex_attribute_list[15])

    aaindex_attribute_dict['THR'] = str(aaindex_attribute_list[16])
    aaindex_attribute_dict['TRP'] = str(aaindex_attribute_list[17])
    aaindex_attribute_dict['TYR'] = str(aaindex_attribute_list[18])
    aaindex_attribute_dict['VAL'] = str(aaindex_attribute_list[19])


def excel_write(row, column, content):
    rb = open_workbook("E:\结合蛋白质分类项目8.12\数据处理过程文件\\aaindex_excel\\aaindex.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save("E:\结合蛋白质分类项目8.12\数据处理过程文件\\aaindex_excel\\aaindex.xls")


def Excel_Read(row, column):
    # 打开指定路径中的xls文件
    read_file = r'E:\结合蛋白质分类项目8.12\数据处理过程文件\aaindex_excel\\aaindex.xls'

    book = xlrd.open_workbook(read_file)  # 得到Excel文件的book对象
    # 得到sheet对象

    sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
    # 通过坐标读取表格中的数据

    cell_value = sheet0.cell_value(row, column)

    return cell_value



def PDB_Shape_File_Shape_Type(pdb_shape_file_content):

    Shape_Type_m = re.match('\w+\s+[0-9]*\s+\w+:\S?\w+.\w+\s+Shape:(\w+)\s+',pdb_shape_file_content)
    if Shape_Type_m== None:
        return 0
    else:
        Shape_Type = Shape_Type_m.group(1)
        return  Shape_Type



def AA_Type_feature_calu(shape_file_handle, aaindex_attribute_dict):
    shape_file_content = pdb_feature_caclu.PDB_Shape_File_Handle(shape_file_handle)

    feature_Sum = 0.0
    Type_Num = 0
    valley_feature_Sum = 0
    flat_feature_Sum   = 0
    peak_feature_Sum   = 0
    valley_Type_Num    = 0
    flat_Type_Num      = 0
    peak_Type_Num      = 0



    for shape_file_row in shape_file_content:
        #匹配氨基酸的类型
        AA_Type = pdb_feature_caclu.PDB_Shape_File_AA_Type(shape_file_row)
        if len(AA_Type) == 4:
            AA_Type = AA_Type[1:4]
        #从list中匹配对应的数值
        AA_Type_feature_value = float(aaindex_attribute_dict[AA_Type])
        #匹配相应形状类型
        Shape_Type = PDB_Shape_File_Shape_Type(shape_file_row)
        #匹配形状并且累加对应属性值
        if Shape_Type == "valley":
            valley_feature_Sum = valley_feature_Sum + AA_Type_feature_value
            valley_Type_Num     = valley_Type_Num + 1
        elif Shape_Type == "flat":
            flat_feature_Sum = flat_feature_Sum + AA_Type_feature_value
            flat_Type_Num     = flat_Type_Num + 1
        elif Shape_Type == "peak":
            peak_feature_Sum = peak_feature_Sum + AA_Type_feature_value
            peak_Type_Num     = peak_Type_Num + 1


    if  valley_Type_Num :
        valley_feature_average = valley_feature_Sum/valley_Type_Num
    else:
        valley_feature_average = 0

    if  flat_Type_Num :
        flat_feature_average = flat_feature_Sum/flat_Type_Num
    else:
        flat_feature_average = 0

    if  peak_Type_Num :
        peak_feature_average = peak_feature_Sum/peak_Type_Num
    else:
        peak_feature_average = 0

    feature_average = [valley_feature_average,flat_feature_average,peak_feature_average]

    return feature_average



def PDB_aaindex_feature_Function_DNA(PDB_Shape_Path, aaindex_attribute_dict, column):

    os.chdir(PDB_Shape_Path)
    shape_Path_listdir = pdb_feature_caclu.PDB_Shape_Read_Path_Process(PDB_Shape_Path)

    row = 0
    flag_row = 0
    for shape_file_handle in shape_Path_listdir:
        feature_value = AA_Type_feature_calu(shape_file_handle, aaindex_attribute_dict)
        #第1个valley
        excel_write(row, column, feature_value[0])
        #第2个valley
        excel_write(row, column+1,feature_value[1])
        #第3个valley
        excel_write(row, column+2, feature_value[2])
        row = row + 1

    while flag_row < row:
        excel_write(flag_row, column+3, 1)
        flag_row = flag_row + 1
    return row


def PDB_aaindex_feature_Function_RNA(PDB_Shape_Path, aaindex_attribute_dict, row, column):
    os.chdir(PDB_Shape_Path)
    shape_Path_listdir = pdb_feature_caclu.PDB_Shape_Read_Path_Process(PDB_Shape_Path)

    flag_row = row
    for shape_file_handle in shape_Path_listdir:
        feature_value = AA_Type_feature_calu(shape_file_handle, aaindex_attribute_dict)
        #第1个valley
        excel_write(row, column, feature_value[0])
        #第2个valley
        excel_write(row, column+1,feature_value[1])
        #第3个valley
        excel_write(row, column+2, feature_value[2])
        row = row + 1

    while flag_row < row:
        excel_write(flag_row, column+3, -1)
        flag_row = flag_row + 1
    return row


def aaindex_feature_svm_test(RNA_last_row, RNA_last_column):
    data = np.zeros((RNA_last_row, RNA_last_column))
    row_counter = 0
    column_counter = 0
    while row_counter < RNA_last_row:
        while column_counter < RNA_last_column:
            data[row_counter][column_counter] = Excel_Read(row_counter, column_counter)
            column_counter = column_counter + 1
        column_counter = 0
        row_counter = row_counter + 1
    row_counter = 0

    data_content = data[:, 0:RNA_last_column - 1]
    data_target = data[:, RNA_last_column - 1]

    lsvc = svm.LinearSVC()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(data_content, data_target, test_size=0.25,random_state=33)

    lsvc.fit(X_train, y_train)
    predict_result = lsvc.score(X_test, y_test)

    return predict_result


def match_aaindex_content_head(file_content):
    CA_head = re.match('(H) (\w+)', file_content)
    if CA_head == None:
        return 0
    else:
        return CA_head.group(2)


def match_aaindex_content_value(file_content):
    CA_value = re.match(
        '\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)',
        file_content)
    if CA_value == None:
        return 0
    else:
        match_aaindex_value_list = [CA_value.group(1), CA_value.group(2), CA_value.group(3), CA_value.group(4),CA_value.group(5),CA_value.group(6), CA_value.group(7), CA_value.group(8), CA_value.group(9),CA_value.group(10)]
        return match_aaindex_value_list


        # 提取aaindex属性值标志位：标志位为1表示提取的是属性头，标志位为2表示提取的第一行属性值，标志位为3表示提取的为第二行属性值


'''
    extract_aaindex_attribute_flag = 0
    aaindex_attribute_list1 = ()
    aaindex_attribute_list2 = ()
    aaindex_predict_result_dict = {}
    aaindex_ID = 'L'
    for file_content in file_handle:
        if extract_aaindex_attribute_flag == 0:
            if match_aaindex_content_head(file_content) != 0:
                extract_aaindex_attribute_flag = 1
                aaindex_ID = match_aaindex_content_head(file_content)
        if extract_aaindex_attribute_flag == 1:
            if match_aaindex_content_value(file_content)!= 0:
                aaindex_attribute_list1 = match_aaindex_content_value(file_content)
                extract_aaindex_attribute_flag = 2
        elif extract_aaindex_attribute_flag == 2:
            if match_aaindex_content_value(file_content) != 0:
                aaindex_attribute_list2 = match_aaindex_content_value(file_content)
                extract_aaindex_attribute_flag = 0
            aaindex_attribute_list = aaindex_attribute_list1+aaindex_attribute_list2
            aaindex_list_to_dict(aaindex_attribute_list, aaindex_attribute_dict)
            DNA_last_row = PDB_aaindex_feature_Function_DNA(PDB_DNA_Shape_Path, aaindex_attribute_dict,0)
            RNA_last_row = PDB_aaindex_feature_Function_RNA(PDB_RNA_Shape_Path, aaindex_attribute_dict,DNA_last_row,0)
            predict_result = aaindex_feature_svm_test(RNA_last_row,2)
            aaindex_predict_result_dict[aaindex_ID] = predict_result
    aaindex_predict_result_list = sorted(aaindex_predict_result_dict.items(), key=lambda item: item[1], reverse=True)
'''


def aaindex_attribute_process():
    print("请输入PDB_DNA_shape文件路径")
    PDB_DNA_Shape_Path = input()
    print("请输入PDB_RNA_shape文件路径")
    PDB_RNA_Shape_Path = input()

    aaindex_attribute_num = 0
    aaindex_excel_last_row = 0
    aaindex_excel_last_column = 0

    aaindex_attribute_list1 = ()
    aaindex_attribute_list2 = ()

    file_path = "E:\结合蛋白质分类项目8.12\数据处理过程文件\AA_index_file\output_aaindex.txt"
    file_aaindex_handle = RE_PDB_content(file_path)
    aaindex_attribute_num = 0
    for file_aaindex_content in file_aaindex_handle:
        if file_aaindex_content != '\n':
            str_content = str(file_aaindex_content[:-1])
            extract_aaindex_attribute_flag = 0
            file_handle = open("E:\结合蛋白质分类项目8.12\数据处理过程文件\AA_index_file\\aaindex.txt", 'r')
            for file_content in file_handle:
                if extract_aaindex_attribute_flag == 0:
                    if match_aaindex_content_head(file_content) != 0:
                        aaindex_name = match_aaindex_content_head(file_content)
                        if aaindex_name == str_content:
                            extract_aaindex_attribute_flag = 1
                if extract_aaindex_attribute_flag == 1:
                    if match_aaindex_content_value(file_content) != 0:
                        aaindex_attribute_list1 = match_aaindex_content_value(file_content)
                        extract_aaindex_attribute_flag = 2
                elif extract_aaindex_attribute_flag == 2:
                    if match_aaindex_content_value(file_content) != 0:
                        aaindex_attribute_list2 = match_aaindex_content_value(file_content)
                        extract_aaindex_attribute_flag = 0
                    aaindex_attribute_list = aaindex_attribute_list1 + aaindex_attribute_list2
                    aaindex_list_to_dict(aaindex_attribute_list, aaindex_attribute_dict)
                    DNA_last_row = PDB_aaindex_feature_Function_DNA(PDB_DNA_Shape_Path, aaindex_attribute_dict,aaindex_attribute_num*3)
                    RNA_last_row = PDB_aaindex_feature_Function_RNA(PDB_RNA_Shape_Path, aaindex_attribute_dict,DNA_last_row, aaindex_attribute_num*3)
                    aaindex_excel_last_row = RNA_last_row
            if aaindex_attribute_num < 39:
                aaindex_attribute_num = aaindex_attribute_num + 1
            else:
                aaindex_excel_last_column = aaindex_attribute_num
                break
    predict_result = aaindex_feature_svm_test(aaindex_excel_last_row, (aaindex_excel_last_column+1)*3+1)

    print(predict_result)


def main():
    aaindex_attribute_process()


main()
