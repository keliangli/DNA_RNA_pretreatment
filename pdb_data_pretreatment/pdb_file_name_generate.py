import re


def match_the_pdb_file_name(pdb_file_name):

        CA_m = re.match('(\S+).pdb', pdb_file_name)
        if CA_m == None:
            return 0
        else:
            return CA_m.group(1)


def RNA_pdb_file_name_generate(pdb_file_list):

    file_name_txt_handle  = open("E:\\PDB_DATA\\RNA_pdb_file_name\\rna_pdb_file_name.txt", 'a')

    for file_name in pdb_file_list:
        pdb_file_name = match_the_pdb_file_name(file_name)
        file_name_txt_handle.write(str(pdb_file_name))
        file_name_txt_handle.write('\n')


def DNA_pdb_file_name_generate(pdb_file_list):

    file_name_txt_handle  = open("E:\\PDB_DATA\\DNA_pdb_file_name\\dna_pdb_file_name.txt", 'a')

    for file_name in pdb_file_list:
        pdb_file_name = match_the_pdb_file_name(file_name)
        file_name_txt_handle.write(str(pdb_file_name))
        file_name_txt_handle.write('\n')
