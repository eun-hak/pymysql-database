import pymysql

from vo import Member
import re

# Dao


class MemberDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(
            host='localhost', user='root', password='akfmzh7979', db='cocktaildb', charset='utf8')

    def disconn(self):
        self.conn.close()

    # 추가 메서드
    def insert(self, a: Member):
        try:

            # 1. db 커넥션 수립
            self.connect()

            # 2. 사용할 cursor객체 생성. db 작업 메서드가 이 클래스에 정의되어 있으므로 꼭 필요.
            cursor = self.conn.cursor()

            # WHERE not exists(SELECT customer_id from cocktaildb.member)

            # 3. 실행할 sql문 정의
            sql = 'insert into member(customer_id, customer_pw, name, email, isLoggined) values(%s, %s, %s, %s, %s) '

            # 4. sql 문에 %s를 사용했다면 각 자리에 들어갈 값을 튜플로 정의
            d = (a.id, a.pwd, a.name, a.email, "0")

            # 5. sql 실행(실행할 sql, %s매칭한 튜플)
            cursor.execute(sql, d)

            # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
            self.conn.commit()
        except Exception as e:
            print("아이디가 중복되었습니다")
        finally:

            # db 커넥션 끊음
            self.disconn()

    # 검색 메서드

    def select(self, id: str):  # num(pk) 기준 검색. 1개 검색
        try:
            self.connect()  # db 연결
            cursor = self.conn.cursor()  # 사용할 커서 객체 생성
            # 구현 하긴 했는데 왜이런지 모르겠음
            sql = 'select (customer_id),(customer_pw),(name),(email) from member where customer_id=%s'
            d = (id,)
            cursor.execute(sql, d)  # sql 실행
            row = cursor.fetchone()  # fetchone(): 현재 커서 위치의 한줄 추출
            if row:

                return Member(row[0], row[1], row[2], row[3])
                # 0번 인덱스는 ID 1번부터 id pw name email
        except Exception as e:
            print(e)
        finally:
            self.disconn()

    # 검색 메서드
    def selectByName(self, name: str):  # name 기준 검색. 여러개 검색
        try:
            self.connect()  # db연결
            cursor = self.conn.cursor()  # 사용할 커서 객체 생성
            sql = 'select*from member where name like %s'
            d = (name,)
            cursor.execute(sql, d)  # sql 실행
            res = [Member(row[0], row[1], row[2], row[3]) for row in cursor]

            return res

        except Exception as e:
            print(e)
        finally:
            self.disconn()

    # 삭제(name)
    def delete(self, id: str):
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = 'delete from member where customer_id = %s'
            d = (id,)
            cursor.execute(sql, d)
            self.conn.commit()

            return print('삭제가 완료되었습니다.')

        except Exception as e:
            print(e)
        finally:
            self.disconn()

    def update(self, a: Member):
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = 'update member set customer_pw=%s, name=%s, email=%s where cutomer_id=%s'

            d = (a.pwd, a.name, a.email, a.id)
            cursor.execute(sql, d)
            self.conn.commit()

            return print('수정 완료')

        except Exception as e:
            print(e)
        finally:
            self.disconn()

    def selectAll(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = 'select * from member'
            cursor.execute(sql)
            res = [Member(row[0], row[1], row[2], row[3]) for row in cursor]
            return res

        except Exception as e:
            print(e)

        finally:
            self.disconn()

    # 로그인시 isLoggined가 0에서 1로 바뀌도록
    # + 종료시 모든 isLoggined 0으로

    def Logined(self, pwd):
        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()
        # 사용할 sql문

        sql = 'UPDATE cocktaildb.member SET isLoggined = "1" WHERE customer_pw = %s ;'

        cursor.execute(sql, pwd)
        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()

    # 로그아웃 및 창 종료시 모든 로그인여부 0으로 통일
    def Logout(self):
        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()
        # 사용할 sql문

        sql = 'UPDATE cocktaildb.member SET isLoggined = "0" WHERE isLoggined = "1";'

        cursor.execute(sql,)
        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()


# 칵테일
    # 칵테일 리스트 불러오기


    def cocktail_select(self):
        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()
        # 사용할 sql문

        sql = 'SELECT name FROM cocktaildb.cocktail_entity'

        cursor.execute(sql,)
        value = cursor.fetchall()

        value1 = str(value)

        value1 = re.sub("\(", "", value1)
        value1 = re.sub("\)", "", value1)
        value2 = value1.split(',,')

        Count = 1
        for i in value2:
            print(Count, ":", i)
            Count += 1

        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()

    # 칵테일 랭킹 불러오기

    def cocktail_rank_select(self):
        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()
        # 사용할 sql문
        sql = 'SELECT name FROM cocktaildb.cocktail_entity order by cocktail_entity.average_grade DESC;'
        sql2 = 'SELECT average_grade FROM cocktaildb.cocktail_entity order by cocktail_entity.average_grade DESC;'

        cursor.execute(sql,)
        value = cursor.fetchall()
        cursor.execute(sql2,)
        grade = cursor.fetchall()
        count = 1
        list_value = str(value)

        # 문자열에서 , ( ) 삭제하기

        rank_value = re.sub(",", "", list_value)
        rank_value = re.sub("\(", "", list_value)
        rank_value2 = re.sub("\)", "", rank_value)
        rank_value2 = re.sub("'", "", rank_value2)
        rank_value2 = re.sub(" ", "", rank_value2)

        rank_value3 = str(rank_value2)
        rank_value4 = rank_value3.split(",,")

        # 완성된 칵테일 문자열
        # print(rank_value4)

        grade1 = str(grade)
        grade1 = re.sub(",", "", grade1)
        grade1 = re.sub("\(", "", grade1)
        grade1 = re.sub("\)", "", grade1)

        grade2 = str(grade1)

        grade3 = grade2.split(" ")
        # 완성된 칵테일 등수
        # print(grade3)


        #10등까지만 보여줌
        for i in range(0,10,1):
            print("%d 등 = %s   점수 : %s" % (count, rank_value4[i], grade3[i]))

            count += 1

        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()

    # 칵테일 검색

    def cocktail_search_db(self, name):
        try:

            self.connect()  # db 연결
            cursor = self.conn.cursor()  # 사용할 커서 객체 생성

            # sql2 = 'UPDATE cocktaildb.cocktail_entity SET review = (SELECT GROUP_CONCAT( customer_ID, ":" ,enroll_review) FROM cocktaildb.evaluation_entity WHERE Cocktail_ID = %s AND NOT enroll_review IS NULL) WHERE name = %s ;'
            # f = (name, name)
            # cursor.execute(sql2, f)

            # 칵테일 찾기
            sql = 'SELECT name,ingredients,made,review FROM cocktaildb.cocktail_entity where name = %s'

            d = (name,)
            cursor.execute(sql, d)  # sql 실행
            search = cursor.fetchall()
            search_str = str(search)
            search_str.strip()
            search_split = search_str.split(',')

            a = search_split[0]
            a = re.sub("\(", "", a)

            b = search_split[1]
            b = re.sub("\(", "", b)
            c = search_split[2]
            c = re.sub("\)", "", c)
            c = re.sub("'", "", c)
            c1 = str(c)
            c2 = c1.split(".")

            d = search_split[3:]
            d1 = str(d)
            d1 = re.sub("\)", "", d1)
            d1 = re.sub("'", "", d1)
            d1 = re.sub("\[", "", d1)
            d1 = re.sub("\]", "", d1)
            d1 = re.sub('"', "", d1)
            d2 = d1.split(",")

            print('\n')
            print("술 이름 :", a, "\n")
            print("준비물 :", b, "\n")

            print("만드는 방법 \n")
            for i in c2:
                print(i, end="\n ")

            print("\n후기 \n")
            for j in d2:
                print(j)

            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconn()

    # 칵테일 랭킹 매기기(평균까지 한번에 계산)
    def cocktail_grade(self, cocktail, grade):
        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()
        # 사용할 sql문

        # 'insert into cocktaildb.evaluation_entity(enroll_grade) values(%d)'

        sql = 'insert into cocktaildb.evaluation_entity(Cocktail_ID,enroll_grade) values(%s,%s)'
        d = (cocktail, grade)
        cursor.execute(sql, d)

        # 평균값을 계산하는 sql문 (update 사용하고 SET에는 평가엔티티의 점수값을 평균 내서 등록)
        sql2 = 'UPDATE cocktaildb.cocktail_entity SET average_grade = (SELECT ROUND(AVG(enroll_grade),1) FROM cocktaildb.evaluation_entity WHERE Cocktail_ID = %s ) WHERE name = %s'
        f = (cocktail, cocktail)
        cursor.execute(sql2, f)

        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()

    # 칵테일 후기 작성  (작성후 바로 칵테일 테이블에 등록)
    def cocktail_review(self, cocktail, review):

        # DB 연결
        self.connect()
        # 사용할 객체 커서 설정
        cursor = self.conn.cursor()

        # 사용할 sql문
        # 로그인되면 isloggined가 1이므로 그 값에 해당하는 name을 찾아서 누가 후기를 등록했는지 알 수 있게 해줌
        sql = 'insert into cocktaildb.evaluation_entity(Cocktail_ID,enroll_review,customer_ID) values(%s,%s,(SELECT name FROM member WHERE isLoggined = "1"));'

        d = (cocktail, review)

        cursor.execute(sql, d)

        # 칵테일을 검색할 때 마다 후기 업데이트 (검색한 칵테일의 이름 값에 해당하는 리뷰를 불러옴) ##중요!!!        GROUP_CONCAT : 문자열 하나로 합쳐줌
        sql2 = 'UPDATE cocktaildb.cocktail_entity SET review = (SELECT GROUP_CONCAT( customer_ID, ":" ,enroll_review) FROM cocktaildb.evaluation_entity WHERE Cocktail_ID = %s AND NOT enroll_review IS NULL) WHERE name = %s ;'
        f = (cocktail, cocktail)
        cursor.execute(sql2, f)

        # 6. 쓰기동작(insert, update, delete) 에서 쓰기 완료
        self.conn.commit()

        # db 커넥션 끊음
        self.disconn()
