#                     计算步骤
#       1，根据dssp文件中对应数字氨基酸的溶剂可及性面积ACC，和氨基酸最大溶剂可及性值计算相对溶剂可及性，
#            使用标准只要是有裸露的氨基酸都是有意义的9%
#                                      |
#                                      |
#       2，根据第一步中选择的氨基酸，计算其形状，并且保存shape.txt中，同时保存氨基酸的序列号
#
import re
import os



aaindex_ACC_dict = {'ALA': 115, 'ARG': 225, 'ASN': 160, 'ASP': 150,
                    'CYS': 135, 'GLN': 180, 'GLU': 190, 'GLY': 75,
                    'HIS': 195, 'ILE': 175, 'LEU': 170, 'LYS': 200,
                    'MET': 185, 'PHE': 210, 'PRO': 145, 'SER': 115,
                    'THR': 140, 'TRP': 255, 'TYR': 230, 'VAL': 155}

def AA_type_tran(one):
    if one == 'A':
        return 'ALA'
    elif one == 'L':
        return 'LEU'
    elif one == 'I':
        return 'ILE'
    elif one == 'V':
        return 'VAL'
    elif one == 'G':
        return 'GLY'
    elif one == 'N':
        return 'ASN'
    elif one == 'Q':
        return 'GLN'
    elif one == 'C':
        return 'CYS'
    elif one == 'M':
        return 'MET'
    elif one == 'P':
        return 'PRO'
    elif one == 'K':
        return 'LYS'
    elif one == 'R':
        return 'ARG'
    elif one == 'D':
        return 'ASP'
    elif one == 'E':
        return 'GLU'
    elif one == 'H':
        return 'HIS'
    elif one == 'S':
        return 'SER'
    elif one == 'T':
        return 'THR'
    elif one == 'Y':
        return 'TYR'
    elif one == 'W':
        return 'TRP'
    elif one == 'F':
        return 'PHE'


def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def match_dssp_content(dssp_file_content):

    Shape_Type_m = re.match('\s+\d+\s+(\d+)\s([A-Z])\s([A-Z])(.{3}).{17}\s{1,3}(\d+).*',dssp_file_content)
    if Shape_Type_m== None:
        return 0
    else:
        Shape_Type = (Shape_Type_m.group(1),Shape_Type_m.group(2),Shape_Type_m.group(3),Shape_Type_m.group(5),Shape_Type_m.group(4))
        print(Shape_Type)
        return  Shape_Type


def realtive_ACC_calcu(dssp_content):
    aa_type = AA_type_tran(dssp_content[2])
    if dssp_content[2] == 'X':
        return  0
    else:
        ACC_max = aaindex_ACC_dict [aa_type]
    ACC = float(dssp_content[3])

    realtive_ACC = ACC/ACC_max

    #return realtive_ACC
    return ACC

def calcu_relative_solvent_sccessiblity():

    print("please input the dssp path：")
    PDB_Path = input()
    os.chdir(PDB_Path)
    print("you input pdb path is :", os.getcwd())
    PDB_Path_listdir = os.listdir(PDB_Path)

    for dssp_file in PDB_Path_listdir:
        file_name = dssp_file + '.txt'
        Write_file_handle = open(file_name, 'a')
        dssp_file_handle = RE_PDB_content(dssp_file)
        print(dssp_file)
        for dssp_file_content in dssp_file_handle:
            dssp_content = match_dssp_content(dssp_file_content)
            if dssp_content:
                print(dssp_content)
                if realtive_ACC_calcu(dssp_content):
                    Write_file_handle.write("chain_ID: ")
                    Write_file_handle.write(str(dssp_content[1]))
                    Write_file_handle.write("  chain_num: ")
                    Write_file_handle.write(str(dssp_content[0]))
                    Write_file_handle.write("  SS_type: ")
                    Write_file_handle.write(str(dssp_content[4]))
                    Write_file_handle.write("  relative_ACC: ")
                    Write_file_handle.write(str(realtive_ACC_calcu(dssp_content)))

                    Write_file_handle.write("\n")


def main():
    calcu_relative_solvent_sccessiblity()


main()