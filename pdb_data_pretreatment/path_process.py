
import os
import os.path


def PDB_Read_Path_Process():

    print("please input the pdb path：")
    PDB_Path = input()
    os.chdir(PDB_Path)
    print("you input pdb path is :",os.getcwd())
    PDB_Path_listdir = os.listdir(PDB_Path)
    return PDB_Path_listdir




