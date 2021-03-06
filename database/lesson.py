# -*- coding:utf-8 -*-

import pymysql
import configparser
#课程数据库操作
class lessonDatabase:
    #读取配置文件中的数据
    cf=configparser.ConfigParser()
    cf.read("classGrabConf.conf","utf-8")
    databaseName=cf.get("database","databaseName")
    host = cf.get("database","host")
    port = cf.getint("database","port")
    username = cf.get("database","username")
    password = cf.get("database","password")
    @staticmethod
    #连接数据库
    def __connectdb():
        try:
            conn = pymysql.connect(host=lessonDatabase.host,user=lessonDatabase.username
                                  ,passwd=lessonDatabase.password,db=lessonDatabase.databaseName,port=lessonDatabase.port
                                   ,charset='utf8')
            #创建一个数据库连接
            return conn
        except Exception:print("连接数据库失败！")
    @staticmethod
    def createLessonTable(userNumber):
        conn = lessonDatabase.__connectdb()
        #得到表名
        tableName="LessonsTable_"+userNumber
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = conn.cursor()
            # 使用 execute() 方法执行 SQL，如果表存在则删除

            # 使用预处理语句创建表
            cursor.execute(("DROP TABLE IF EXISTS %s")%(tableName))
            sql = """CREATE TABLE %s (
                     TYPE VARCHAR(20),
                     NAME  VARCHAR(50) ,
                     URL  TEXT,
                     TIME VARCHAR(100),
                     TEACHER VARCHAR(50),
                     CAPACITY SMALLINT,
                     NUMHAVECHOSED SMALLINT,
                     CREDIT FLOAT
                      )"""%(tableName)
            cursor.execute(sql)
        except Exception:print("创建数据表失败！")
        # 关闭数据库连接
        finally:
            conn.close()
    @staticmethod
    def updateLessons(userNumber,lessonInfoList):
        #得到表名
        tableName="LessonsTable_"+userNumber
        conn = lessonDatabase.__connectdb()
        cursor = conn.cursor()
        try:
            for index in range(len(lessonInfoList)):
                if index==0:
                    continue
                sql='''SELECT COUNT(*) FROM %s WHERE URL = '%s' '''%(tableName,lessonInfoList[index]["url"])
                try:
                    cursor.execute(sql)
                    result=cursor.fetchone()
                    # 数据存在,先删除
                    if result[0]!=0:
                        sql='''DELETE FROM %s WHERE URL ='%s' '''%(tableName,lessonInfoList[index]["url"])
                        try:
                            cursor.execute(sql)
                            conn.commit()
                        except Exception:
                            print("删除失败")
                            conn.rollback()
                except Exception:print("查询失败")
                sql='''INSERT INTO %s (TYPE,NAME,URL,TIME,TEACHER,CAPACITY,NUMHAVECHOSED,CREDIT) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')'''%(tableName,lessonInfoList[0],lessonInfoList[index]["lessonName"],
                    lessonInfoList[index]["url"],lessonInfoList[index]["lessonTime"],lessonInfoList[index]["teacher"],lessonInfoList[index]["capacity"],lessonInfoList[index]["numHaveChosed"],lessonInfoList[index]["credit"])
                try:
                    cursor.execute(sql)
                    conn.commit()
                except:
                    #回滚
                    print("添加失败")
                    conn.rollback()
        finally:
            conn.close()
    @staticmethod
    #加载全部课程
    def queryAllLEssons(userNumber):
        conn = lessonDatabase.__connectdb()
        cursor = conn.cursor()
        tableName="LessonsTable_"+userNumber
        sql ='''SELECT * FROM %s'''%(tableName)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            conn.rollback()
        finally:
            conn.close()
    #按课程名查询课程
    @staticmethod
    def queryLessonsByName(userNumber,lessonName):
        conn = lessonDatabase.__connectdb()
        cursor = conn.cursor()
        tableName="LessonsTable_"+userNumber
        sql ='''SELECT * FROM %s where name like '%s' '''%(tableName,("%"+lessonName+"%"))
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            conn.rollback()
        finally:
            conn.close()
    #按教师姓名查询课程
    @staticmethod
    def queryLessonsByTeacher(userNumber, teacherName):
        conn = lessonDatabase.__connectdb()
        cursor = conn.cursor()
        tableName = "LessonsTable_" + userNumber
        sql = '''SELECT * FROM %s where teacher like '%s' ''' % (tableName, ("%" + teacherName + "%"))
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            conn.rollback()
        finally:
            conn.close()
    #按学分查询课程
    @staticmethod
    def queryLessonsByCredit(userNumber, credit):
        conn = lessonDatabase.__connectdb()
        cursor = conn.cursor()
        tableName = "LessonsTable_" + userNumber
        sql = '''SELECT * FROM %s where credit = '%s' ''' % (tableName,credit)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            conn.rollback()
        finally:
            conn.close()
            # lessInfo = {
            #     "lessonName": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(2)").text(),
            #     "url": url,
            #     "lessonTime": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(4)").attr(
            #         "title"),
            #     "teacher": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(3) a").text(),
            #     "capacity": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(6)").text(),
            #     "numHaveChosed": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(8)").text(),
            #     "credit": pqHtmlData("#gxkxk_wxkc_tb tbody").children("tr").eq(j).find("td:nth-child(10)").text(),
            # }

