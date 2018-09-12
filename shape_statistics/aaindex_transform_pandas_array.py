import pandas as pd
import re
import numpy as np


aaindex_attribute_dict = {'ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE',
                          'LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL'}

def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle

def match_aaindex_content_value(file_content):

    CA_value = re.match('\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)\s+(-?\d+.\d*)', file_content)
    if CA_value == None:
        return 0
    else:
        match_aaindex_value_list = [CA_value.group(1), CA_value.group(2), CA_value.group(3), CA_value.group(4), CA_value.group(5),
                                     CA_value.group(6), CA_value.group(7), CA_value.group(8), CA_value.group(9), CA_value.group(10)]
        return match_aaindex_value_list


def match_aaindex_content_head(file_content):
    CA_head = re.match('(H) (\w+)', file_content)
    if CA_head == None:
        return 0
    else:
        return CA_head.group(2)

def aaindex_value_assign(aaindex_name,aaindex_frame,aaindex_value_tuple):

    i = 0
    while i<20:
        aaindex_frame.loc[aaindex_name,[aaindex_attribute_dict[i]]] = aaindex_value_tuple[i]
        i = i + 1



def aaindex_transform_pandas_array():

    aaindex_name = []
    file_path = "E:\PDB_DATA\AA_index_file\output_aaindex.txt"
    file_handle = RE_PDB_content(file_path)
    for file_content in file_handle:
        if file_content != '\n':
            aaindex_name.append(file_content[:-1])
    aaindex_frame = pd.DataFrame(0,index = aaindex_name,columns = aaindex_attribute_dict)

    file_path = "E:\PDB_DATA\AA_index_file\output_aaindex.txt"
    file_handle = RE_PDB_content(file_path)
    for aaindex_name in aaindex_name:
        read_aaindex_value_flag = 0
        for aaindex_content in file_handle:
            if match_aaindex_content_head(aaindex_content) == aaindex_name:
                read_aaindex_value_flag =1
            if read_aaindex_value_flag == 1:
                if match_aaindex_content_value(aaindex_content) :
                    aaindex_value_tuple = match_aaindex_content_value(aaindex_content)
                    aaindex_value_assign(aaindex_name,aaindex_frame,aaindex_value_tuple)

    print(aaindex_frame)

    return aaindex_frame



def main():

    aaindex_transform_pandas_array()


main()