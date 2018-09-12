# 插入操作所需要的模块
import os
import os.path
import re
import excel.PDB_excel_module as PDB_excel_module


# 文件路径处理函数：
# 功能：将文件指针指向PDB文件所放路径；并且返回路径下面所有PDB文件名
# 输入参数： 无
# 返回参数：PDB文件名列表

def PDB_Shape_Read_Path_Process(PDB_Shape_Path):

    # 改变当前路径为PDB存放路径
    os.chdir(PDB_Shape_Path)
    shape_Path_listdir = os.listdir(PDB_Shape_Path)
    return shape_Path_listdir

# 文件内容处理函数：
# 功能：将输入的文件名下的所有内容都返回
# 输入参数： 文件名句柄
# 返回参数：PDB_shape_file内容


def PDB_Shape_File_Handle(pdb_shape_file):
    read_file_handle = open(pdb_shape_file, 'r')
    return read_file_handle

# 检测当前文件行的氨基酸类型：
# 功能：匹配当前行内容，并返回当前行的氨基酸类型
# 输入参数：文件行内容句柄
# 返回参数：当前行氨基酸类型

def PDB_Shape_File_AA_Type(pdb_shape_file_content):

    AA_Type_m = re.match('(\w+)\s+[0-9]*\s+\w+:\S?\w+.\w+\s+Shape:\w+\s+',pdb_shape_file_content)
    if AA_Type_m== None:
        return 0
    else:
        AA_Type = AA_Type_m.group(1)
        return  AA_Type

# 检测当前文件行的氨基酸形状类型：
# 功能：匹配当前行内容，并返回当前行的氨基酸形状类型
# 输入参数：文件行内容句柄
# 返回参数：当前行氨基酸形状类型

def PDB_Shape_File_Shape_Type(pdb_shape_file_content):

    Shape_Type_m = re.match('\w+\s+[0-9]*\s+\w+:\S?\w+.\w+\s+Shape:(\w+)\s+',pdb_shape_file_content)
    if Shape_Type_m== None:
        return 0
    else:
        Shape_Type = Shape_Type_m.group(1)
        return  Shape_Type


# 计算每个文件中不同形状的残基的特征值：
# 功能：计算没个文件内的不同形状的特征值
# 输入参数：txt文件句柄
# 返回参数：无

def PDB_Shape_Match_feature_calculate(shape_file_handle,AA_Type_feature_value):

    shape_file_content = PDB_Shape_File_Handle(shape_file_handle)

    valley_feature_Sum  = 0
    valley_Type_Num     = 0
    flat_feature_Sum    = 0
    flat_Type_Num       = 0
    peak_feature_Sum    = 0
    peak_Type_Num       = 0

    for shape_file_row in shape_file_content:
        AA_Type = PDB_Shape_File_AA_Type(shape_file_row)
        if len(AA_Type) == 4:
            AA_Type = AA_Type[1:4]
        Shape_Type = PDB_Shape_File_Shape_Type(shape_file_row)
        AA_Type_feature_counter = AA_Type_feature_value[AA_Type]
        if Shape_Type == "valley":
            valley_feature_Sum = valley_feature_Sum + AA_Type_feature_counter
            valley_Type_Num     = valley_Type_Num + 1
        elif Shape_Type == "falt":
            flat_feature_Sum = flat_feature_Sum + AA_Type_feature_counter
            flat_Type_Num     = flat_Type_Num + 1
        elif Shape_Type == "peak":
            peak_feature_Sum = peak_feature_Sum + AA_Type_feature_counter
            peak_Type_Num     = peak_Type_Num + 1

    if valley_Type_Num == 0:
        valley_feature_average = 0
    else:
        valley_feature_average = valley_feature_Sum / valley_Type_Num
    if flat_Type_Num == 0:
        flat_feature_average = 0
    else:
        flat_feature_average   = flat_feature_Sum   / flat_Type_Num
    if peak_Type_Num == 0:
        peak_feature_average = 0
    else:
        peak_feature_average   = peak_feature_Sum   / peak_Type_Num

    feature_value_tuple = (peak_feature_average,flat_feature_average,valley_feature_average)
    return feature_value_tuple

# pdb属性处理接口：
# 功能：为计算各种蛋白质属性并且打印到蛋白质性能特征excel文件
# 输入参数：每种属性的氨基酸所对应的值字典，pdb被处理文件存放路径，当前特征在excel表中存放的位置（列）
# 返回参数：无

def PDB_Shape_feature_Function(AA_Type_feature_value,PDB_Shape_Path,feature_column):

    shape_Path_listdir = PDB_Shape_Read_Path_Process(PDB_Shape_Path)

    #我们从第二行开始写入，第一行为属性名称
    row    = 1
    for shape_file_handle in shape_Path_listdir:
        feature_value_tuple = PDB_Shape_Match_feature_calculate(shape_file_handle,AA_Type_feature_value)
        #peak
        PDB_excel_module.Excel_Write(row, feature_column, 0, feature_value_tuple[0])
        #flat
        PDB_excel_module.Excel_Write(row, feature_column+1, 0, feature_value_tuple[1])
        #valley
        PDB_excel_module.Excel_Write(row, feature_column+2, 0, feature_value_tuple[2])
        row = row + 1






