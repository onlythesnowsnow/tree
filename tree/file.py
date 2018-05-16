#encoding: utf-8
import time
import sys
import requests
import json
reload(sys)
sys.setdefaultencoding('utf-8')
NODE_FILENAME = 'nodes.txt'
#常量，存的是节点信息的文件名
USER_FILENAME = 'user.txt'
#常量，存的是存储用户信息的文件名
LOG_FILENAME = 'nodes.log'
#常量，存的是日志文件名
admin = '管理员'

#文件操作
def read_file(filename):
    '''
    用来读取文件内容，返回一个字典
    :param filename: 文件名
    :return: 文件N内容的字典
    :
    '''
    with open(filename,'a+') as fr:
        fr.seek(0)    #2从末尾开始
        content = fr.read()
        print content
        if len(content):#这里判断文件内容是否为空的，如果不为0的话就为是真
           return eval(content)
        return []

def write_file(filename,content):
    '''
    用来读取文件内容，返回一个字典
    :param filename: 文件名
    :return: 文件N内容的字典
    '''
    with open(filename,'a+') as fw:
        fw.seek(0)
        fw.truncate()
        fw.write(str(content))
def write_log(username,operation):
    '''
    写日志函数
    :param username:用户名
    :param operation:用户的操作信息
    :return:
    '''
    w_time = time.strftime('%Y-%m-%d %H%M%S')
    with open(LOG_FILENAME,'a+') as fw:
        log_content = '%s %s %s \n'%(w_time,username,operation)
        fw.write(log_content)
