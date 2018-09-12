import re
import os
from xlrd import open_workbook
from xlutils.copy import copy



electrostatic_num_dict = {'ARG':0,'ASP':0,'GLU':0,'HIS':0,'LYS':0}


electrostatic_result_dict = {'ARG':0,'ASP':0,'GLU':0,'HIS':0,'LYS':0}

def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM.{9}CA\s+([A-Z]+).{11}(\s+?\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).*',pdb_content)
    if CA_m == None:
        return 0
    else:
        CA_Conten_Tuple = (CA_m.group(1),CA_m.group(2),CA_m.group(3),CA_m.group(4))
    return  CA_Conten_Tuple

def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def excel_write(row, column, content):
    rb = open_workbook("E:\数据实验区\DNA接口氨基酸电荷分布情况\DNA_接口电荷分布情况.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save("E:\数据实验区\DNA接口氨基酸电荷分布情况\DNA_接口电荷分布情况.xls")



print("please input the interface path：")
interface_Path = input()
os.chdir(interface_Path)
print("you input shape path is :" ,os.getcwd())
interface_Path_listdir = os.listdir(interface_Path)

row_num = 0
interface_file_num = 0

for interface_file_name in interface_Path_listdir:
    # 读取pdb的文件的名字
    interface_handle = RE_PDB_content(interface_file_name)
    # 返回pdb文件的句柄，准备对于文件内容进行处理
    AA_interface_num = 0
    for interface_content in interface_handle:
        AA_type = Match_PDB_CA_ATOM(interface_content)
        AA_interface_num = AA_interface_num + 1
        if AA_type[0] == 'LYS':
            electrostatic_num_dict[AA_type[0]] = electrostatic_num_dict[AA_type[0]] + 1
        elif AA_type[0] == 'ARG':
            electrostatic_num_dict[AA_type[0]] = electrostatic_num_dict[AA_type[0]] + 1
        elif AA_type[0] == 'HIS':
            electrostatic_num_dict[AA_type[0]] = electrostatic_num_dict[AA_type[0]] + 1
        elif AA_type[0] == 'GLU':
            electrostatic_num_dict[AA_type[0]] = electrostatic_num_dict[AA_type[0]] - 1
        elif AA_type[0] == 'ASP':
            electrostatic_num_dict[AA_type[0]] = electrostatic_num_dict[AA_type[0]] - 1

    excel_write(interface_file_num,0,interface_file_name)
    cnt = 1
    for key in electrostatic_num_dict:
        electrostatic_result_dict[key] = electrostatic_num_dict[key]/AA_interface_num
        excel_write(interface_file_num,cnt,str(electrostatic_result_dict[key]))
        electrostatic_result_dict[key] = 0
        electrostatic_num_dict[key]    = 0
        cnt = cnt + 1

    print("                           ",cnt)
    print(interface_file_num)
    interface_file_num = interface_file_num + 1
