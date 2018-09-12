import os
import re



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




def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def Match_aatype(PDB_aatype_content):
    aatype_m = re.match('ATOM\s+[0-9]+\s+CA\s+([A-Z]+)\s+(\w+)\s+(\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).+',PDB_aatype_content)
    if aatype_m == None:
        return 0
    else:
        return aatype_m.group(1)




print("输入要统计的数据的路径：")

PDB_Path = input()
os.chdir(PDB_Path)
print("you input pdb path is :", os.getcwd())
PDB_Path_listdir = os.listdir(PDB_Path)


for pbd_shape_txt_name in PDB_Path_listdir:
    pdb_shape_txt_handle = RE_PDB_content(pbd_shape_txt_name)
    for pdb_shape_txt_content in pdb_shape_txt_handle:
        aatype = Match_aatype(pdb_shape_txt_content)
        for key in aatype_num_dict:
            if aatype == key:
                aatype_num_dict[key] = aatype_num_dict[key] + 1



value_sum = 0

for key in aatype_num_dict:
    value_sum = value_sum + aatype_num_dict[key]

for key in aatype_num_dict:
    aatype_per_dict[key] = aatype_num_dict[key]/value_sum

print(aatype_num_dict)

print(value_sum)

print(aatype_per_dict)