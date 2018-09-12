import re

#去冗余结束后文件名称处理程序
#作用：能将fccc产生的结果提取出名字，然后按照名字进行下载

def match_the_pdb_file_name(pdb_file_name):

        CA_m = re.match('(\S{4}).*', pdb_file_name)
        if CA_m == None:
            return 0
        else:
            return CA_m.group(1)


def DNA_pdb_file_name_generate():

    file_content_handle  = open("E:\pdb_file_name.txt", 'r')
    file_write_handle    = open("E:\pdb_file_name_output.txt", 'a')

    counter = 0
    for file_name in file_content_handle:
        pdb_file_name = match_the_pdb_file_name(file_name)
        if pdb_file_name != 0:
            counter = counter + 1
            file_write_handle.write(str(pdb_file_name))
            file_write_handle.write(' ,')
    print(counter)


'''
def main():

    DNA_pdb_file_name_generate()


main()
'''