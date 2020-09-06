import sys
import time


def print_act(word):
    sys.stdout.write("\r")  # 让光标回到行首
    sys.stdout.flush()  # 缓冲区的数据全部输出
    for item in word:
        sys.stdout.write(item)
        sys.stdout.flush()
        time.sleep(0.3)


print('  访澳游客     ' + chr(0xf090) + ' ' + chr(0xf091) + '     访澳游客  ')
while True:
    print_act('VISITANTES           VISITANTES')
