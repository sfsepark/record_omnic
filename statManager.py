import pymysql
from print_log import print_log, get_log_text
from singleton import SingletonType

class Funzdb:
    def __init__(self):

        #github 오픈판에는 DB 이름이 공개되지 않습니다.

        self.conn = pymysql.connect(host='DB 이름', user='유저', password='비밀번호', db='디비네임', charset='utf8', autocommit=True)
        self.curs = self.conn.cursor()
    
    def add_score(self, rank, total=0, gametype=1):
        self.conn.ping(True)
        sql = 'select `series` from `broadcast` order by `series` desc limit 1;'
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        series = rows[0][0]

        sql = 'insert into `pubg`(`series`, `cur_rank`, `total_rank`, `type`) value(%s, %s, %s, %s)'
        self.curs.execute(sql, (series, rank, total, gametype))


    def add_score_test(self, rank, total=0, gametype=1):
        self.conn.ping(True)
        sql = 'select `series` from `broadcast_test` order by `series` desc limit 1;'
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        series = rows[0][0]

        sql = 'insert into `pubg_test`(`series`, `cur_rank`, `total_rank`, `type`) value(%s, %s, %s, %s)'
        self.curs.execute(sql, (series, rank, total, gametype))

class StatManager :
    __metaclass__ = SingletonType

    def __init__(self) :
        self.funzDB = Funzdb()
    
    def send_log(self, grade, total, isTest = True) :
        grade_data = 'THE RESULT IS........... ' + str(grade) + '/ ' + str(total)
        print_log(grade_data)

        f = open('./log_grade','a')
        f.write(get_log_text(grade_data) + '\n')
        f.close()

        gametype = 1

        if total != 0 :
            if grade > total :
                gametype = 1
            if total <= 12:
                gametype = 1
       #     elif total <= 30:
       #         gametype = 3
            elif total <= 53 :
                gametype = 2
            else :
                gametype = 1

        if isTest == True :
            self.funzDB.add_score_test(grade, total, gametype)
        else :
            self.funzDB.add_score(grade,total,gametype)

