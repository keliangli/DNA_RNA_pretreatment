# 插入操作所需要的模块
import os
import os.path
import re

# 文件路径处理函数：
# 功能：将文件指针指向PDB文件所放路径；并且返回路径下面所有PDB文件名：
# 输入参数： 无
# 返回参数：PDB文件名列表

def PDB_read_path_process():
    # 输入PDB文件所存放的路径
    print("请输入药物蛋白质文件存放的路径：")
    PDB_Path = input()
    # 改变当前路径为PDB存放路径
    os.chdir(PDB_Path)
    print("您输入的P药物蛋白质文件存放路径为:",os.getcwd())
    PDB_Path_listdir = os.listdir(PDB_Path)
    return PDB_Path_listdir

# 可改进功能：检测并且删除返回列表中不是PDB文件元素

#文件内容读取函数：
#功能：将文件内的内容返回
#返回参数：PDB文件内容列表
def RE_PDB_content(pdb_file_name):
    file_handle = open(pdb_file_name, 'r')
    return file_handle


#文件内容匹配函数：
#功能：匹配文件红的药物大分子的符号并且返回
#返回参数：药物大分子的符号
def match_protein_drug_molecules_repeat(protein_drug_file_content):

    CA_m = re.match('HETNAM\s+(\d)\s+\S+\s+', protein_drug_file_content)
    if CA_m == None:
        return 0
    else:
        return 1

#药物大分子重复检查函数：
#功能：匹配文件红的药物大分子是否出现重复现象
#返回参数：返回1表示出现了重复，返回0表示没有重复

def match_protein_drug_molecules(protein_drug_file_content):

    CA_m = re.match('HETNAM\s+\d?\s+(\S+)\s+', protein_drug_file_content)
    if CA_m == None:
        return 0
    else:
        CA_Content_Tuple = CA_m.group(1)

    return CA_Content_Tuple


#匹配药物大分子函数：
#功能：匹配药物大分子中是否有传入的符号的分子
#返回参数：返回0表示没有，返回1表示有这样的符号
def match_dictionary_function(match_content,match_dictionary):
    match_flag = 0
    for key in match_dictionary:
        if key == match_content:
            match_flag = 1
    return match_flag

#字典处理函数：
#功能：更新字典中的值
#返回参数：无
def build_drug_molecules_dictionary(drug_molecules,drug_molecules_appear_dict,pdb_file_name_dict,protein_drug_file_name,drug_molecules_repeat_flag):
    #判断药物大分子字典中是否有输入该项，如果没有返回0，添加该项并且赋值1，如果有则进行下一个判断环节
    if match_dictionary_function(drug_molecules,drug_molecules_appear_dict)==0:
        drug_molecules_appear_dict[drug_molecules] = 1
    else:
        #判断pdb文件名字典中是否有该项的值，如果有，则不操作，如果没有则，进入下一处理环节
        if match_dictionary_function(protein_drug_file_name,pdb_file_name_dict)==0:
            if drug_molecules_repeat_flag ==0:
                drug_molecules_appear_dict[drug_molecules] = drug_molecules_appear_dict[drug_molecules] + 1


#文件内容处理函数：
#功能：1，取出文件中的药物大分子的内容，2.建立索引字典，对于药物大分子出现次数进行统计，3，将药物大分子的内容输出到txt文件
#返回参数：无
def PDB_content_process(PDB_Path_listdir):
    print("请输入药物蛋白质处理结果文件存放的路径以文件名字和后缀：")
    pdb_result_path = input()
    Write_file_handle = open(pdb_result_path, 'a')
    drug_molecules_appear_dict = {}
    pdb_file_name_dict = {}
    for protein_drug_file_name in PDB_Path_listdir:
        Write_file_handle.write(protein_drug_file_name)
        Write_file_handle.write('\n')
        protein_drug_file_handle = RE_PDB_content(protein_drug_file_name)
        for protein_drug_file_content in protein_drug_file_handle:
            if match_protein_drug_molecules(protein_drug_file_content) !=0 :
                drug_molecules_repeat_flag = match_protein_drug_molecules_repeat(protein_drug_file_content)
                Write_file_handle.write(protein_drug_file_content)
                drug_molecules = match_protein_drug_molecules(protein_drug_file_content)
                build_drug_molecules_dictionary(drug_molecules,drug_molecules_appear_dict,
                                                pdb_file_name_dict,protein_drug_file_name,drug_molecules_repeat_flag)
        if match_dictionary_function(protein_drug_file_name, pdb_file_name_dict) == 0:
            pdb_file_name_dict[protein_drug_file_name] = 1
        Write_file_handle.write('\n')

    for key in drug_molecules_appear_dict:
        Write_file_handle.write(str(key))
        Write_file_handle.write(':')
        drug_molecules_num = int(drug_molecules_appear_dict[key])
        Write_file_handle.write(str(drug_molecules_num))
        Write_file_handle.write('\n')
    Write_file_handle.close()


def main():
    PDB_Path_listdir =  PDB_read_path_process()
    PDB_content_process(PDB_Path_listdir)


main()




