import re
import os
from pdb_data_pretreatment.A7提供相对溶剂可及性查询接口 import check_pdb_RACC


def Match_shape_ATOM(content):
    CA_m = re.match('.{21}(\w)(\s{0,3})(\d+).*',content)
    if CA_m == None:
        return 0
    else:
        CA_Content_Tuple = (CA_m.group(1),CA_m.group(3))
    return  CA_Content_Tuple

def match_file_name(pdb_file_name):

    file_name = re.match('(\w+)shape\.txt',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)

def Print_shape_racc(shape_file_name,shape_content,racc_str):

    PDB_file_name = match_file_name(shape_file_name)
    file_name = PDB_file_name +'racc.data'
    Write_file_handle = open(file_name,'a')
    Write_file_handle.write(shape_content[:-1])
    Write_file_handle.write("  racc:")
    Write_file_handle.write(str(racc_str))
    Write_file_handle.write('\n')
    Write_file_handle.close()


print("please input the shape path：")
shape_Path = input()
os.chdir(shape_Path)
print("you input interface path is :", shape_Path)
shape_Path_listdir = os.listdir(shape_Path)

print("please input the AA type：")
AA_type = input()

for shape_file_name in shape_Path_listdir:
    shape_handle = open(shape_file_name, 'r')
    shape_name = match_file_name(shape_file_name)
    print(shape_name)
    for shape_content in shape_handle:
        shape_atom_content = Match_shape_ATOM(shape_content)
        racc_num = check_pdb_RACC(AA_type,shape_atom_content[0],shape_atom_content[1],shape_name)
        os.chdir(shape_Path)
        Print_shape_racc(shape_file_name, shape_content, racc_num)
    shape_handle.close()
