import os
import sys

def syncFunc(orcl_name, table_name):
    dirname = os.path.dirname(os.path.abspath(__file__))
    cmd = 'cd' + ' ' + dirname + '\syncFunc' + ' ' + '&&' + ' ' + 'syncFunc.exe' + ' ' + orcl_name + ' ' + table_name

    if dirname[0] == 'C':
        os.popen(cmd)
    if dirname[0] == 'D':
        cmd1 = 'd:' + ' ' + '&&' + ' ' + cmd
        os.popen(cmd1)
        """print(cmd1)"""
    """print(cmd)"""

"""syncFunc('AS_EALL_BJ#0', 'sysarg')"""         #测试用
syncFunc(sys.argv[1],sys.argv[2])                        #测试用
"""print(sys.argv[1])
print(sys.argv[2])"""