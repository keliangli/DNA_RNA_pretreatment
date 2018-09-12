# 插入操作所需要的模块
import os
import os.path
import re


def match_pdb_file_name(protein_drug_file_name):

    CA_m = re.match('(\S+).pdb', protein_drug_file_name)
    if CA_m == None:
        return 0
    else:
        return CA_m.group(1)



def remove_redundancy_fccc_function(process_type,PDB_Path_listdir):


    for protein_drug_file_name in PDB_Path_listdir:
        pdb_remove_flag = 0
        pdb_file_name = match_pdb_file_name(protein_drug_file_name)
        if process_type == 'DNA':
            file_handle = open("E:\\PDB_DATA\\DNA_pdb_file_name\\dna_pdb_file_name.txt", 'r')
        else:
            file_handle = open("E:\\PDB_DATA\\RNA_pdb_file_name\\rna_pdb_file_name.txt", 'r')
        for remove_redundancy_file_content in file_handle:
            CA_m = re.match(pdb_file_name, remove_redundancy_file_content)
            if CA_m != None:
                pdb_remove_flag = 1
        if pdb_remove_flag ==0:
            os.remove(protein_drug_file_name)



