import os

#存放pdb文件的路径下面一定要有dssp的软件

def calcu_solvent_sccessiblity():

    print("please input the pdb path：")
    PDB_Path = input()
    os.chdir(PDB_Path)
    print("you input pdb path is :", os.getcwd())
    PDB_Path_listdir = os.listdir(PDB_Path)
    for pdb_file_name in PDB_Path_listdir:
        print(pdb_file_name)
        str = "dssp-3.0.0-win32.exe -i "+pdb_file_name+" -o "+pdb_file_name+".dssp"
        print(str)
        p=os.popen(str)
        print(p.read())

def main():
    calcu_solvent_sccessiblity()

main()

