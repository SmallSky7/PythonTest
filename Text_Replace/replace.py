# coding=utf-8

import xlrd
import sys
import json

excel_flie = xlrd.open_workbook('C:\\Users\\huxt27670\\Desktop\\工作簿2.xlsx')

excel_flie.sheet_names()
excel_table = excel_flie.sheet_by_name('Sheet1')
excel_rows = int(excel_table.nrows)
excel_vlues = []

f = open('C:\\Users\\huxt27670\\Desktop\\replace.txt', 'r+')

for i in range(0, excel_rows):
    excel_vlues.append(excel_table.cell(i, 0).value)
    new_file = "\n\"" + str(excel_vlues[i]) + "\"" + ":{" + "\n\t\"language\": \"java\"," + "\n\t\"custom_fields\":{" + "\n\t\t\"operator_no\":{" + "\n\t\t\t\"values\":[\"1\"]," + "\n\t\t\t\"flag\":false" + "\n\t\t}," + "\n\t\t\"op_password\":{" + "\n\t\t\t\"values\":[\"AEha3G0G1yf4PfCa0eoZjfMD\"]," + "\n\t\t\t\"flag\":false" + "\n\t\t}" + "\n\t}" + "\n},"
    f.write(new_file)
print("加载完成")
