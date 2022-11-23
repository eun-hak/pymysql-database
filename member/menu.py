from service import MemberService
from vo import Member
from dao_db import MemberDao

class Menu:
    def __init__(self):
        self.service = MemberService()
        self.dao = MemberDao()
    def run(self):

        while True:
            m = input(
                'ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n\n1.회원가입 \n2.로그인 \n3.내 정보확인 \n4.로그아웃 \n5.탈퇴 \n6.칵테일 창 가기 \n7.종료 \n\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n')
            if m == '1':
                self.service.addMember()
            elif m == '2':
                self.service.login()
            elif m == '3':
                self.service.printMyInfo()
            elif m == '4':
                self.service.logout()
            elif m == '5':
                self.service.delMember()
            elif m == '6':


                while True:
                    if MemberService.loginId == '':
                        print('로그인 먼저 하세요')
                        break
                    n = input(
                        'ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n\n1.칵테일 리스트확인 \n2.칵테일 찾기 \n3.랭킹 확인 \n4.칵테일 평점주기 \n5.칵테일 후기 남기기 \n6.뒤로가기 \n\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ \n')
                    if n == '1':
                        self.service.cocktail_list()
                    if n == '2':
                        self.service.cocktail_search()
                    if n == '3':
                        self.service.cocktail_rank()
                    if n == '4':
                        self.service.cocktail_grade()
                    if n == '5':
                        self.service.cocktail_enroll()
                    if n == '6':
                        break
            elif m == '7':
                self.dao.Logout()
                break


if __name__ == '__main__':
    m = Menu()
    m.run()
