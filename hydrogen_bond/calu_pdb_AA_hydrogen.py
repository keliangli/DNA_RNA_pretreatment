# 插入操作所需要的模块
import os
import os.path
import re
import sys
sys.path.append('D:\python_prj\excel')
import PDB_excel_module


AA_Type_Hydrogen_value = {'ALA': 0, 'ARG': 4, 'ASN': 2, 'ASP': 1, 'CYS': 0, 'GLN': 2, 'GLU': 1, 'GLY': 0, 'HIS': 1, 'ILE': 0,
                          'LEU': 0, 'LYS': 2, 'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 1, 'THR': 1, 'TRP': 1, 'TYR': 1, 'VAL': 0}


# 文件路径处理函数：
# 功能：将文件指针指向PDB文件所放路径；并且返回路径下面所有PDB文件名
# 输入参数： 无
# 返回参数：PDB文件名列表

def PDB_Shape_Read_Path_Process(PDB_Shape_Path):

    # 改变当前路径为PDB存放路径
    os.chdir(PDB_Shape_Path)
    print("您输入的PDB文件存放路径为:",os.getcwd())
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

    AA_Type_m = re.match('(\w+)\s+SI:\w+.\w+\s+\w+:\w+',pdb_shape_file_content)
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

    Shape_Type_m = re.match('\w+\s+SI:\w+.\w+\s+\w+:(\w+)',pdb_shape_file_content)
    if Shape_Type_m== None:
        return 0
    else:
        Shape_Type = Shape_Type_m.group(1)
        return  Shape_Type


# 根据当前氨基酸的类型匹配并返回氢键值：
# 功能：匹配当前氨基酸类型，并返回其氢键值
# 输入参数：氨基酸类型
# 返回参数：当前行氨基酸氢键值

def PDB_Shape_Match_AA_Hydrogen_value(AA_Type):
    Hydrogen_value = AA_Type_Hydrogen_value[AA_Type]
    return  Hydrogen_value


# 计算每个文件中不同形状的残基的氢键值：
# 功能：计算没个文件内的不同形状的氢键值
# 输入参数：txt文件句柄
# 返回参数：无

def PDB_Shape_Match_Hydrogen_calculate(shape_file_handle):

    shape_file_content = PDB_Shape_File_Handle(shape_file_handle)

    valley_Hydrogen_Sum = 0
    valley_Type_Num     = 0
    flat_Hydrogen_Sum   = 0
    flat_Type_Num       = 0
    peak_Hydrogen_Sum   = 0
    peak_Type_Num       = 0


    for shape_file_row in shape_file_content:
        AA_Type = PDB_Shape_File_AA_Type(shape_file_row)
        Shape_Type = PDB_Shape_File_Shape_Type(shape_file_row)
        AA_Type_Hydrogen_value = PDB_Shape_Match_AA_Hydrogen_value(AA_Type)
        if Shape_Type == "valley":
            valley_Hydrogen_Sum = valley_Hydrogen_Sum + AA_Type_Hydrogen_value
            valley_Type_Num     = valley_Type_Num + 1
        elif Shape_Type == "flat":
            flat_Hydrogen_Sum = flat_Hydrogen_Sum + AA_Type_Hydrogen_value
            flat_Type_Num     = flat_Type_Num + 1
        elif Shape_Type == "peak":
            peak_Hydrogen_Sum = peak_Hydrogen_Sum + AA_Type_Hydrogen_value
            peak_Type_Num     = peak_Type_Num + 1

    valley_Hydrogen_average = valley_Hydrogen_Sum / valley_Type_Num
    flat_Hydrogen_average   = flat_Hydrogen_Sum   / flat_Type_Num
    peak_Hydrogen_average   = peak_Hydrogen_Sum   / peak_Type_Num

    Hydrogen_value_tuple = (peak_Hydrogen_average,flat_Hydrogen_average,valley_Hydrogen_average)
    return Hydrogen_value_tuple

# 文件下形状文件的三种形状的氢键平均值：
# 功能：计算三种形状的氢键值并且打印到蛋白质性能特征excel文件
# 输入参数：形状文件存放轮径
# 返回参数：无

def PDB_Shape_Hydrogen_Function(PDB_Shape_Path):

    shape_Path_listdir = PDB_Shape_Read_Path_Process(PDB_Shape_Path)

    #我们从第二行开始写入，第一行为属性名称
    row    = 1
    for shape_file_handle in shape_Path_listdir:
        Hydrogen_value_tuple = PDB_Shape_Match_Hydrogen_calculate(shape_file_handle)
        #peak
        Excel_Write(row, 4, 0, Hydrogen_value_tuple[0])
        #flat
        Excel_Write(row, 5, 0, Hydrogen_value_tuple[1])
        #valley
        Excel_Write(row, 6, 0, Hydrogen_value_tuple[2])
        row = row + 1







