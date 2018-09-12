
import re
import numpy
import os
import math


def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle

def Match_PDB_Calcu_DX(PDB_Content_Atom):
    ATOM_m = re.match('ATOM.{14}(DA|DT|DG|DC| A| C| G| T| U| I).{10}\s+?(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).*',PDB_Content_Atom)
    if ATOM_m == None:
        return 0
    else:
        ATOM_Coordinate_Tuple = (ATOM_m.group(2),ATOM_m.group(3),ATOM_m.group(4))
        print(ATOM_Coordinate_Tuple)
    return  ATOM_Coordinate_Tuple


def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM.{9}CA\s+([A-Z]+).{10}\s+?(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).*',pdb_content)
    if CA_m == None:
        return 0
    else:
        CA_Conten_Tuple = (CA_m.group(1),CA_m.group(2),CA_m.group(3),CA_m.group(4))
    return  CA_Conten_Tuple


def Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate,ATOM_Coordinate):

    CA_Coordinate_X   = float(CA_ATOM_Coordinate[1])
    CA_Coordinate_Y   = float(CA_ATOM_Coordinate[2])
    CA_Coordinate_Z   = float(CA_ATOM_Coordinate[3])
    ATOM_Coordinate_X = float(ATOM_Coordinate[0])
    ATOM_Coordinate_Y = float(ATOM_Coordinate[1])
    ATOM_Coordinate_Z = float(ATOM_Coordinate[2])

    vector1 = numpy.array((CA_Coordinate_X,CA_Coordinate_Y,CA_Coordinate_Z))
    vector2 = numpy.array((ATOM_Coordinate_X,ATOM_Coordinate_Y,ATOM_Coordinate_Z))

    ATOM_Euclid_Dis = numpy.sqrt(numpy.sum((vector1-vector2)**2))

    return ATOM_Euclid_Dis



#计算CA远在所在的氨基酸是否为接口
def calcu_CA_is_interface(CA_ATOM_Coordinate,PDB_ATOM_Content):

    for PDB_Content_Atom in PDB_ATOM_Content:
        ATOM_Coordinate = Match_PDB_Calcu_DX(PDB_Content_Atom)
        if ATOM_Coordinate != 0:
            CA_DX_dis = Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate,ATOM_Coordinate)
            if CA_DX_dis <6:
                return CA_DX_dis
            else:
                continue
    return 0


def match_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.pdb',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)


def Print_PDB_interface_atom(pdb_file_name,pdb_file_content):

    PDB_file_name = match_file_name(pdb_file_name)
    file_name = PDB_file_name +'.txt'
    Write_file_handle = open(file_name,'a')
    Write_file_handle.write(pdb_file_content)
    Write_file_handle.close()


def PDB_File_Process():

        print("please input the pdb path：")
        PDB_Path = input()
        os.chdir(PDB_Path)
        print("you input pdb path is :", os.getcwd())
        PDB_Path_listdir = os.listdir(PDB_Path)

        for pdb_file_name in PDB_Path_listdir:
            # 读取pdb的文件的名字
            PDB_CA_Content = RE_PDB_content(pdb_file_name)
            # 返回pdb文件的句柄，准备对于文件内容进行处理
            for pdb_content in PDB_CA_Content:
                # 返回ca原子的位置坐标
                CA_ATOM_Coordinate = Match_PDB_CA_ATOM(pdb_content)
                PDB_ATOM_Content = RE_PDB_content(pdb_file_name)
                if CA_ATOM_Coordinate == 0:
                    continue
                else:
                    CA_interface_result = calcu_CA_is_interface(CA_ATOM_Coordinate, PDB_ATOM_Content)
                #    if CA_interface_result:
                #        Print_PDB_interface_atom(pdb_file_name,pdb_content)
            PDB_CA_Content.close()

def main():
    PDB_File_Process()


main()
