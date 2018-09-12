
import os
import re


def match_racc_pdb_name(racc_file_name):

    Shape_Type_m = re.match('(\S+.pdb).dssp.txt',racc_file_name)
    if Shape_Type_m== None:
        return 0
    else:
        return Shape_Type_m.group(1)


def match_racc_content(racc_file_content):

    Shape_Type_m = re.match('chain_ID: (\w+)\s+chain_num: (\d+).*',racc_file_content)
    if Shape_Type_m== None:
        return 0
    else:
        return (Shape_Type_m.group(1),Shape_Type_m.group(2))



def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def check_pdb_RACC(pdb_type,chain_id,aa_nume,pdb_file_name):

    if pdb_type == 'DNA':
        PDB_Path = "E:\结合蛋白质分类项目8.12\数据预处理\\3数据分类前处理\数据容积可及性处理\计算溶剂可及性\PDB_DNA_binding_protein计算相对溶剂可及性之后得到的文件"
    else:
        PDB_Path = "E:\结合蛋白质分类项目8.12\数据预处理\\3数据分类前处理\数据容积可及性处理\计算溶剂可及性\PDB_RNA_binding_protein计算相对溶剂可及性之后得到的文件"
    os.chdir(PDB_Path)

    PDB_Path_listdir = os.listdir(PDB_Path)

    for racc_file_name in PDB_Path_listdir:
        racc_pdb_name = match_racc_pdb_name(racc_file_name)
        if racc_pdb_name == pdb_file_name:
            racc_file_handle = RE_PDB_content(racc_file_name)
            for racc_file_content in racc_file_handle:
                racc_chain_id_aa_num_content = match_racc_content(racc_file_content)
                if (chain_id == racc_chain_id_aa_num_content[0])&(aa_nume == racc_chain_id_aa_num_content[1]):
                    return 1
    return 0

def main():
    check_pdb_RACC('DNA','B','518','5t14.pdb')


main()