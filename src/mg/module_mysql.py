# -*- coding: utf-8 -*-
# create by Aramis
import time
import datetime
import pymysql
import requests
from scrapy.selector import Selector

import server_return
import json

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'woshinanshen'
PASSWORD_LOCAL = '123456'
DATABASE = 'moviegetter'
TABLE_USER = 'user'
TABLE_USER_LOG = 'user_log'
TABLE_USER_MOVIE = 'user_movie_log'

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
            self.db = pymysql.connect(host=HOST, user='lizhidan', password=PASSWORD, database=DATABASE,
                                      charset='utf8', port=3306)
        except:
            self.db = pymysql.connect(host=HOST, user=USER, password=PASSWORD_LOCAL, database=DATABASE,
                                      charset='utf8', port=3306)
        self.cursor = self.db.cursor()
        # self._create_table()

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
            return server_return.server_success({'role': user[INDEX_ROLE]})
        else:
            insert_result = self._save_new_user(imei, None, None, None)
            if insert_result['code'] == 200:
                return server_return.server_success('normal')
            else:
                return insert_result

    def mark_in(self, imei, login_time, local, ip, version_code, version_name):
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
            if version_code:
                insert_sql += ',version_code'
                values_str += ',{version_code}'.format(version_code=version_code)
            if version_name:
                insert_sql += ',version_name'
                values_str += ',\"{version_name}\"'.format(version_name=version_name)
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
            print('mark_out:', update_sql)
            self.cursor.execute(update_sql)
            self.db.commit()
            return server_return.server_success('更新成功')
        except:
            return server_return.server_error(server_return.ERROR_DB)

    def mark_movie(self, imei, movie_id, movie_name, downloaded_time, downloaded_timestamp):
        select_url = "select * from {table} where imei = \"{imei}\";".format(table=TABLE_USER, imei=imei)
        self.cursor.execute(select_url)
        user = self.cursor.fetchone()
        if user:
            user_id = user[INDEX_ID]
            user_name = user[INDEX_NAME]
            sql = 'insert into {table}(userId,userName,movieId,movieName,downloaded_time,' \
                  'downloaded_timestamp) values({userId},\"{userName}\",{movieId},\"{movieName}\",\"{downloaded_time}\",' \
                  '{downloaded_timestamp});'.format(table=TABLE_USER_MOVIE, userId=user_id, userName=user_name,
                                                    movieId=movie_id, movieName=movie_name,
                                                    downloaded_time=downloaded_time,
                                                    downloaded_timestamp=downloaded_timestamp)
            try:
                print('记录数据', sql)
                self.cursor.execute(sql)
                self.db.commit()
                return server_return.server_success('记录成功')
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

    def check_version(self):
        select_sql = 'select * from versions where is_current = 1;'
        self.cursor.execute(select_sql)
        version = self.cursor.fetchone()
        print(version)
        # if current_version:
        #     # print('===', current_version)
        #     db_version_code = int(current_version[1])
        #     if db_version_code < version_code:
        #         insert_sql = 'insert into versions(version_code,version_name,is_current,create_time) values({version_code},\"{version_name}\",1,curdate())'.format(
        #             version_code=version_code, version_name=version_name)
        #         update_sql = 'update versions set is_current = 0 where id = {id}'.format(id=current_version[0])
        #         self.cursor.execute(insert_sql)
        #         self.cursor.execute(update_sql)
        #         self.db.commit()
        #         return server_return.server_success(
        #             {'version_code': version_code, 'version_name': version_name, 'is_current': 1})
        #     else:
        #         return server_return.server_success(
        #             {'version_code': current_version[1], 'version_name': current_version[2],
        #              'is_current': current_version[3]})
        #
        # else:
        #     insert_sql = 'insert into versions(version_code,version_name,is_current,create_time) values({version_code},\"{version_name}\",1,curdate())'.format(
        #         version_code=version_code, version_name=version_name)
        #     self.cursor.execute(insert_sql)
        #     self.db.commit()

        t=version[4]
        t2=t.strftime('%Y-%m-%d %H:%M:%S')
        print(type(t),t)
        print("t2",t2)
        r = {
            'version_code': version[1],
            'version_name': version[2],
            'is_current': version[3],
            'create_time': version[4].strftime('%Y-%m-%d %H:%M:%S'),
            'message': version[5],
            'url': version[6],
            'is_force': version[7],
        }
        return server_return.server_success(r)

    def save_version(self, file_name: str, version_code: int, version_name: str, is_current: int, message: str,
                     is_force: int):
        select_sql = 'select id,version_code from versions;'
        self.cursor.execute(select_sql)
        codes = self.cursor.fetchall()
        print(codes, codes)
        is_update = False
        for i in codes:
            if version_code == int(i[1]):
                is_update = True
                break

        file_url = '/download/apk/{file_name}'.format(file_name=file_name)
        if is_update:
            update_code_sql = 'update versions set version_name=\"{version_name}\",is_current={is_current},message=\"{message}\",is_force={is_force},url=\"{url}\" where version_code={version_code};'.format(
                version_name=version_name, is_current=is_current, message=message, is_force=is_force, url=file_url,version_code=version_code)
            print('更新同version_code',update_code_sql)
            self.cursor.execute(update_code_sql)
            self.db.commit()
        else:
            if is_current > 0:
                update_sql = 'update versions set is_current=0 where is_current>0;'
                self.cursor.execute(update_sql)
            sql = 'insert into versions(version_code,version_name,is_current,message,is_force,url,create_time) values({version_code},\"{version_name}\",{is_current},\"{message}\",{is_force},\"{url}\",CURRENT_TIME )'.format(
                version_code=version_code, version_name=version_name, is_current=is_current, message=message,
                is_force=is_force, url=file_url)
            self.cursor.execute(sql)
            self.db.commit()

    def mark_in_ip(self, ip, mark_id):
        local = None
        try:
            res = requests.get('http://ip.zxinc.org/ipquery/?ip={ip}'.format(ip=ip))
            selector = Selector(text=res.text)
            local = selector.xpath('//form[@method="get"]//tr[4]/td[2]/text()').extract_first()
        except:
            pass
        sets = 'ip=\"{ip}\"'.format(ip=ip)
        if local:
            sets += ',local=\"{local}\"'.format(local=local)
        update_sql = 'update {table} set {sets} where id = {mark_id}'.format(table=TABLE_USER_LOG, sets=sets,
                                                                             mark_id=mark_id)
        print('update_sql', update_sql)
        try:
            self.cursor.execute(update_sql)
            self.db.commit()
            return server_return.server_success('更新成功')
        except:
            return server_return.server_error(server_return.ERROR_DB, update_sql)

    def _create_table(self):
        create_1 = "CREATE TABLE IF NOT EXISTS `user`(\
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
  `imei` varchar(50) DEFAULT NULL,\
  `name` varchar(50) DEFAULT NULL,\
  `role` varchar(20) DEFAULT NULL,\
  `create_time` varchar(50) DEFAULT NULL,\
  `usable` int(4) NOT NULL DEFAULT '1' COMMENT '是否可用',\
  PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;"
        create_2 = "CREATE TABLE IF NOT EXISTS `user_log` (\
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
  `user_id` int(11) DEFAULT NULL,\
  `imei` varchar(50) DEFAULT NULL,\
  `username` varchar(50) DEFAULT NULL,\
  `login_time` varchar(50) DEFAULT NULL,\
  `logout_time` varchar(50) DEFAULT NULL,\
  `local` varchar(50) DEFAULT NULL,\
  `ip` varchar(50) DEFAULT NULL,\
  PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;"
        self.cursor.execute(create_1)
        self.cursor.execute(create_2)
        self.db.commit()

        # self.cursor.execute("show tables like '{table}'".format(table=TABLE_USER))
        # if self.cursor.fetchone() is None:
        #     self.cursor.execute(create_1)
        #     self.db.commit()
        # self.cursor.execute("show tables like '{table}'".format(table=TABLE_USER_LOG))
        # if self.cursor.fetchone() is None:
        #     self.cursor.execute(create_2)
        #     self.db.commit()

    def save(self, sql: str):
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def get_movie_board_data(self, tag, limit=10, offset=0):

        hour = int(time.strftime('%H', time.localtime(time.time())))
        date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 3600 if hour < 10 else time.time()))
        print(date)
        sql = 'select * from maoyan_board where tag={tag} and update_time=\"{date}\" limit {limit} offset {offset}'.format(
            tag=tag, limit=limit,
            offset=offset, date=date)
        self.cursor.execute(sql)
        ts = self.cursor.fetchall()

        def to_dict(t: tuple):
            return {
                'id': t[0],
                'movie_name': t[1],
                'movie_id': t[2],
                'movie_year': t[3],
                'actors': t[4],
                'score': t[5],
                'ranking': t[6],
                'update_time': str(t[7]),
                'sync_time': str(t[8]),
                'description': t[9],
                'wanna_watch': t[10],
                'wanna_watch_all': t[11],
                'boxoffice': t[12],
                'boxoffice_all': t[13],
                'boxoffice_lastweek': t[14],
                'tag': t[15],
                'tag_name': t[16],
                'cover_image': t[17],
                'images': t[18]
            }

        return [to_dict(i) for i in ts]

    def __del__(self):
        self.db.close()


if __name__ == '__main__':
    c = MysqlClient()

    r = c.get_movie_board_data(0, 10)
    print(r)
