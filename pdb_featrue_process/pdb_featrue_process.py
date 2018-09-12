import os
import os.path
import re
import shape_statistics.calu_pdb_shape as  calu_pdb_shape
import pdb_feature_caclu.pdb_feature_caclu as pdb_feature_caclu
import excel.PDB_excel_module as excel

AA_Type_CHOP780202_value = {'ALA': 0.83, 'ARG': 0.93, 'ASN': 0.89, 'ASP': 0.54, 'CYS': 1.19, 'GLN': 1.10, 'GLU': 0.37, 'GLY': 0.75, 'HIS': 0.87, 'ILE': 1.60,
                            'LEU': 1.30, 'LYS': 0.74, 'MET': 1.05, 'PHE': 1.38, 'PRO': 0.55, 'SER': 0.75, 'THR': 1.19, 'TRP': 1.37, 'TYR': 1.47, 'VAL': 1.70}

AA_Type_CIDH920103_value = {'ALA': 0.36, 'ARG': -0.52, 'ASN': -0.90, 'ASP': -1.09, 'CYS': 0.70,  'GLN': -1.05, 'GLU': -0.83, 'GLY': -0.82, 'HIS': 0.16, 'ILE': 2.17,
                            'LEU': 1.18, 'LYS': -0.56, 'MET': 1.21,  'PHE': 1.01,  'PRO': -0.06, 'SER': -0.60, 'THR': -1.20, 'TRP': 1.31,  'TYR': 1.05, 'VAL': 1.21}

AA_Type_FAUJ880109_value = {'ALA': 0, 'ARG': 4, 'ASN': 2, 'ASP': 1, 'CYS': 0, 'GLN': 2, 'GLU': 1, 'GLY': 0, 'HIS': 1, 'ILE': 0,
                            'LEU': 0, 'LYS': 2, 'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 1, 'THR': 1, 'TRP': 1, 'TYR': 1, 'VAL': 0}

AA_Type_FAUJ880111_value = {'ALA': 0, 'ARG': 1, 'ASN': 0, 'ASP': 0, 'CYS': 0, 'GLN': 0, 'GLU': 0, 'GLY': 0, 'HIS': 1, 'ILE': 0,
                            'LEU': 0, 'LYS': 1, 'MET': 0, 'PHE': 0, 'PRO': 0, 'SER': 0, 'THR': 0, 'TRP': 0, 'TYR': 0, 'VAL': 0}

AA_Type_FINA910104_value = {'ALA': 1, 'ARG': 1.70, 'ASN': 1, 'ASP': 0.70,'CYS': 1,   'GLN': 1, 'GLU': 0.70, 'GLY': 1.50,'HIS': 1,'ILE': 1,
                            'LEU': 1, 'LYS': 1.70, 'MET': 1, 'PHE': 1,   'PRO': 0.10,'SER': 1, 'THR': 1,    'TRP': 1,   'TYR': 1,'VAL': 1}

AA_Type_GEIM800104_value = {'ALA': 1.19, 'ARG': 1,    'ASN': 0.94, 'ASP': 1.07, 'CYS': 0.95, 'GLN': 1.32, 'GLU': 1.64, 'GLY': 0.60, 'HIS': 1.03, 'ILE': 1.12,
                            'LEU': 1.18, 'LYS': 1.27, 'MET': 1.49, 'PHE': 1.02, 'PRO': 0.68, 'SER': 0.81, 'THR': 0.85, 'TRP': 1.18, 'TYR': 0.77, 'VAL': 0.74}

AA_Type_GEIM800106_value = {'ALA': 0.86, 'ARG': 1.15, 'ASN': 0.60, 'ASP': 0.66, 'CYS': 0.91,  'GLN': 1.11, 'GLU': 0.37, 'GLY': 0.86, 'HIS': 1.07, 'ILE': 1.17,
                            'LEU': 1.28, 'LYS': 1.01, 'MET': 1.15,  'PHE':1.34,  'PRO': 0.61, 'SER': 0.91, 'THR': 1.14, 'TRP': 1.13, 'TYR': 1.37, 'VAL': 1.31}

AA_Type_KANM800102_value = {'ALA': 0.81, 'ARG': 0.85, 'ASN': 0.62, 'ASP': 0.71, 'CYS': 1.17, 'GLN': 0.98, 'GLU': 0.53, 'GLY': 0.88, 'HIS': 0.92, 'ILE': 1.48,
                            'LEU': 1.24, 'LYS': 0.77, 'MET': 1.05, 'PHE': 1.20, 'PRO': 0.61, 'SER': 0.92, 'THR': 1.18, 'TRP': 1.18, 'TYR': 1.23, 'VAL': 1.66}

AA_Type_KLEP840101_value = {'ALA': 0, 'ARG': 1, 'ASN': 0, 'ASP': -1, 'CYS': 0, 'GLN': 0, 'GLU': -1, 'GLY': 0, 'HIS': 0, 'ILE': 0,
                            'LEU': 0, 'LYS': 1, 'MET': 0, 'PHE': 0,  'PRO': 0, 'SER': 0, 'THR': 0, 'TRP': 0,  'TYR': 0, 'VAL': 0}

AA_Type_KRIW710101_value = {'ALA': 4.60, 'ARG': 6.50, 'ASN': 5.90, 'ASP': 5.70, 'CYS': -1.00, 'GLN': 6.10, 'GLU': 5.60, 'GLY': 7.60, 'HIS': 4.50, 'ILE': 2.60,
                            'LEU': 3.25, 'LYS': 7.90, 'MET': 1.40, 'PHE': 3.20, 'PRO': 7.00, 'SER': 5.25, 'THR': 4.80, 'TRP': 4.00, 'TYR': 4.35, 'VAL': 3.40}

AA_Type_LIFS790101_value = {'ALA': 0.92, 'ARG': 0.93, 'ASN': 0.60, 'ASP': 0.48, 'CYS': 1.16, 'GLN': 0.95, 'GLU': 0.61, 'GLY': 0.61, 'HIS': 0.93, 'ILE': 1.81,
                            'LEU': 1.30, 'LYS': 0.70, 'MET': 1.19, 'PHE': 1.25, 'PRO': 0.40, 'SER': 0.82, 'THR': 1.12, 'TRP': 1.54, 'TYR': 1.53, 'VAL': 1.81}

AA_Type_MEEJ800101_value = {'ALA':0.5, 'ARG': 0.8, 'ASN': 0.8, 'ASP': -8.2, 'CYS': -6.8, 'GLN': -4.8, 'GLU': -16.9, 'GLY': 0.0, 'HIS': -3.5, 'ILE': 13.9,
                            'LEU':8.8, 'LYS': 0.1, 'MET': 4.8, 'PHE': 13.2, 'PRO': 6.1, 'SER': 1.2, 'THR': 2.7, 'TRP':14.9, 'TYR': 6.1, 'VAL': 2.7}

AA_Type_OOBM770102_value = {'ALA': -1.404, 'ARG': -0.921, 'ASN': -1.178, 'ASP': -1.162, 'CYS': -1.365, 'GLN': -1.116, 'GLU': -1.163, 'GLY': -1.364, 'HIS': -1.215, 'ILE': -1.189,
                            'LEU': -1.315, 'LYS': -1.074, 'MET': -1.303, 'PHE': -1.135, 'PRO': -1.236, 'SER': -1.297, 'THR': -1.252, 'TRP': -1.030, 'TYR': -1.030, 'VAL': -1.254}

AA_Type_PALJ810107_value = {'ALA': 1.08, 'ARG': 0.93, 'ASN': 1.05, 'ASP': 0.86, 'CYS': 1.22, 'GLN': 0.95, 'GLU': 1.09, 'GLY': 0.85, 'HIS': 1.02, 'ILE': 0.98,
                            'LEU': 1.04, 'LYS': 1.01, 'MET': 1.11, 'PHE': 0.96, 'PRO': 0.91, 'SER': 0.95, 'THR': 1.15, 'TRP': 1.17, 'TYR': 0.80, 'VAL': 1.03}

AA_Type_QIAN880123_value = {'ALA': -0.44, 'ARG': -0.13, 'ASN': 0.05, 'ASP': -0.20, 'CYS': 0.13, 'GLN': -0.58, 'GLU': -0.28, 'GLY': 0.08, 'HIS': 0.09, 'ILE': -0.04,
                            'LEU': -0.12, 'LYS': -0.33, 'MET': -0.21, 'PHE': -0.13, 'PRO': -0.48, 'SER': 0.27, 'THR': 0.47, 'TRP': -0.22, 'TYR': -0.11, 'VAL': 0.06}

AA_Type_RACS770103_value = {'ALA': 1.16, 'ARG': 1.72, 'ASN': 1.97, 'ASP': 2.66, 'CYS': 0.50, 'GLN': 3.87, 'GLU': 2.40, 'GLY': 1.63, 'HIS': 0.86, 'ILE': 0.57,
                            'LEU': 0.51, 'LYS': 3.90, 'MET': 0.40, 'PHE': 0.43, 'PRO': 2.04, 'SER': 1.61, 'THR': 1.48, 'TRP': 0.75, 'TYR': 1.72, 'VAL': 0.59}

AA_Type_RADA880108_value = {'ALA': -0.06, 'ARG': -0.84, 'ASN': -0.48, 'ASP': -0.80, 'CYS': 1.36, 'GLN': -0.73, 'GLU': -0.77, 'GLY': -0.41, 'HIS': 0.49, 'ILE': 1.31,
                            'LEU': 1.21, 'LYS': -1.18, 'MET': 1.27, 'PHE': 1.27, 'PRO': 0,     'SER': -0.50, 'THR': -0.27, 'TRP': 0.88, 'TYR': 0.33, 'VAL': 1.09}

AA_Type_ROSM880102_value = {'ALA': -0.67, 'ARG': 3.89, 'ASN': 2.27, 'ASP': 1.57, 'CYS': -2.00, 'GLN': 2.12, 'GLU': 1.78, 'GLY': 0.00, 'HIS': 1.09, 'ILE': -3.02,
                            'LEU': -3.02, 'LYS': 2.46, 'MET': -1.67, 'PHE': -3.24, 'PRO': -1.75, 'SER': 0.10, 'THR':-1.42, 'TRP':-2.86, 'TYR': 0.98, 'VAL': -2.18}

AA_Type_SWER830101_value = {'ALA': -0.40, 'ARG': -0.59, 'ASN': -0.92, 'ASP': -1.31, 'CYS': 0.17, 'GLN': -0.91, 'GLU': -1.22, 'GLY': -0.67, 'HIS': -0.64, 'ILE': 1.25,
                            'LEU': 1.22, 'LYS': -0.67, 'MET': 1.02, 'PHE': 1.92, 'PRO': -0.49, 'SER': -0.55, 'THR': -0.28, 'TRP': 0.50, 'TYR': 1.67, 'VAL': 0.91}

AA_Type_ZIMJ680102_value = {'ALA': 11.50, 'ARG': 14.28, 'ASN': 12.82, 'ASP': 11.68, 'CYS': 13.46, 'GLN': 14.45, 'GLU': 13.57, 'GLY': 3.40, 'HIS': 13.69, 'ILE': 21.40,
                            'LEU': 21.40, 'LYS': 15.71, 'MET': 16.25, 'PHE': 19.80, 'PRO': 17.43, 'SER': 9.47, 'THR': 15.77, 'TRP': 21.67, 'TYR': 18.03, 'VAL': 21.57}

AA_Type_ZIMJ680104_value = {'ALA': 6.00, 'ARG': 10.76, 'ASN': 5.41, 'ASP': 2.77, 'CYS': 5.05, 'GLN': 5.65, 'GLU': 3.22, 'GLY': 5.97, 'HIS': 7.59, 'ILE': 6.02,
                            'LEU': 5.98, 'LYS': 9.74, 'MET': 5.74, 'PHE': 5.48, 'PRO': 6.30, 'SER': 5.68, 'THR': 5.66, 'TRP': 5.89, 'TYR': 5.66, 'VAL': 5.96}

AA_Type_AURR980120_value = {'ALA': 0.71, 'ARG': 1.09, 'ASN': 0.95, 'ASP': 1.43, 'CYS': 0.65, 'GLN': 0.87, 'GLU': 1.19, 'GLY': 1.07, 'HIS': 1.13, 'ILE': 1.05,
                            'LEU': 0.84, 'LYS': 1.10, 'MET': 0.80, 'PHE': 0.95, 'PRO': 1.70, 'SER': 0.65, 'THR': 0.086, 'TRP': 1.25, 'TYR': 0.85, 'VAL': 1.12}

AA_Type_MUNV940103_value = {'ALA': 1.080, 'ARG': 0.976, 'ASN': 1.197, 'ASP': 1.266, 'CYS': 0.733, 'GLN': 1.050, 'GLU': 1.085, 'GLY': 1.104, 'HIS': 0.906, 'ILE': 0.583,
                            'LEU': 0.789, 'LYS': 1.026, 'MET': 0.812, 'PHE': 0.685, 'PRO': 1.412, 'SER': 0.987, 'THR': 0.784, 'TRP': 0.755, 'TYR': 0.665, 'VAL': 0.546}

AA_Type_NADH010104_value = {'ALA': 32, 'ARG': -95, 'ASN': -73, 'ASP': -29, 'CYS': 182, 'GLN': -95, 'GLU': -74, 'GLY': -22, 'HIS': -25, 'ILE': 106,
                            'LEU': 104, 'LYS': -124, 'MET': 82, 'PHE': 132, 'PRO': -82, 'SER': -34, 'THR': 20, 'TRP': 118, 'TYR': 44, 'VAL': 113}

AA_Type_NADH010106_value = {'ALA': 5, 'ARG': -57, 'ASN': -77, 'ASP': 45, 'CYS': 224, 'GLN': -67, 'GLU': -8, 'GLY': -47, 'HIS': -50, 'ILE': 83,
                            'LEU': 82, 'LYS': -38, 'MET': 83, 'PHE': 117, 'PRO': -103, 'SER': -41, 'THR': 79, 'TRP': 130, 'TYR': 27, 'VAL': 117}

AA_Type_GUYH850105_value = {'ALA': -0.27, 'ARG': 2.00, 'ASN': 0.61, 'ASP': 0.50, 'CYS': -0.23, 'GLN': 1.00, 'GLU': 0.33, 'GLY': -0.22, 'HIS': 0.37, 'ILE': -0.80,
                            'LEU': -0.44, 'LYS': 1.17, 'MET': -0.31, 'PHE': -0.55, 'PRO': 0.36, 'SER': 0.17, 'THR': 0.18, 'TRP': 0.05, 'TYR': 0.48, 'VAL': -0.65}

AA_Type_MIYS990104_value = {'ALA': -0.04, 'ARG': 0.07, 'ASN': 0.13, 'ASP': 0.19, 'CYS': -0.38, 'GLN': 0.14, 'GLU': 0.23, 'GLY': 0.09, 'HIS': -0.04, 'ILE': -0.34,
                            'LEU': -0.37, 'LYS': 0.33, 'MET': -0.30, 'PHE': -0.38, 'PRO': 0.19, 'SER': 0.12, 'THR': 0.03, 'TRP': -0.33, 'TYR': -0.29, 'VAL': -0.29}

excel_table_format = {'shape':1,       'CHOP780202':4,  'CIDH920103': 7,  'FAUJ880109': 10, 'FAUJ880111': 13,'FINA910104': 16, 'GEIM800104': 19,
                      'GEIM800106':22, 'KANM800102':25, 'KLEP840101': 28, 'KRIW710101': 31, 'LIFS790101': 34,'MEEJ800101': 37, 'OOBM770102': 40,
                      'PALJ810107':43, 'QIAN880123':46, 'RACS770103': 49, 'RADA880108': 52, 'ROSM880102': 55,'SWER830101': 58, 'ZIMJ680102': 61,
                      'ZIMJ680104':64, 'AURR980120':67, 'MUNV940103': 70, 'NADH010104': 73, 'NADH010106': 76,'GUYH850105': 79, 'MIYS990104': 82}

def pdb_feature_process_function(PDB_Shape_Path):


    #对于残基接口形状进行处理
    calu_pdb_shape.PDB_Shape_Function(PDB_Shape_Path, excel_table_format['shape'])

    #对于属性进行处理

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_CHOP780202_value,PDB_Shape_Path,excel_table_format['CHOP780202'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_CIDH920103_value,PDB_Shape_Path,excel_table_format['CIDH920103'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_FAUJ880109_value,PDB_Shape_Path,excel_table_format['FAUJ880109'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_FAUJ880111_value,PDB_Shape_Path,excel_table_format['FAUJ880111'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_FINA910104_value,PDB_Shape_Path,excel_table_format['FINA910104'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_GEIM800104_value,PDB_Shape_Path,excel_table_format['GEIM800104'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_GEIM800106_value,PDB_Shape_Path,excel_table_format['GEIM800106'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_KANM800102_value,PDB_Shape_Path,excel_table_format['KANM800102'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_KLEP840101_value,PDB_Shape_Path,excel_table_format['KLEP840101'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_KRIW710101_value,PDB_Shape_Path,excel_table_format['KRIW710101'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_LIFS790101_value,PDB_Shape_Path,excel_table_format['LIFS790101'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_MEEJ800101_value,PDB_Shape_Path,excel_table_format['MEEJ800101'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_OOBM770102_value,PDB_Shape_Path,excel_table_format['OOBM770102'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_PALJ810107_value,PDB_Shape_Path,excel_table_format['PALJ810107'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_QIAN880123_value,PDB_Shape_Path,excel_table_format['QIAN880123'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_RACS770103_value,PDB_Shape_Path,excel_table_format['RACS770103'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_RADA880108_value,PDB_Shape_Path,excel_table_format['RADA880108'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_ROSM880102_value,PDB_Shape_Path,excel_table_format['ROSM880102'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_SWER830101_value,PDB_Shape_Path,excel_table_format['SWER830101'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_ZIMJ680102_value,PDB_Shape_Path,excel_table_format['ZIMJ680102'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_ZIMJ680104_value,PDB_Shape_Path,excel_table_format['ZIMJ680104'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_AURR980120_value,PDB_Shape_Path,excel_table_format['AURR980120'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_MUNV940103_value,PDB_Shape_Path,excel_table_format['MUNV940103'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_NADH010104_value,PDB_Shape_Path,excel_table_format['NADH010104'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_NADH010106_value,PDB_Shape_Path,excel_table_format['NADH010106'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_GUYH850105_value,PDB_Shape_Path,excel_table_format['GUYH850105'])

    pdb_feature_caclu.PDB_Shape_feature_Function(AA_Type_MIYS990104_value,PDB_Shape_Path,excel_table_format['MIYS990104'])

def excel_table_head_generate(shape_Path_listdir):

    excel.Excel_Write(0, 0, 0, 'pdb_name')
    row = 1
    for shape_file_name in shape_Path_listdir:
        file_name_m = re.match('(\w+).txt', shape_file_name)
        if file_name_m == None:
            return 0
        else:
            excel.Excel_Write(row,0,0, file_name_m.group(1))
        row = row + 1


    peak_str   = '_peak'
    flat_str   = '_flat'
    valley_str = '_valley'

    for key in excel_table_format:
        peak_featrue   = key + peak_str
        falt_featrue   = key + flat_str
        valley_featrue = key + valley_str

        excel.Excel_Write(0, excel_table_format[key], 0, peak_featrue)
        excel.Excel_Write(0, excel_table_format[key]+1, 0, falt_featrue)
        excel.Excel_Write(0, excel_table_format[key]+2, 0, valley_featrue)

def main():

    print("请输入PDB_shape文件路径")
    PDB_Shape_Path = input()
    os.chdir(PDB_Shape_Path)
    print("您输入的PDB_shape文件存放路径为:",os.getcwd())
    shape_Path_listdir = os.listdir(PDB_Shape_Path)

    excel_table_head_generate(shape_Path_listdir)

    pdb_feature_process_function(PDB_Shape_Path)

main()










