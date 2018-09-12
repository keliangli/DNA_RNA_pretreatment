
import os
import re
import numpy
from xlrd import open_workbook
from xlutils.copy import copy



aatype_num_dict = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                   'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                   'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                   'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                   'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


aatype_per_dict = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                   'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                   'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                   'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                   'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}

aatype_total_per_dict = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                         'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                         'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                         'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                         'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle





def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM.{9}CA\s+([A-Z]+).{11}(\s+?\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).*',pdb_content)
    if CA_m == None:
        return 0
    else:
        CA_Conten_Tuple = (CA_m.group(1),CA_m.group(2),CA_m.group(3),CA_m.group(4))
    return  CA_Conten_Tuple



def Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate,ATOM_Coordinate):

    CA_Coordinate_X   = float(CA_ATOM_Coordinate[1])
    CA_Coordinate_Y   = float(CA_ATOM_Coordinate[2])
    CA_Coordinate_Z   = float(CA_ATOM_Coordinate[3])
    ATOM_Coordinate_X = float(ATOM_Coordinate[1])
    ATOM_Coordinate_Y = float(ATOM_Coordinate[2])
    ATOM_Coordinate_Z = float(ATOM_Coordinate[3])

    vector1 = numpy.array((CA_Coordinate_X,CA_Coordinate_Y,CA_Coordinate_Z))
    vector2 = numpy.array((ATOM_Coordinate_X,ATOM_Coordinate_Y,ATOM_Coordinate_Z))

    ATOM_Euclid_Dis = numpy.sqrt(numpy.sum((vector1-vector2)**2))

    return ATOM_Euclid_Dis


def match_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.txt',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)


def match_pbd_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.pdb',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)


def Calcu_AA_shere_num(PDB_Path,interface_file_name,CA_ATOM_Coordinate):

    Valid_ATOM_count = 0
    os.chdir(PDB_Path)
    PDB_Path_listdir = os.listdir(PDB_Path)

    for key in aatype_per_dict:
        aatype_per_dict[key] = 0

    for key in aatype_num_dict:
        aatype_num_dict[key] = 0

    for pdb_file_name in PDB_Path_listdir:
        pdb_name = match_pbd_file_name(pdb_file_name)
        interface_name = match_file_name(interface_file_name)
        if pdb_name == interface_name:
            pdb_handle = RE_PDB_content(pdb_file_name)
            for pdb_content in pdb_handle:
                ATOM_Coordinate = Match_PDB_CA_ATOM(pdb_content)
                if (ATOM_Coordinate !=0):
                    Valid_ATOM_Dis = Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate, ATOM_Coordinate)
                    if 0<Valid_ATOM_Dis<12 :
                        Valid_ATOM_count = Valid_ATOM_count + 1
                        for key in aatype_num_dict:
                            if ATOM_Coordinate[0] == key:
                                aatype_num_dict[key] = aatype_num_dict[key] + 1


    for key in aatype_per_dict:
        if Valid_ATOM_count:
            aatype_per_dict[key] = aatype_num_dict[key]/Valid_ATOM_count
        else:
            aatype_per_dict[key] = 0
            print("这个是0")
            print(interface_file_name)

    return aatype_per_dict


def excel_write(row, column, content):
    rb = open_workbook("E:\数据实验区\DNA接口氨基酸周围氨基酸分布\DNA_接口氨基酸分布.xls")
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save("E:\数据实验区\DNA接口氨基酸周围氨基酸分布\DNA_接口氨基酸分布.xls")



print("输入要统计的接口数据的路径：")

interface_Path = input()
os.chdir(interface_Path)
print("you input interface path is :", os.getcwd())
interface_Path_listdir = os.listdir(interface_Path)

print("please input the pdb path：")
PDB_Path = input()
print("you input pdb path is :", PDB_Path)


interface_file_num = 0

for interface_file_name in interface_Path_listdir:
    # 读取pdb的文件的名字
    interface_handle = RE_PDB_content(interface_file_name)
    interface_num = 0
    for interface_content in interface_handle:
        CA_atom_coordinate = Match_PDB_CA_ATOM(interface_content)
        aatype_per = Calcu_AA_shere_num(PDB_Path,interface_file_name,CA_atom_coordinate)
        os.chdir(interface_Path)
        interface_num = interface_num + 1
        for key in aatype_total_per_dict:
            aatype_total_per_dict[key] = aatype_total_per_dict[key] + aatype_per[key]

    excel_write(interface_file_num,0, interface_file_name)
    cnt  = 1
    for key in aatype_total_per_dict:
        aatype_total_per_dict[key] = aatype_total_per_dict[key]/interface_num
        excel_write(interface_file_num,cnt,str(aatype_total_per_dict[key]))
        aatype_total_per_dict[key] = 0
        cnt = cnt + 1

    print("          ",cnt)
    print(interface_file_num)
    interface_file_num = interface_file_num + 1