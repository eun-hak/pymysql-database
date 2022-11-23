# service.py

from vo import Member
from dao_db import MemberDao

# service


class MemberService:
    loginId = ''

    def __init__(self):
        self.dao = MemberDao()

    # 추가. name 중복 허용 안됨

    def addMember(self):
        print('=== 추가 ===')

        id = input('id:')
        pwd = input('pwd:')
        name = input('name:')
        email = input('email:')
        self.dao.insert(Member(id=id, pwd=pwd, name=name, email=email))

    def getById(self):
        print('=== 아이디로 검색 ===')
        id = int(input('search id:'))
        a: Member = self.dao.select(id)
        if a == None:
            print('없는 번호')
        else:
            print(a)

    # 검색: 검색할 이름을 입력받아서 dao로 검색한 결과 출력

    def printMember(self):
        print('=== 이름으로 검색 ===')
        name = input('name:')
        res = self.dao.selectByName('%'+name+'%')
        if res == None:  # 중복 안됨
            print('예외발생')
        elif len(res) == 0:
            print('검색결과 없음')
        else:
            for i in res:
                print(i)

    # 삭제

    def delMember(self):
        print('=== 삭제 ===')
        if MemberService.loginId != '':
            print('로그아웃 하고 진행하세요')
            return
        id = input('id:')
        self.dao.delete(id)

    # 전체출력
    def printAll(self):
        print('=== 전체출력 ===')
        data = self.dao.selectAll()
        for i in data:
            print(i)

    # 로그인
    def login(self):
        if MemberService.loginId != '':
            print('이미 로그인중')
            return
        id = input('아이디 : ')
        a = self.dao.select(id)

        if a == None:
            print('없는 아이디')
            return
        else:
            pwd = input('패스워드 :')
            if pwd == a.pwd:  # 여기가 customer_pwd 여야하지 않을까?
                MemberService.loginId = id
                self.dao.Logined(pwd)
                print('로그인 성공')
            else:
                print('패스워드(이름) 불일치')

    def printMyInfo(self):  # 로그인 상태에서만 사용가능
        if MemberService.loginId == '':
            print('로그인 먼저 하세요')
            return
        else:
            print("내 정보 \n", end="\n ")
            a = self.dao.select(MemberService.loginId)
            a1 = str(a)
            a1 = a1.split(",")

            for i in a1:
                print(i)

            # print('=== 수정 ===')
            # # id = input('id:')
            # # a:Member = self.dao.select(num) #수정전 데이터 검색
            # #
            # # if a == None:  # 중복 안됨
            # #     print('가입되지 않았습니다')
            # # else:
            # s = ['pwd', 'name', 'email']
            # data=[input('new' + s[i]+':') for i in range(len(s))]
            # for idx, i in enumerate(data):
            #     if i != '':
            #         #객체 멤버 변수 수정
            #         a.__setattr__(s[idx], i)

            # self.dao.update(a)

    def logout(self):
        if MemberService.loginId == '':
            print('로그인 먼저 하시오')
            return
        MemberService.loginId = ''
        self.dao.Logout()
        print('로그아웃 완료!')


# 칵테일 관련 기능

    # 칵테일 엔티티 불러오기


    def cocktail_list(self):
        print("\n 칵테일 리스트 \n")
        self.dao.cocktail_select()

    # 칵테일 랭킹 불러오기

    def cocktail_rank(self):
        print("           랭킹\n")
        self.dao.cocktail_rank_select()

    # 칵테일 찾기

    def cocktail_search(self):
        cocktail = input("칵테일 이름을 입력하세요 : ")
        self.dao.cocktail_search_db(cocktail)

    # 칵테일 랭킹 매기기
    def cocktail_grade(self):
        cocktail = input("평점을 매길 칵테일 이름을 입력하세요 : ")
        grade = int(input("점수를 입력하세요 (1~10) : "))
        self.dao.cocktail_grade(cocktail, grade)
    # 칵테일 후기 남기기

    def cocktail_enroll(self):
        cocktail = input("후기를 남길 칵테일을 입력하세요 : ")
        review = input("후기를 입력하세요 : ")

        self.dao.cocktail_review(cocktail, review)
