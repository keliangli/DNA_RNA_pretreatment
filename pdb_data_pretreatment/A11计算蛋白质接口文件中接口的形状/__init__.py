import os
import re
import math
import numpy




def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM.{9}CA\s+([A-Z]+).{11}(\s+?\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).*',pdb_content)
    if CA_m == None:
        return 0
    else:
        CA_Content_Tuple = (CA_m.group(1),CA_m.group(2),CA_m.group(3),CA_m.group(4))
    return  CA_Content_Tuple


def Match_PDB_Calcu_ATOM(PDB_Content_Atom):
    ATOM_m = re.match('ATOM.{11}\s+([A-Z]+).{11}(\s+?\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).{23}(\w).*',PDB_Content_Atom)
    if ATOM_m == None:
        return 0
    else:
        if (ATOM_m.group(5) !='H')&\
           (ATOM_m.group(1) !='DA')&\
           (ATOM_m.group(1) !='DT')&\
           (ATOM_m.group(1) !='DG')&\
           (ATOM_m.group(1) !='DC')&\
           (ATOM_m.group(1) !='A')&\
           (ATOM_m.group(1) !='C')&\
           (ATOM_m.group(1) !='G')&\
           (ATOM_m.group(1) !='T')&\
           (ATOM_m.group(1) !='U')&\
           (ATOM_m.group(1) !='I'):
            ATOM_Coordinate_Tuple = (ATOM_m.group(2),ATOM_m.group(3),ATOM_m.group(4))
        else:
            ATOM_Coordinate_Tuple = 0

    return  ATOM_Coordinate_Tuple


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

def match_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.txt',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)


def match_pbd_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.pdb',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)


def Calcu_PDB_Sphere_ATOM(PDB_Path,interface_file_name,CA_ATOM_Coordinate):

    Valid_ATOM_count = 0
    os.chdir(PDB_Path)
    PDB_Path_listdir = os.listdir(PDB_Path)

    for pdb_file_name in PDB_Path_listdir:
        pdb_name = match_pbd_file_name(pdb_file_name)
        interface_name = match_file_name(interface_file_name)
        if pdb_name == interface_name:
            pdb_handle = RE_PDB_content(pdb_file_name)
            for pdb_content in pdb_handle:
                ATOM_Coordinate = Match_PDB_Calcu_ATOM(pdb_content)
                if (ATOM_Coordinate !=0):
                    Valid_ATOM_Dis = Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate, ATOM_Coordinate)
                    if Valid_ATOM_Dis <12 :
                        Valid_ATOM_count = Valid_ATOM_count + 1
    return Valid_ATOM_count



def Calcu_PDB_CA_SI(PDB_Path,interface_file_name,CA_ATOM_Coordinate):

    Valid_ATOM_Num = Calcu_PDB_Sphere_ATOM(PDB_Path,interface_file_name,CA_ATOM_Coordinate)
    Vint   = Valid_ATOM_Num * 20.1
    Vsphere= 4*math.pi*12**3/3
    Vext   = Vsphere - Vint
    CX = (Vext-Vint)/Vsphere
    return CX



def calcu_interface_shape(PDB_Path,interface_file_name,CA_ATOM_Coordinate):

    CX = Calcu_PDB_CA_SI(PDB_Path,interface_file_name,CA_ATOM_Coordinate)
    if CX < -0.2:
        return "valley"
    elif CX < 0.2:
        return "flat"
    else:
        return "peak"




def Print_PDB_Amino_acid_SI(interface_file_name,interface_content,shape_str):

    PDB_file_name = match_file_name(interface_file_name)
    file_name = PDB_file_name +'shape.txt'
    Write_file_handle = open(file_name,'a')
    Write_file_handle.write(interface_content[:-1])
    Write_file_handle.write("  Shape:")
    Write_file_handle.write(shape_str)
    Write_file_handle.write('\n')
    Write_file_handle.close()


def PDB_File_Process():


    print("please input the interface path：")
    interface_Path = input()
    os.chdir(interface_Path)
    print("you input interface path is :", interface_Path)
    interface_Path_listdir = os.listdir(interface_Path)

    print("please input the pdb path：")
    PDB_Path = input()
    print("you input pdb path is :", PDB_Path)



    for interface_file_name in interface_Path_listdir:
        # 读取pdb的文件的名字
        interface_CA_Content = RE_PDB_content(interface_file_name)
        # 返回pdb文件的句柄，准备对于文件内容进行处理
        for interface_content in interface_CA_Content:
            # 返回ca原子的位置坐标
            CA_ATOM_Coordinate = Match_PDB_CA_ATOM(interface_content)
            if CA_ATOM_Coordinate != 0:
                shape_str = calcu_interface_shape(PDB_Path,interface_file_name,CA_ATOM_Coordinate)
                Print_PDB_Amino_acid_SI(interface_file_name,interface_content,shape_str)
                os.chdir(interface_Path)
        interface_CA_Content.close()


def main():
    PDB_File_Process()


main()
