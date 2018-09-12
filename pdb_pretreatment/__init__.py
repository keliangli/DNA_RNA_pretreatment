
import os
import os.path
import re
import numpy
import subprocess

# ########################删除不含DNA的蛋白质文件#################################################

# 输入pdb存放路径
print("请输入pdb存放的路径：")
Pdb_File_Path = input()

# 改变文件指针路径为输入路径
os.chdir(Pdb_File_Path)

print("您输入的PDB文件存放路径为:", os.getcwd())

# 返回输入路径下面所有文件的文件名
PDB_Path_listdir = os.listdir(Pdb_File_Path)

remove_flag = 0

for PDB_Path_name in PDB_Path_listdir:
    # 判断路径下面的文件是否都是pdb文件
    pdb_name_m = re.match('\w+\.(pdb)', PDB_Path_name)
    if pdb_name_m == None:
        remove_flag = 0
    else:
        # 打开当前pdb文件
        file_handle = open(PDB_Path_name, 'r')
        # 遍历文件内每行内容
        for pdb_file_content in file_handle:
            # 匹配当前行内容是否存在蛋白质DNA所特有的DA\DC\DT\DA的名字
            pdb_content_m = re.match('ATOM\s+[0-9]+\s+\w+\S?\s+(DG|DC|DT|DA)\s+\w+\s+\d+\s+(\D?\d+\.\d+)(\s+)?(\D?\d+\.\d+)(\s+)?(\D?\d+\.\d+).+',pdb_file_content)
            if pdb_content_m == None:
                continue
            else:
                remove_flag = 1
                break
        file_handle.close()
    if remove_flag == 0:
        os.remove(PDB_Path_name)
    else:
        remove_flag = 0

#  #####################################################################################################
# 打开一个txt文件存放删选完毕的含有DNA的蛋白质文件名
PDB_name_file_handle = open("E:\PDB\PDB_name_file.txt", 'a')

for pdb_file_name in PDB_Path_listdir:
    m = re.match("(\w+).pdb", pdb_file_name)
    if m==None:
        continue
    else:
        PDB_name_file_handle.write(m.group(1))
        PDB_name_file_handle.write("\n")

PDB_name_file_handle.close()


#  #####################################################################################################
# 检查pdb文件，并且删除有冗余的文件
print("pdb名字抽取已经完成，请登录网站进行冗余性检验，完成后请输入YES:")
str1 = input()
if str1 != "YES":
    print("您输入的错误")
else:
    # 打开txt文件读取文件中的内容
    for pdb_file_name in PDB_Path_listdir:
        # 循环遍历pdb文件内的内容
        remove_flag_2 = 0
        file_pdb_name_file = open("E:\PDB\PDB_name_file.txt", 'r')
        m = re.match("(\w+).pdb", pdb_file_name)
        string_1 = str(m.group(1))
        for file_name in file_pdb_name_file:
            # 如果发现冗余文件就讲删除标志设1
            m_1 = re.match(string_1, file_name)
            if m_1 != None:
                remove_flag_2 = 1
        file_pdb_name_file.close()
        if remove_flag_2 == 0:
            print("找到一个冗余文件为：")
            print(pdb_file_name)
            print("\n文件即将被删除")
            os.remove(pdb_file_name)
os.remove("E:\PDB\PDB_name_file.txt")

#  #####################################################################################################
#  计算保存下来的pdb文件内的各个原子间的距离，只要有一个距离小于4.5则保存，如果不存在则删除

"""

# 匹配PDB文件中的所有的值，匹配成功返回其XYZ的坐标值，匹配不成功返回0值
def Match_PDB_Calcu_ATOM(PDB_Content_Atom):
    ATOM_m = re.match('\w+\s+[0-9]+\s+\w+\S?\s+\w+\s+\w+\s+\d+\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+)\s+(\D?\d+\.\d+).+',PDB_Content_Atom)
    if ATOM_m == None:
        return 0
    else:
        ATOM_Coordinate_Tuple = (ATOM_m.group(1), ATOM_m.group(2), ATOM_m.group(3))
    return ATOM_Coordinate_Tuple


# 计算并且返回PDB文件与当前CA原子的距离
def Calcu_PDB_ATOM_Dis (CA_ATOM_Coordinate,ATOM_Coordinate):

    CA_Coordinate_X   = float(CA_ATOM_Coordinate[0])
    CA_Coordinate_Y   = float(CA_ATOM_Coordinate[1])
    CA_Coordinate_Z   = float(CA_ATOM_Coordinate[2])
    ATOM_Coordinate_X = float(ATOM_Coordinate[0])
    ATOM_Coordinate_Y = float(ATOM_Coordinate[1])
    ATOM_Coordinate_Z = float(ATOM_Coordinate[2])

    vector1 = numpy.array((CA_Coordinate_X,CA_Coordinate_Y,CA_Coordinate_Z))
    vector2 = numpy.array((ATOM_Coordinate_X,ATOM_Coordinate_Y,ATOM_Coordinate_Z))

    ATOM_Euclid_Dis = numpy.sqrt(numpy.sum((vector1-vector2)**2))

    return ATOM_Euclid_Dis


# 变量pdb所在路径返回其每个pdb文件的文件句柄
for pdb_file_name in PDB_Path_listdir:
    # 打开一个文件，设置为第一文件句柄，作为遍历的第一层
    Frist_pdb_content = open(pdb_file_name, 'r')
    file_name = Pdb_File_Path + '\\' + pdb_file_name + '.txt'
    remove_flag_3 = 0
    for frist_pdb_content in Frist_pdb_content:
        # 返回第一层所匹配的原子的坐标
        ATOM_Coordinate_Tuple1 = Match_PDB_Calcu_ATOM(frist_pdb_content)
        if ATOM_Coordinate_Tuple1 == 0:
            continue
        # 打开一个文件，设置为第一文件句柄，作为遍历的第二层
        Second_pdb_content = open(pdb_file_name, 'r')
        for second_pdb_content in Second_pdb_content:
            # 返回第一层所匹配的原子的坐标
            ATOM_Coordinate_Tuple2 = Match_PDB_Calcu_ATOM(second_pdb_content)
            if ATOM_Coordinate_Tuple2 == 0:
                continue
            ATOM_DIS = Calcu_PDB_ATOM_Dis(ATOM_Coordinate_Tuple1, ATOM_Coordinate_Tuple2)
            if ATOM_DIS < 4.5:
                remove_flag_3 = 1
                ATOM_Coordinate_str1 = "".join(ATOM_Coordinate_Tuple1)
                ATOM_Coordinate_str2 = "".join(ATOM_Coordinate_Tuple2)
                ATOM_DIS_str         = str(ATOM_DIS)
                Write_file_handle = open(file_name, 'a')
                Write_file_handle.write(ATOM_Coordinate_str1)
                Write_file_handle.write("<------->")
                Write_file_handle.write(ATOM_Coordinate_str2)
                Write_file_handle.write(">-- DIS  --< :::::")
                Write_file_handle.write(ATOM_DIS_str)
                Write_file_handle.write("\n")
                Write_file_handle.close()

    Frist_pdb_content.close()
    Second_pdb_content.close()
    if remove_flag_3 == 0:
        os.remove(pdb_file_name)
        remove_flag_3 = 0
"""
























