# coding=utf-8

import xlrd
import sys

excel_flie = xlrd.open_workbook('C:\\Users\\huxt27670\\Desktop\\新建 Microsoft Excel 工作表.xlsx')
excel_flie.sheet_names()#获取标签名
excel_table = excel_flie.sheet_by_name('Sheet1')#获取标签名下的数据
excel_rows = int(excel_table.nrows)#获取excel行数
excel_vlues = []

for i in range(0, excel_rows):
    excel_vlues.append(excel_table.cell(i, 1).value)
print(str(excel_vlues))