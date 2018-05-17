#encoding: utf-8

import sys
from flask import *
import time
import json
import requests
from file import *
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    context = {
        'username': u'dddd',
        'gender': u'man',
        'age': 18
    }
    return render_template('login.html',**context)

#用户管理
@app.route('/node', methods=['get'])
def get_node():
    return render_template('node.html')

#删除学生
@app.route('/delete_node', methods=['get'])
def get_delete_node():
    return render_template('delete_node.html')

@app.route('/delete_node', methods=['post'])
def submit_delete_node():
    nodes=read_file(NODE_FILENAME)
    n = 0
    logo = {}
    conn={}
    conn['source']=request.form['delete_teacher']
    conn['target']=request.form['delete_student']
    if (conn['source']!='')|(conn['target']!=''):
        for node in nodes:
            if node['name']==conn['source']:
               for stu in node['student']:
                   if stu['target']==conn['target']:
                        node['student'].remove(stu)
                        write_file(NODE_FILENAME, nodes)
                        logo['logo'] = u'删除成功'
                        return render_template('result.html', **logo)
                   n = n + 1
                   if n == len(node['student']):
                       logo['logo'] = u'没有该学生信息'
                       return render_template('result.html', **logo)
            else:
                logo['logo'] = u'没有此用户'
                return render_template('result.html', **logo)
    else:
        logo['logo'] = u'老师姓名和学生姓名不能为空'
        return render_template('result.html', **logo)

#添加学生
@app.route('/add_node', methods=['get'])
def get_add_node():
    return render_template('add_node.html')

@app.route('/add_node', methods=['post'])
def submit_add_node():
    nodes=read_file(NODE_FILENAME)
    logo = {}
    conn={}
    conn['source']=request.form['add_teacher']
    conn['target']=request.form['add_student']
    conn['value'] = '师/生'
    if (conn['source']!='')|(conn['target']!=''):
        for node in nodes:
            if node['name']==conn['source']:
                node['student'].append(conn)
                write_file(NODE_FILENAME, nodes)
                logo['logo'] = u'添加成功'
                return render_template('result.html', **logo)
            else:
                logo['logo'] = u'没有此用户'
                return render_template('result.html', **logo)
    else:
        logo['logo'] = u'老师姓名和学生姓名不能为空'
        return render_template('result.html', **logo)

#师承树
@app.route('/base', methods=['get'])
def get_tree():
    nodes = []
    links = []

    nodes = read_file(NODE_FILENAME)
    for node in nodes:
        try:
            links.extend(node['student'])
        except KeyError:
            print 'error'
    for node in nodes:
        try:
            del node['student']
        except KeyError:
            print 'error'


    data1 = json.dumps(nodes)
    data2 = json.dumps(links)
    return render_template('tree.html',data1 = data1,data2 = data2)

#用户管理
@app.route('/user', methods=['get'])
def get_user():
    return render_template('user.html')

#查找用户
@app.route('/find_user', methods=['get'])
def get_find_user():
    nodes = read_file(NODE_FILENAME)
    datas = []
    for i in nodes:
        data = {}
        data['name'] = i['name']
        data['age'] = i['age']
        data['sex'] = i['sex']
        data['category'] = i['category']
        data['student'] = ''
        try:
            for temp in i['student']:
                data['student'] = data['student'] + temp['target'] + '/'
        except KeyError:
            print 'error'
        datas.append(data)
    data = json.dumps(datas)
    return render_template('find_user.html',data = data)

'''
@app.route('/find_user', methods=['post'])
def submit_find_user():
    users = read_file(NODE_FILENAME)
    user = {}
    logo = {}
    n = 0
    user['name'] = request.form['find_username']
    if user['name'] != '':
        for u in users:
            if user['name'] == u['name'] :
                user = users[n]
                logo['logo'] = u'查找成功'
                return render_template('info_user.html', **user)
            n = n + 1
            if (n == len(users)):
                logo['logo'] = u'没有此用户'
                return render_template('result.html', **logo)
    else:
        logo['logo'] = u'用户名或密码不能为空'
        return render_template('result.html', **logo)
'''

#删除用户
@app.route('/delete_user', methods=['get'])
def get_delete_user():
    return render_template('delete_user.html')

@app.route('/delete_user', methods=['post'])
def submit_delete_user():
    users = read_file(USER_FILENAME)
    user = {}
    logo = {}
    n = 0
    user['name'] = request.form['delete_username']
    if user['name'] != '':
        for u in users:
            if user['name'] == u['name'] :
                del users[n]
                write_log( admin,'删除了用户 用户名名【%s】' % user['name'])
                write_file(USER_FILENAME, users)
                logo['logo'] = u'删除用户成功'
                return render_template('result.html', **logo)
            if (n == len(users)):
                logo['logo'] = u'要删除的用户信息不存在'
                return render_template('result.html', **logo)
            n = n + 1
    else:
        logo['logo'] = u'要删除的用户名不能为空'
        return render_template('result.html', **logo)

#添加用户
@app.route('/add_user', methods=['get'])
def get_add_user():
    return render_template('add_user.html')

@app.route('/add_user', methods=['post'])
def submit_add_user():
    users = read_file(USER_FILENAME)
    user = {}
    logo = {}
    n = 0
    user['name'] = request.form['add_username']
    user['password'] = request.form['add_password']
    if user['name'] != '' and user['password'] != '':
        for u in users:
            n = n + 1
            if user['name'] == u['name'] :
                logo['logo'] = u'用户名已经存在'
                return render_template('result.html', **logo)
                break
            if (n == len(users)):
                write_log(user['name'], '添加成功！')
                logo['logo'] = u'添加成功'
                users.append(user)
                write_file(USER_FILENAME, users)
                return render_template('result.html', **logo)
    else:
        logo['logo'] = u'用户名或密码不能为空'
        return render_template('result.html', **logo)

# 返回首页
@app.route('/main', methods=['get'])
def get_main():
        return render_template('main.html')

#登录函数
@app.route('/login', methods=['get'])
def get_login():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def submit_login():
    users = read_file(USER_FILENAME)
    user = {}
    logo = {}
    n = 0
    user['name'] = request.form['username']
    user['password'] = request.form['password']
    if user['name'] == 'admin' and user['password'] == 'root':
        return render_template('main.html',**logo)
    if user['name'] != '' and user['password'] != '':
        for u in users:
            n = n + 1
            if user['name'] == u['name'] and user['password'] == u['password']:
                write_log(user['name'], '登录成功！')
                logo['logo'] = u'欢迎您登录'
                #登录成功
                return render_template('main.html', **logo)
            if (n == len(users)):
                logo['logo'] = u'用户名或密码错误'
                return render_template('result.html', **logo)
    else:
        logo['logo'] = u'用户名或密码不能为空'
        return render_template('result.html', **logo)


if __name__ == '__main__':
    app.run(host='127.0.0.1')