import re

def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle



def match_pdb_file_name(file_content):
    CA_head = re.match('(\w{4}).*', file_content)
    if CA_head == None:
        return 0
    else:
        return CA_head.group(1)





file_path = r'E:\SCPDB_R\PDB_after'


file_aaindex_handle = RE_PDB_content(file_path)

file_w_name = r'E:\SCPDB_R\PDB_NAME.txt'
Write_file_handle = open(file_w_name, 'a')

for file_content in file_aaindex_handle:
    file_name = match_pdb_file_name(file_content)
    if file_name:
        Write_file_handle.write(file_name)
        Write_file_handle.write(',')