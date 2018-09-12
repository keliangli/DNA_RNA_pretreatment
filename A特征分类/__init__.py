import xlrd
from xlrd import open_workbook
from xlutils.copy import copy
import numpy as np
import pandas as pd
import excel.PDB_excel_module as PDB_excel_module
from  sklearn import cross_validation

from sklearn.ensemble import RandomForestClassifier


def Excel_Read(row, column):
    # 打开指定路径中的xls文件
    read_file = r'E:\数据实验区\分类特征向量表.xls'

    book = xlrd.open_workbook(read_file)  # 得到Excel文件的book对象
    # 得到sheet对象

    sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
    # 通过坐标读取表格中的数据

    cell_value = sheet0.cell_value(row, column)

    return cell_value



def aaindex_feature_svm_test(RNA_last_row, RNA_last_column):
    data = np.zeros((RNA_last_row, RNA_last_column))
    row_counter = 0
    column_counter = 0
    while row_counter < RNA_last_row:
        while column_counter < RNA_last_column:
            data[row_counter][column_counter] = Excel_Read(row_counter, column_counter)
            column_counter = column_counter + 1
        column_counter = 0
        row_counter = row_counter + 1
    row_counter = 0

    data_content = data[:, 0:RNA_last_column - 1]
    data_target = data[:, RNA_last_column - 1]

    #随机森林
    rfc = RandomForestClassifier()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(data_content, data_target, test_size=0.25,random_state=33)

    rfc.fit(X_train, y_train)
    rfc_result = rfc.score(X_test, y_test)

    print("随机森林的精确度为：",rfc_result)

    from sklearn.linear_model import  LogisticRegression

    #逻辑回归
    lr = LogisticRegression()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(data_content, data_target, test_size=0.25,random_state=33)

    lr.fit(X_train, y_train)
    lr_result = lr.score(X_test, y_test)

    print("逻辑回归的精确度为：",lr_result)

    #支持向量机
    from sklearn.svm import LinearSVC
    lsvc = LinearSVC()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(data_content, data_target, test_size=0.25,random_state=33)

    lsvc.fit(X_train, y_train)
    lsvc_result = lsvc.score(X_test, y_test)

    print("支持向量机的精确度为：",lsvc_result)



def main():
    aaindex_feature_svm_test(250,4 )


main()