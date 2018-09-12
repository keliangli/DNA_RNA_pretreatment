import re
import os


def match_pdb_nucleotide(pdb_file_content):
    CA_m = re.match('ATOM.{14}(DA|DT|DG|DC| A| C| G| T| U| I).*',pdb_file_content)
    if CA_m == None:
        return 0
    else:
        print(pdb_file_content)
        return 1


def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM.{9}(CA).*',pdb_content)
    if CA_m == None:
        return 0
    else:
        print(pdb_content)
        return 1

def eliminate_protein_without_nucleotide(pdb_data_path):

    for pdb_file_name in pdb_data_path:
        pdb_file_handle = open(pdb_file_name, 'r')
        pdb_remove_flag = 0
        for  pdb_file_content in pdb_file_handle:
            if match_pdb_nucleotide(pdb_file_content):
                pdb_remove_flag = 1
                break
            else:
                pdb_remove_flag = 0
        if pdb_remove_flag == 0:
            print(pdb_file_name)
            print("without NC")
            pdb_file_handle.close()
            os.remove(pdb_file_name)
            continue
        pdb_file_handle = open(pdb_file_name, 'r')
        pdb_remove_flag = 0
        for  pdb_file_content in pdb_file_handle:
            if Match_PDB_CA_ATOM(pdb_file_content):
                pdb_remove_flag=1
                break
            else:
                pdb_remove_flag = 0
        if pdb_remove_flag == 0:
            print(pdb_file_name)
            print("without CA")
            pdb_file_handle.close()
            os.remove(pdb_file_name)



def main():

    print("please input the pdb path：")
    PDB_Path = input()
    os.chdir(PDB_Path)
    print("you input pdb path is :",os.getcwd())
    PDB_Path_listdir = os.listdir(PDB_Path)

    eliminate_protein_without_nucleotide(PDB_Path_listdir)


main()
