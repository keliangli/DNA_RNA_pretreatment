import re
import os


list1 = ('KARS160112','CHAM830108','KARS160114','KARS160115')

file_handle = open("E:\\DNA_RNA分类项目\\AAindex\\AAindex.txt", 'r')


def match_function(str1,str2):

    if re.match(str1,str2)!=None:
        return 1
    else:
        return 0

def match_aaindex_content_head(file_content):
    CA_head = re.match('(H) (\w+)', file_content)
    if CA_head == None:
        return 0
    else:
        return CA_head.group(2)


for file_content in file_handle:
    str1 = list1[1]
    str2 = match_aaindex_content_head(file_content)
    if str2 == str1:
        print(str2)
