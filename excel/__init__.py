import xlwt
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


