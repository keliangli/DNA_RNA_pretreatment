import os.path
import re
import matplotlib.pyplot as plt;plt.rcdefaults()
import numpy as np
import excel.PDB_excel_module as PDB_excel_module


def PDB_Shape_Read_Path_Process(PDB_Shape_Path):

    # 改变当前路径为PDB存放路径
    os.chdir(PDB_Shape_Path)
    shape_Path_listdir = os.listdir(PDB_Shape_Path)
    return shape_Path_listdir

# 匹配凸区域
def match_shape_peak(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:peak\s+', shape_file_content)
    if shape_m==None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)

# 匹配平区域
def match_shape_flat(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:falt\s+', shape_file_content)
    if shape_m == None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)

# 匹配凹区域
def match_shape_valley(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:valley\s+', shape_file_content)
    if shape_m == None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)



#统计并且返回一个shape_file中各个形状的百分比
def PDB_Shape_calculate(shape_file_handle):

    pdb_peak_counter   = 0
    pdb_flat_counter   = 0
    pdb_valley_counter = 0
    pdb_AA_total       = 0
    shape_file = open(shape_file_handle, 'r')
    for shape_file_content in shape_file:
        pdb_AA_total = pdb_AA_total + 1
        peak_aa_type = match_shape_peak(shape_file_content)
        flat_aa_type = match_shape_flat(shape_file_content)
        valley_aa_type = match_shape_valley(shape_file_content)

        if peak_aa_type != 0:
            pdb_peak_counter = pdb_peak_counter + 1
        elif flat_aa_type != 0:
            pdb_flat_counter = pdb_flat_counter + 1
        elif valley_aa_type != 0:
            pdb_valley_counter = pdb_valley_counter + 1

    pdb_peak_percentage = pdb_peak_counter / pdb_AA_total
    pdb_flat_percentage = pdb_flat_counter / pdb_AA_total
    pdb_valley_percentage = pdb_valley_counter / pdb_AA_total

    pdb_shape_percentage_tuple = (pdb_peak_percentage,pdb_flat_percentage,pdb_valley_percentage)

    return pdb_shape_percentage_tuple


#将计算出的shape的比例打印到pdb_feature_excel中去
def PDB_Shape_Function(PDB_Shape_Path,featrue_column):

    shape_Path_listdir = PDB_Shape_Read_Path_Process(PDB_Shape_Path)

    #我们从第二行开始写入，第一行为属性名称
    row    = 1
    for shape_file_handle in shape_Path_listdir:
        shape_percentage_tuple = PDB_Shape_calculate(shape_file_handle)
        #peak
        PDB_excel_module.Excel_Write(row, featrue_column, 0, shape_percentage_tuple[0])
        #flat
        PDB_excel_module.Excel_Write(row, featrue_column+1, 0, shape_percentage_tuple[1])
        #valley
        PDB_excel_module.Excel_Write(row, featrue_column+2, 0, shape_percentage_tuple[2])
        row = row + 1


