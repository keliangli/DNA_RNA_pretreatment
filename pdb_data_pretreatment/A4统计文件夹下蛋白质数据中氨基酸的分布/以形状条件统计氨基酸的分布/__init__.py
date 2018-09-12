import os
import re



aatype_num_dict_peak = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                        'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                        'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                        'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                        'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


aatype_per_dict_peak = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                        'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                        'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                        'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                        'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}



aatype_num_dict_flat = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                        'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                        'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                        'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                        'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


aatype_per_dict_flat = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                        'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                        'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                        'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                        'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


aatype_num_dict_valley = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                          'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                          'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                          'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                          'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}


aatype_per_dict_valley = {'ALA': 0, 'ARG': 0, 'ASN': 0, 'ASP': 0,
                          'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0,
                          'HIS': 0, 'ILE': 0, 'LEU': 0, 'LYS': 0,
                          'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0,
                          'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}




def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def Match_aatype(PDB_aatype_content):
    aatype_m = re.match('(\w{3}).*Shape:(\w+)',PDB_aatype_content)
    if aatype_m == None:
        return 0
    else:
        return (aatype_m.group(1),aatype_m.group(2))




print("输入要统计的数据的路径：")

PDB_Path = input()
os.chdir(PDB_Path)
print("you input pdb path is :", os.getcwd())
PDB_Path_listdir = os.listdir(PDB_Path)


for pbd_shape_txt_name in PDB_Path_listdir:
    pdb_shape_txt_handle = RE_PDB_content(pbd_shape_txt_name)
    for pdb_shape_txt_content in pdb_shape_txt_handle:
        aatype = Match_aatype(pdb_shape_txt_content)
        if aatype[1] == 'peak':
            for key in aatype_num_dict_peak:
                if aatype[0] == key:
                    aatype_num_dict_peak[key] = aatype_num_dict_peak[key] + 1

        if aatype[1] == 'flat':
            for key in aatype_num_dict_flat:
                if aatype[0] == key:
                    aatype_num_dict_flat[key] = aatype_num_dict_flat[key] + 1


        if aatype[1] == 'valley':
            for key in aatype_num_dict_valley:
                if aatype[0] == key:
                    aatype_num_dict_valley[key] = aatype_num_dict_valley[key] + 1




value_sum_peak = 0
value_sum_flat = 0
value_sum_valley = 0




for key in aatype_num_dict_peak:
    value_sum_peak = value_sum_peak + aatype_num_dict_peak[key]

for key in aatype_num_dict_peak:
    aatype_per_dict_peak[key] = aatype_num_dict_peak[key]/value_sum_peak

for key in aatype_num_dict_valley:
    value_sum_flat = value_sum_flat + aatype_num_dict_valley[key]

for key in aatype_num_dict_valley:
    aatype_per_dict_valley[key] = aatype_num_dict_valley[key]/value_sum_flat


for key in aatype_num_dict_flat:
    value_sum_valley = value_sum_valley + aatype_num_dict_flat[key]

for key in aatype_num_dict_flat:
    aatype_per_dict_flat[key] = aatype_num_dict_flat[key]/value_sum_valley



print(aatype_num_dict_peak)
print(aatype_num_dict_flat)
print(aatype_num_dict_valley)
print(aatype_per_dict_valley)
print(aatype_per_dict_peak)
print(aatype_per_dict_flat)