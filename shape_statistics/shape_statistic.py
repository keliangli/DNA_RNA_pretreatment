
import os.path
import re
import matplotlib.pyplot as plt;plt.rcdefaults()
import numpy as np

# 匹配凸区域
def match_shape_peak(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:peak\s+', shape_file_content)
    if shape_m==None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)

# 匹配平区域
def match_shape_flat(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:falt\s+', shape_file_content)
    if shape_m == None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)

# 匹配凹区域
def match_shape_valley(shape_file_content):
    shape_m = re.match('(\w+)\s+([0-9]*)\s+\w+:(\S?)\w+.\w+\s+Shape:valley\s+', shape_file_content)
    if shape_m == None:
        return 0
    else:
        # 如果匹配成功则返回氨基酸的类型
        return shape_m.group(1)


# #############RNA_数据############################
RNA_peak_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                          'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                          'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                          'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}

def RNA_peak_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    RNA_peak_AA_count_dict[AA_type] = RNA_peak_AA_count_dict[AA_type] + 1


RNA_flat_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                          'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                          'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                          'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}
def RNA_flat_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    RNA_flat_AA_count_dict[AA_type] = RNA_flat_AA_count_dict[AA_type] + 1

RNA_valley_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                            'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                            'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                            'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}
def RNA_valley_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    RNA_valley_AA_count_dict[AA_type] = RNA_valley_AA_count_dict[AA_type] + 1
# #############RNA_数据############################

# #############DNA_数据处理############################

DNA_peak_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                          'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                          'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                          'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}

def DNA_peak_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    DNA_peak_AA_count_dict[AA_type] = DNA_peak_AA_count_dict[AA_type] + 1


DNA_flat_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                          'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                          'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                          'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}
def DNA_flat_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    DNA_flat_AA_count_dict[AA_type] = DNA_flat_AA_count_dict[AA_type] + 1

DNA_valley_AA_count_dict = {'GLY': 0, 'PRO': 0, 'ALA': 0, 'VAL': 0, 'PHE': 0,
                            'LEU': 0, 'ILE': 0, 'MET': 0, 'TRP': 0, 'GLN': 0,
                            'ASN': 0, 'SER': 0, 'CYS': 0, 'THR': 0, 'TYR': 0,
                            'HIS': 0, 'LYS': 0, 'ARG': 0, 'GLU': 0, 'ASP': 0}
def DNA_valley_AA_counter(AA_type):
    if len(AA_type)==4:
        AA_type = AA_type[1:4]
    DNA_valley_AA_count_dict[AA_type] = DNA_valley_AA_count_dict[AA_type] + 1
# #############DNA_数据############################




# #############RNA_数据处理############################
print("请输入RNA_PDB形状数据存放的路径：")

pdb_shape_dir = input()

# 改变当前的路径为输入的路径
os.chdir(pdb_shape_dir)

print("您输入的RNA_PDB文件存放路径为:", os.getcwd())

# 返回路径中的文件句柄
PDB_Path_listdir = os.listdir(pdb_shape_dir)

RNA_peak_counter   = 0
RNA_flat_counter   = 0
RNA_valley_counter = 0
RNA_file_counter   = 0

for pdb_shape_file in PDB_Path_listdir:
    RNA_file_counter = RNA_file_counter + 1
    print(pdb_shape_file)
    shape_file = open(pdb_shape_file, 'r')
    for shape_file_content in shape_file:
        peak_aa_type = match_shape_peak(shape_file_content)
        flat_aa_type = match_shape_flat(shape_file_content)
        valley_aa_type = match_shape_valley(shape_file_content)
        if peak_aa_type != 0:
            RNA_peak_counter = RNA_peak_counter + 1
            RNA_peak_AA_counter(peak_aa_type)
        elif flat_aa_type != 0:
            RNA_flat_counter = RNA_flat_counter + 1
            RNA_flat_AA_counter(flat_aa_type)
        elif valley_aa_type != 0:
            RNA_valley_counter = RNA_valley_counter + 1
            RNA_valley_AA_counter(valley_aa_type)
        else:
            print(shape_file_content)
            print("分析错误，没有找到形状数据")

# #############DNA_数据处理############################
print("请输入DNA_PDB形状数据存放的路径：")

pdb_shape_dir = input()

# 改变当前的路径为输入的路径
os.chdir(pdb_shape_dir)

print("您输入的DNA_PDB文件存放路径为:", os.getcwd())

# 返回路径中的文件句柄
PDB_Path_listdir = os.listdir(pdb_shape_dir)

DNA_peak_counter   = 0
DNA_flat_counter   = 0
DNA_valley_counter = 0
DNA_file_counter   = 0


for pdb_shape_file in PDB_Path_listdir:
    DNA_file_counter = DNA_file_counter + 1
    print(pdb_shape_file)
    shape_file = open(pdb_shape_file, 'r')
    for shape_file_content in shape_file:
        peak_aa_type = match_shape_peak(shape_file_content)
        flat_aa_type = match_shape_flat(shape_file_content)
        valley_aa_type = match_shape_valley(shape_file_content)
        if peak_aa_type != 0:
            DNA_peak_counter = DNA_peak_counter + 1
            DNA_peak_AA_counter(peak_aa_type)
        elif flat_aa_type != 0:
            DNA_flat_counter = DNA_flat_counter + 1
            DNA_flat_AA_counter(flat_aa_type)
        elif valley_aa_type != 0:
            DNA_valley_counter = DNA_valley_counter + 1
            DNA_valley_AA_counter(valley_aa_type)
        else:
            print(shape_file_content)
            print("分析错误，没有找到形状数据")






'''
AA_TYPE = list(DNA_valley_AA_count_dict.keys())

DNA_peak_AA_num   = tuple(DNA_peak_AA_count_dict.values())
DNA_flat_AA_num   = tuple(DNA_flat_AA_count_dict.values())
DNA_valley_AA_num = tuple(DNA_valley_AA_count_dict.values())


RNA_peak_AA_num   = tuple(RNA_peak_AA_count_dict.values())
RNA_flat_AA_num   = tuple(RNA_flat_AA_count_dict.values())
RNA_valley_AA_num = tuple(RNA_valley_AA_count_dict.values())

DNA_peak_AA_average   = {}
DNA_flat_AA_average   = {}
DNA_valley_AA_average = {}

RNA_peak_AA_average   = {}
RNA_flat_AA_average   = {}
RNA_valley_AA_average = {}

DNA_peak_i = 0

for element in DNA_peak_AA_num:
    DNA_peak_AA_average[DNA_peak_i] = element / DNA_file_counter
    DNA_peak_i = DNA_peak_i + 1

DNA_flat_i = 0

for element in DNA_flat_AA_num:
    DNA_flat_AA_average[DNA_flat_i] = element / DNA_file_counter
    DNA_flat_i = DNA_flat_i + 1

DNA_valley_i = 0

for element in DNA_valley_AA_num:
    DNA_valley_AA_average[DNA_valley_i] = element / DNA_file_counter
    DNA_valley_i = DNA_valley_i + 1

RNA_peak_i = 0

for element in RNA_peak_AA_num:
    RNA_peak_AA_average[RNA_peak_i] = element / RNA_file_counter
    RNA_peak_i = RNA_peak_i + 1

RNA_flat_i = 0

for element in RNA_flat_AA_num:
    RNA_flat_AA_average[RNA_flat_i] = element / RNA_file_counter
    RNA_flat_i = RNA_flat_i + 1

RNA_valley_i = 0

for element in RNA_valley_AA_num:
    RNA_valley_AA_average[RNA_valley_i] = element / RNA_file_counter
    RNA_valley_i = RNA_valley_i + 1

DNA_peak_counter   = DNA_peak_counter   / DNA_file_counter
DNA_flat_counter   = DNA_flat_counter   / DNA_file_counter
DNA_valley_counter = DNA_valley_counter / DNA_file_counter


RNA_peak_counter   = RNA_peak_counter   / RNA_file_counter
RNA_flat_counter   = RNA_flat_counter   / RNA_file_counter
RNA_valley_counter = RNA_valley_counter / RNA_file_counter


print(RNA_peak_counter)
print(RNA_flat_counter)
print(RNA_valley_counter)

print(DNA_peak_counter)
print(DNA_flat_counter)
print(DNA_valley_counter)


# 输出SSB和SSB的各种形状的总数柱状图

shape_list          = ['peak','flat','valley']
RNA_shape_total_num = [RNA_peak_counter,RNA_flat_counter,RNA_valley_counter]
DNA_shape_total_num = [DNA_peak_counter,DNA_flat_counter,DNA_valley_counter]

fig_t, ax_t = plt.subplots()
index = np.arange(3)
bar_width = 0.2

opacity = 0.4
rects1_t = plt.bar(index, RNA_shape_total_num, bar_width,alpha=opacity, color='b',label='SSB')
rects2_t = plt.bar(index + bar_width, DNA_shape_total_num, bar_width,alpha=opacity,color='g',label='DSB')

plt.xlabel('AA_TYPE')
plt.ylabel('NUM')
plt.title('The frequency distributions of amino acid–nucleotide pairs in peak region')
plt.xticks(index + bar_width,shape_list)
plt.ylim(0,DNA_valley_counter*1.5)
plt.legend()

plt.tight_layout()
plt.show()



# 输出SSB和DSB的peak区域的各个氨基酸的分布


fig_p, ax_P = plt.subplots()
index = np.arange(20)
bar_width = 0.2

opacity = 0.4
rects1_p = plt.bar(index, RNA_peak_AA_num, bar_width,alpha=opacity, color='b',label='SSB')
rects2_p = plt.bar(index + bar_width, DNA_peak_AA_num, bar_width,alpha=opacity,color='g',label='DSB')

plt.xlabel('AA_TYPE')
plt.ylabel('NUM')
plt.title('The frequency distributions of amino acid–nucleotide pairs in peak region')
plt.xticks(index + bar_width,AA_TYPE)
plt.ylim(0,max(DNA_peak_AA_num)+1.5)
plt.legend()

plt.tight_layout()
plt.show()


# 输出SSB和DSB的flat区域的各个氨基酸的分布


fig_f, ax_f = plt.subplots()
index = np.arange(20)
bar_width = 0.2

opacity = 0.4
rects1_f = plt.bar(index, RNA_flat_AA_num, bar_width,alpha=opacity, color='b',label='SSB')
rects2_f = plt.bar(index + bar_width, DNA_flat_AA_num, bar_width,alpha=opacity,color='g',label='DSB')

plt.xlabel('AA_TYPE')
plt.ylabel('NUM')
plt.title('The frequency distributions of amino acid–nucleotide pairs in flat region')
plt.xticks(index + bar_width,AA_TYPE)
plt.ylim(0,max(DNA_flat_AA_num)*1.5)
plt.legend()

plt.tight_layout()
plt.show()


# 输出SSB和DSB的valley区域的各个氨基酸的分布


fig_v, ax_v = plt.subplots()
index = np.arange(20)
bar_width = 0.2

opacity = 0.4
rects1_v = plt.bar(index, RNA_valley_AA_num, bar_width,alpha=opacity, color='b',label='SSB')
rects2_v = plt.bar(index + bar_width, DNA_valley_AA_num, bar_width,alpha=opacity,color='g',label='DSB')

plt.xlabel('AA_TYPE')
plt.ylabel('NUM')
plt.title('The frequency distributions of amino acid–nucleotide pairs in valley region')

plt.xticks(index + bar_width,AA_TYPE)
plt.ylim(0,max(DNA_valley_AA_num)*1.5)
plt.legend()

plt.tight_layout()
plt.show()


'''


