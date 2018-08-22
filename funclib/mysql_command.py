# coding=utf-8
import time

import pymysql


class Mysql(object):
    def __init__(self, user='root', passwd='admin123', db='test'):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                port=3306,
                user=user,
                passwd=passwd,
                db=db,
                charset='utf8'
            )
        except Exception as e:
            print(e)
        else:
            print('数据库连接成功')
            self.cur = self.conn.cursor()

    def create_table(self, table_name, table_title):
        sql = 'create table ' + table_name + '%s' % table_title
        res = self.cur.execute(sql)
        print(res)

    def close(self):
        self.cur.close()
        self.conn.close()

    def add(self, table_name, table_title, add_content):  # 增
        sql = 'insert into ' + table_name + '%s' % table_title + 'values' + '%s' % add_content
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def rem(self, table_name):  # 删
        sql = 'drop table ' + table_name
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def mod(self):  # 改
        sql = 'update testtb set name="Tom Ding" where id=2'
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def show(self):  # 查
        sql = 'select * from testtb'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i)


def time_now():
    return time.strftime('%Y%m%d_%H%M%S')


if __name__ == "__main__":
    mysql = Mysql()
    try:
        pass
        # mysql.create_table('table_time', '(version varchar(10), back(avg) float, back(max) float), home(avg) float, home(max) float), force(avg) float, force(max) float)')
        # mysql.add('test_01', '(version, back(avg), back(max), home(avg), home(max), force(avg), force(max))', '(%s, %s, %s, %s, %s, %s, %s)' % (app_version, t_b_avg, t_b_max, t_h_avg, t_h_max, t_f_avg, t_f_max)
    except Exception as e:
        print(e)
    finally:
        mysql.close()
