# -*- coding: utf-8 -*-
# create by Aramis
import time

import pymysql

import server_return

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'uu@5!uacqr!qGZly'
PASSWORD_LOCAL = '123456'
DATABASE = 'moviegetter'
TABLE_USER = 'user'
TABLE_USER_LOG = 'user_log'

ERROR_PERMISSION_DE = server_return.ERROR_PERMISSION_DE
ERROR_PARAMS = server_return.ERROR_PARAMS
ERROR_LOGIC = server_return.ERROR_LOGIC

INDEX_ID = 0
INDEX_IMEI = 1
INDEX_NAME = 2
INDEX_ROLE = 3
INDEX_CREATETIME = 4
INDEX_USABLE = 5

INDEX_LOG_ID = 0
INDEX_LOG_USERID = 1
INDEX_LOG_IMEI = 2
INDEX_LOG_USERNAME = 3
INDEX_LOG_LOGINTIME = 4
INDEX_LOG_LOGOUTITME = 5
INDEX_LOG_LOCAL = 6
INDEX_LOG_IP = 7


class MysqlClient(object):

    def __init__(self):
        try:
            self.db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE,
                                      charset='utf8', port=3306)
        except:
            self.db = pymysql.connect(host=HOST, user=USER, password=PASSWORD_LOCAL, database=DATABASE,
                                      charset='utf8', port=3306)
        self.cursor = self.db.cursor()

    def create_user(self, root_imei, imei, role, usable, name):
        """
        创建/更新用户（更新时，只改变role,name和usable字段）
        :param root_imei:
        :param imei:
        :param role:
        :param usable:
        :param name:
        :return:
        """
        self.cursor.execute('select role from {table} where imei = {imei};'.format(table=TABLE_USER, imei=root_imei))
        # root_role = self.cursor.fetchone()
        # print(type(root_role), root_role)
        if self.cursor.fetchone()[0] == 'root':
            count_sql = 'select count(*) from user where imei = "{imei}";'.format(imei=imei)
            self.cursor.execute(count_sql)
            if self.cursor.fetchone()[0] == 0:
                # 插入新用户
                return self._save_new_normal_user(imei, root_imei, usable, name)
            else:
                # 更新 只改变role,name和usable字段
                self.cursor.execute('select * from user where imei = "{imei}";'.format(imei=imei))
                user = self.cursor.fetchone()
                print('更新 select')
                print(user)
                _role = user[3] if role is None else role
                _usable = user[5] if usable is None else usable
                # _name = '' if name is None else name
                update_sql = 'update {table} set role=\"{role}\",usable={usable},name=\"{name}\" where imei ={imei};' \
                    .format(table=TABLE_USER, role=_role, imei=imei, usable=_usable, name=name)
                try:
                    print('更新', update_sql)
                    self.cursor.execute(update_sql)
                    self.db.commit()
                    return server_return.server_success('更新成功')
                except:
                    return server_return.server_error(server_return.ERROR_DB)
        else:
            return server_return.server_error(ERROR_PERMISSION_DE)

    def _save_new_user(self, imei, role, usable, name):
        """
        插入新用户(普通)
        :param imei:
        :param role:
        :param usable:
        :param name:
        :return: json
        """
        print('插入新用户')
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        _name = '' if name is None else name
        _usable = 1 if usable is None else usable
        _role = 'normal' if role is None else role
        sql = 'insert into {table}(imei,role,create_time,name,usable) values (\"{imei}\",\"{role}\",\"{create_time}\",\"{name}\",\"{usable}\");' \
            .format(table=TABLE_USER, role=_role, imei=imei, create_time=now, name=_name, usable=_usable)
        try:
            # print('插入新用户', sql)
            self.cursor.execute(sql)
            self.db.commit()
            return server_return.server_success('插入成功')
        except:
            return server_return.server_error(server_return.ERROR_DB)

    def select_role(self, imei):
        sql = 'select * from user where imei = %s;' % imei
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        if user:
            return server_return.server_success(user[INDEX_ROLE])
        else:
            insert_result = self._save_new_user(imei, None, None, None)
            if insert_result['code'] == 200:
                return server_return.server_success('normal')
            else:
                return insert_result

    def mark_in(self, imei, login_time, local, ip):
        select_sql = 'select * from {table} where imei = {imei}' \
            .format(table=TABLE_USER, imei=imei)
        self.cursor.execute(select_sql)
        user = self.cursor.fetchone()
        if user:
            user_id = user[INDEX_ID]
            username = user[INDEX_NAME]
            values_str = ' values({user_id},\"{imei}\",\"{login_time}\"' \
                .format(user_id=user_id, imei=imei, login_time=login_time)
            insert_sql = 'insert into {table}(user_id,imei,login_time'.format(table=TABLE_USER_LOG)
            if username:
                insert_sql += ',username'
                values_str += ',\"{username}\"'.format(username=username)
            if local:
                insert_sql += ',local'
                values_str += ',\"{local}\"'.format(local=local)
            if ip:
                insert_sql += ',ip'
                values_str += ',\"{ip}\"'.format(ip=ip)
            f_insert_sql = insert_sql + ')' + values_str + ');'

            print('mark_in', f_insert_sql)

            try:
                self.cursor.execute(f_insert_sql)
                lastrowid = self.cursor.lastrowid
                self.db.commit()
                return server_return.server_success({'mark_id': lastrowid})
            except:
                return server_return.server_error(server_return.ERROR_DB)


        else:
            return server_return.server_error(server_return.ERROR_DB, '用户不存在')

    def mark_out(self, id, logout_time):
        update_sql = 'update {table} set logout_time = \"{logout_time}\" where id=\"{id}\";' \
            .format(table=TABLE_USER_LOG, logout_time=logout_time, id=id)
        try:
            print('mark_out:',update_sql)
            self.cursor.execute(update_sql)
            self.db.commit()
            return server_return.server_success('更新成功')
        except:
            return server_return.server_error(server_return.ERROR_DB)

    def _to_user_log_bean(self, s: tuple):
        return {'id': s[0],
                'user_id': s[1],
                'imei': s[2],
                'username': s[3],
                'login_time': s[4],
                'logout_time': s[5],
                'local': s[6],
                'ip': s[7]}