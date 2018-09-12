
import sys
sys.path.append("D:\python_prj\pdb_data_pretreatment")

import pdb_data_pretreatment.path_process as path_process
import pdb_data_pretreatment.pdb_file_process as pdb_file_process
import pdb_data_pretreatment.pdb_file_process_with_racc as pdb_file_process_with_racc
import pdb_data_pretreatment.eliminate_protein_without_nucleotide as eliminate_protein_without_nucleotide
import pdb_data_pretreatment.pdb_file_name_generate as pdb_file_name_generate
import pdb_data_pretreatment.remove_redundancy_fccc_process as remove_redundancy_fccc_process

def main():

    '''
    print("PDB type DNA or RNA?")
    pdb_type = input()
    print("The first step,eliminate protein data does not contain nucleotide,keywords :DA,DC,DG,DA")
    pdb_file_list = path_process.PDB_Read_Path_Process()
    print("the path have input，processing......")
    eliminate_protein_without_nucleotide.eliminate_protein_without_nucleotide(pdb_file_list)

    print("The second step,generates a file name")
    print("No nucleotide containing proteins have been cleaned ,Please keep the file name TXT file is empty")
    pdb_file_list = path_process.PDB_Read_Path_Process()
    if pdb_type =='DNA':
        pdb_file_name_generate.DNA_pdb_file_name_generate(pdb_file_list)
    elif pdb_type == 'RNA':
        pdb_file_name_generate.RNA_pdb_file_name_generate(pdb_file_list)
    print("Remove the redundant pdb file name has been stored.go to fccc process.....")
    print("If you have been removed redundant files in the path ,input y")
    fccc_flag = input()
    if pdb_type =='DNA':
        remove_redundancy_fccc_process.remove_redundancy_fccc_function('DNA',pdb_file_list)
    elif pdb_type == 'RNA':
        remove_redundancy_fccc_process.remove_redundancy_fccc_function('RNA',pdb_file_list)
    print("The data have been pre processed, will calculate the shape of the PDB the next step")
    '''
    pdb_file_list = path_process.PDB_Read_Path_Process()
    pdb_file_process_with_racc.PDB_File_Process(pdb_file_list)
   #pdb_file_process.PDB_File_Process(pdb_file_list)
    print("calculate finished！！")


main()