
import re
import math
import numpy
import os
import pdb_data_pretreatment.A7提供相对溶剂可及性查询接口 as check_pdb_RACC


def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle

def Match_PDB_CA_ATOM(pdb_content):
    CA_m = re.match('ATOM\s+[0-9]+\s+CA\s+([A-Z]+)\s+(\w+)\s+(\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).+',pdb_content)
    if CA_m == None:
        return 0
    else:
        CA_Conten_Tuple = (CA_m.group(1),CA_m.group(4),CA_m.group(5),CA_m.group(6),CA_m.group(2),CA_m.group(3))
    return  CA_Conten_Tuple


def Match_PDB_Calcu_DX(PDB_Content_Atom):
    ATOM_m = re.match('ATOM\s+[0-9]+\s+\w+\s+(DA|DT|DG|DC|C|G|A|U|T|I|\+A|\+C|\+T|\+U|\+I)\s+\w+\s+\d+\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).+',PDB_Content_Atom)
    if ATOM_m == None:
        return 0
    else:
        ATOM_Coordinate_Tuple = (ATOM_m.group(2),ATOM_m.group(3),ATOM_m.group(4))
    return  ATOM_Coordinate_Tuple



def Match_PDB_Calcu_ATOM(PDB_Content_Atom):
    ATOM_m = re.match('ATOM\s+[0-9]+\s+\w+\s+\w+\s+\w+\s+\d+\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).+',PDB_Content_Atom)
    if ATOM_m == None:
        return 0
    else:
        ATOM_Coordinate_Tuple = (ATOM_m.group(1),ATOM_m.group(2),ATOM_m.group(3))
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



def Calcu_PDB_Sphere_ATOM(PDB_ATOM_Content,CA_ATOM_Coordinate):

    Valid_ATOM_cout = 0
    for PDB_Content_Atom in PDB_ATOM_Content:
        ATOM_Coordinate = Match_PDB_Calcu_ATOM(PDB_Content_Atom)
        if ATOM_Coordinate !=0:
            Valid_ATOM_Dis = Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate, ATOM_Coordinate)
            if Valid_ATOM_Dis <12 :
                Valid_ATOM_cout = Valid_ATOM_cout + 1
    return Valid_ATOM_cout



def Calcu_PDB_CA_SI(PDB_ATOM_Content, CA_ATOM_Coordinate):

    Valid_ATOM_Num = Calcu_PDB_Sphere_ATOM(PDB_ATOM_Content, CA_ATOM_Coordinate)
    Vint   = Valid_ATOM_Num * 20.1
    Vsphere= 4*math.pi*12**3/3
    Vext   = Vsphere - Vint
    CX = (Vext-Vint)/Vsphere
    return CX


def match_file_name(pdb_file_name):

    file_name = re.match('(\w+)\.pdb',pdb_file_name)
    if file_name == None:
        return 0
    else:
        return file_name.group(1)

def Print_PDB_Amino_acid_SI(pdb_file_name,CA_ATOM_SI_Value,CA_ATOM_Coordinate,Residues_Shape):

    #PDB_file_name = match_file_name(pdb_file_name)
    file_name = pdb_file_name +'.txt'
    Write_file_handle = open(file_name,'a')
    Write_file_handle.write(CA_ATOM_Coordinate[0])
    Write_file_handle.write("  SI:")
    Write_file_handle.write(str(CA_ATOM_SI_Value))
    Write_file_handle.write("  Shape:")
    Write_file_handle.write(Residues_Shape)
    Write_file_handle.write("\n")
    Write_file_handle.close()

#计算CA远在所在的氨基酸是否为接口
def calcu_CA_is_interface(CA_ATOM_Coordinate,PDB_ATOM_Content):

    for PDB_Content_Atom in PDB_ATOM_Content:
        ATOM_Coordinate = Match_PDB_Calcu_DX(PDB_Content_Atom)
        if ATOM_Coordinate != 0:
            CA_DX_dis = Calcu_PDB_ATOM_Dis(CA_ATOM_Coordinate,ATOM_Coordinate)
            if CA_DX_dis <4.5:
                return CA_DX_dis
            else:
                continue
    return 0


def PDB_File_Process():

        print("please input the pdb path：")
        PDB_Path = input()
        os.chdir(PDB_Path)
        print("you input pdb path is :", os.getcwd())
        PDB_Path_listdir = os.listdir(PDB_Path)

        print("please input the pdb type:")
        PDB_type = input()

        for pdb_file_name in PDB_Path_listdir:
            #读取pdb的文件的名字
            PDB_CA_Content = RE_PDB_content(pdb_file_name)
            print(pdb_file_name)
            #返回pdb文件的句柄，准备对于文件内容进行处理
            for pdb_content in PDB_CA_Content:
                #返回ca原子的位置坐标
                CA_ATOM_Coordinate = Match_PDB_CA_ATOM(pdb_content)
                PDB_ATOM_Content = RE_PDB_content(pdb_file_name)
                if CA_ATOM_Coordinate==0:
                   continue
                else:
                   # CA_interface_result = calcu_CA_is_interface(CA_ATOM_Coordinate, PDB_ATOM_Content)
                    pdb_RACC_flag = check_pdb_RACC.check_pdb_RACC(PDB_type, CA_ATOM_Coordinate[4], CA_ATOM_Coordinate[5], pdb_file_name)
                    os.chdir(PDB_Path)
                    if pdb_RACC_flag:
                        os.chdir(PDB_Path)
                        CA_ATOM_SI_Value = Calcu_PDB_CA_SI(PDB_ATOM_Content,CA_ATOM_Coordinate)
                        PDB_ATOM_Content.close()
                        if CA_ATOM_SI_Value<-0.2:
                            Residues_Shape = "valley"
                        elif (CA_ATOM_SI_Value<0.2):
                            Residues_Shape = "flat"
                        else:
                            Residues_Shape = "peak"
                        Print_PDB_Amino_acid_SI(pdb_file_name,CA_ATOM_SI_Value,CA_ATOM_Coordinate,Residues_Shape)
            PDB_CA_Content.close()

def main():

    PDB_File_Process()


main()

