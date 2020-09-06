# -*- coding: UTF-8 -*-

import paramiko
import re
import cx_Oracle
from hslib.common import logger

log = logger.getlogger()

def Log2sql(clouddict, uiexpect=None):
    try:
        cx_Oracle.init_oracle_client(lib_dir=r'D:\\instantclient_11_2')
    except Exception as e:
        if str(e) == 'Oracle Client library has already been initialized':
            pass
        else:
            log.info(str(e) + '\n请检查数据库是否是32位，建议可以安装一个32位的instantclient')
            return

    host = clouddict.get('host', None)
    port = int(clouddict.get('port', None))  # 端口是int类型pp
    username = clouddict.get('username', None)
    password = clouddict.get('password', None)
    logpath = clouddict.get('logpath', None)

    get_log = ssh_test(host, port, username, password, logpath)
    log.info('推送日志:' + get_log)
    logsplit = get_log.split('\n')
    for i in range(0, len(logsplit)):
        log_dict = strsplit(logsplit[i])
        if log_dict != 0:
            tooracle(log_dict)
            log.info('>>>数据已同步至数据库<<<')


# SSH连接，语句执行
def ssh_test(host, port, username, password, logpath):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password)
        log.info('连接至{}:{}'.format(host, port))
    except Exception as e:
        log.info(e)
        return

    # 设置一个内部函数，执行shell命令并返回输出结果
    def run_shell(cmd):
        ssh_in, ssh_out, ssh_error = ssh.exec_command(cmd)
        result = ssh_out.read() or ssh_error.read()
        return result.decode().strip()

    # 获取指定日志中的内容
    """
    cmd_get_log = 'cd ' + logpath + ';tail -n 2 Bizlog.log | head -1'
    """
    cmd_get_log = 'cd ' + logpath + ';cat Bizlog.log'
    get_log = run_shell(cmd_get_log)

    # 关闭连接
    ssh.close()
    return get_log


# 对获取到的日志作分割
def strsplit(strline):
    sql_dict = {
        'log_date': '',
        'log_time': '',
        'log_info': '',
        'method': '',
        'operation': '',
        'trace_id': '',
        'log_data': '',
        'log_indexes': '',
        'jourNumber': '',
        'jourNumber_flag': 0,
        'log_topic': '',
    }

    if re.search('send message to mq|send end', strline) is None:
        return 0

    sql_dict['log_date'] = strline[0:10]
    sql_dict['log_time'] = strline[11:23]
    regex1 = re.compile(r'\[(.*?)\]')
    sql_dict['log_info'] = regex1.findall(strline)[0]
    regex2 = re.compile(r'\] (.*?) \[')
    sql_dict['method'] = regex2.findall(strline)[0]
    regex3 = re.compile(r'\-\|(.*?),')
    sql_dict['operation'] = regex3.findall(strline)[0]

    log_line = "{" + strline.split(sql_dict['operation'] + ", ")[1] + "}"
    log2dict = eval(log_line)  # 格式化成dict格式，方便处理

    sql_dict['trace_id'] = log2dict.get('trace_id')

    if log2dict.get('message'):
        log_message = log2dict.get('message')
        sql_dict['log_data'] = log_message.get('data')
        sql_dict['log_indexes'] = log_message.get('indexes')
        sql_dict['jourNumber'] = log_message.get('jourNumber')
        sql_dict['log_topic'] = log_message.get('topic')
    else:
        sql_dict['log_data'] = log2dict.get('data')
        sql_dict['log_indexes'] = log2dict.get('indexs')
        sql_dict['jourNumber'] = log2dict.get('jour_number')
        sql_dict['log_topic'] = log2dict.get('topic')

    # 保证不会传null
    for key in sql_dict:
        if sql_dict[key] is None:
            sql_dict[key] = ' '

    return sql_dict


# 将分割后的数据同步至数据库
def tooracle(data_dict):
    log_date = str(data_dict['log_date'])
    log_time = str(data_dict['log_time'])
    log_info = str(data_dict['log_info'])
    method = str(data_dict['method'])
    operation = str(data_dict['operation'])
    trace_id = str(data_dict['trace_id'])
    log_data = str(data_dict['log_data'])
    log_indexes = str(data_dict['log_indexes'])
    journumber = str(data_dict['jourNumber'])
    journumber_flag = str(data_dict['jourNumber_flag'])
    log_topic = str(data_dict['log_topic'])

    key_list = [log_date, log_time, log_info, method, operation, trace_id, log_data, log_indexes, journumber,
                journumber_flag, log_topic]
    for i in range(0, len(key_list)):
        a = key_list[i].split("'")
        b = "''".join(a)
        key_list[i] = b

    # 数据库信息
    username = u'HSSEE'
    password = u'hundsun'
    host = u'10.20.25.249'
    port = u'1521'
    a = host + ":" + port + "/orcl"

    try:
        conn = cx_Oracle.connect(username, password, a, encoding='UTF-8')
    except Exception as e:
        print(e)
        return
    cur = conn.cursor()

    # 将分割后的日志插入数据库
    sql1 = 'insert into hssee.log_bizlog (LOG_DATE, LOG_TIME, LOG_INFO, METHOD, OPERATION, TRACE_ID, LOG_DATA, LOG_INDEXES, JOURNUMBER, JOURNUMBER_FLAG, LOG_TOPIC) values ('
    for i in range(0, len(key_list)):
        sql1 = sql1 + "'" + key_list[i] + "',"
    sql1 = sql1[0:-1] + ")"

    cur.execute(sql1)
    conn.commit()

    # 找出数据库中是否有topic、info、operation、journumber都相同的数据
    sql2 = 'select count(1) from hssee.log_bizlog where log_topic = \'{}\' and log_info = \'{}\' and operation = \'{}\' and journumber = \'{}\''.format(
        log_topic, log_info, operation, journumber)
    cur.execute(sql2)
    a = cur.fetchone()

    # 将都相同的数据的journumber_flag置为1
    if int(a[0]) > 1:
        sql3 = 'update hssee.log_bizlog set journumber_flag = 1 where log_topic = \'{}\' and log_info = \'{}\' and operation = \'{}\' and journumber = \'{}\''.format(
            log_topic, log_info, operation, journumber)
        cur.execute(sql3)
        conn.commit()

    cur.close()
    conn.close()


'''
# 测试用
clouddict = {
    "host": "10.20.18.202",
    "port": "22",
    "username": "root",
    "password": "520@UF3.0",
    "logpath": "/home/hundsun/server/broker-act/logs/",
}
Log2sql(clouddict)
'''
