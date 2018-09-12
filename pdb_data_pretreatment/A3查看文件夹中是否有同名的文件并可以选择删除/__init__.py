import os



DNA_name = {}
RNA_name = {}
both_name = {}

print('DNA_PATH:')
DNA_PDB_Path = input()
os.chdir(DNA_PDB_Path)
print("you input pdb path is :", os.getcwd())
PDB_Path_listdir = os.listdir(DNA_PDB_Path)


i = 0
for pdb_name in PDB_Path_listdir:
     DNA_name[i] = pdb_name
     i = i +1


print('RNA_PATH:')
RNA_PDB_Path = input()
os.chdir(RNA_PDB_Path)
print("you input pdb path is :", os.getcwd())
PDB_Path_listdir = os.listdir(RNA_PDB_Path)


j = 0
for pdb_name in PDB_Path_listdir:
     RNA_name[j] = pdb_name
     j = j +1

print(DNA_name)

print(RNA_name)

n = 0
flag = 0
for key in DNA_name:
    dna_name = DNA_name[key]
    for key in RNA_name:
        if dna_name == RNA_name[key]:
            flag = 1
    print(dna_name)
    print(flag)
    if flag == 1:
        both_name[n] = dna_name
        n = n + 1
    flag = 0

print(both_name)



os.chdir(DNA_PDB_Path)
for key in both_name:
   print(both_name[key])
   os.remove(both_name[key])

#
#
#
# os.chdir(RNA_PDB_Path)
# for key in both_name:
#    os.remove(both_name[key])
#

