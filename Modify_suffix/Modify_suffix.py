import os
import sys

old_suffix = sys.argv[1]
new_suffix = sys.argv[2]
filepath = sys.argv[3]
count = 0

if filepath == ' ' or filepath == None:
    filepath = os.path.dirname(os.path.abspath(__file__))

files = os.listdir(filepath)

for file in files:
    portion = os.path.splitext(file)
    if portion[1] == old_suffix:
        count = count + 1
        newname = portion[0] + new_suffix
        os.chdir(filepath)
        os.rename(file, newname)
if count == 0:
    print("\n该文件夹下没有后缀为" + old_suffix + "的文件")
else:
    print("\n后缀已经修改为" + new_suffix)

