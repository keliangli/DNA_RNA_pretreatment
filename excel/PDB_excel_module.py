import xlrd
from xlrd import open_workbook
from xlutils.copy import copy


# 对于excel文件进行追加写入操作：
# 功能：对于存在的excel文件进行修改，添加数据
# 输入参数：想要输入的行，列，表单，内容
# 返回参数：无


def Excel_Write(row,column,sheet,content):
    # 打开文件
    rb = open_workbook("F:\pdb_feature_sheet\pdb_feature.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(sheet)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save("F:\pdb_feature_sheet\pdb_feature.xls")



def Excel_PDB_type_Write(PDB_type,row,column,sheet,content):
    # 打开文件
    if PDB_type == 'DNA':
        rb = open_workbook("F:\pdb_feature_sheet\DNA_pdb_feature.xls")
    else:
        rb = open_workbook("F:\pdb_feature_sheet\RNA_pdb_feature.xls")

    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(sheet)
    # 写入数据
    s.write(row, column, content)
    # 保存
    if PDB_type == 'DNA':
        wb.save("F:\pdb_feature_sheet\DNA_pdb_feature.xls")
    else:
        wb.save("F:\pdb_feature_sheet\RNA_pdb_feature.xls")




def Excel_Read(PDB_type,row,column,sheet):
    # 打开指定路径中的xls文件
    if PDB_type == 'DNA':
        read_file = r'F:\pdb_feature_sheet\DNA_pdb_feature.xls'
    else:
        read_file = r'F:\pdb_feature_sheet\RNA_pdb_feature.xls'

    book = xlrd.open_workbook(read_file)  # 得到Excel文件的book对象
    # 得到sheet对象

    sheet0 = book.sheet_by_index(sheet)  # 通过sheet索引获得sheet对象
    # 通过坐标读取表格中的数据

    cell_value = sheet0.cell_value(row, column)

    return cell_value

def Excel_get_row_num(PDB_type,sheet):
    if PDB_type == 'DNA':
        read_file = r'F:\pdb_feature_sheet\DNA_pdb_feature.xls'
    else:
        read_file = r'F:\pdb_feature_sheet\RNA_pdb_feature.xls'
    book = xlrd.open_workbook(read_file)  # 得到Excel文件的book对象
    # 得到sheet对象
    sheet0 = book.sheet_by_index(sheet)  # 通过sheet索引获得sheet对象
    # 通过坐标读取表格中的数据
    row_num = sheet0.nrows
    return  row_num

def Excel_get_column_num(PDB_type,sheet):
    if PDB_type == 'DNA':
        read_file = r'F:\pdb_feature_sheet\DNA_pdb_feature.xls'
    else:
        read_file = r'F:\pdb_feature_sheet\RNA_pdb_feature.xls'
    book = xlrd.open_workbook(read_file)  # 得到Excel文件的book对象
    # 得到sheet对象
    sheet0 = book.sheet_by_index(sheet)  # 通过sheet索引获得sheet对象
    # 通过坐标读取表格中的数据
    column_num = sheet0.ncols
    return  column_num