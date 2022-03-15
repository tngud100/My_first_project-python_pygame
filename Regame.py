import pygame
from beat import *
from class_get import get

class set(get):
    # 초기화 및 변수 지정    
    def __init__(self):
        # 스크린 설정
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_center = (self.screen_width / 2, self.screen_height / 2)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 노래 및 효과음
        self.star_music = pygame.mixer.Sound("first_copy/image/Sound/별똥별.mp3")
        self.next_key = pygame.mixer.Sound("first_copy/image/Sound/MP_핑거스냅 1.mp3")
        self.river_music = pygame.mixer.Sound("first_copy/image/Sound/한적한 감성 카페.mp3")
        self.key_down_sound = pygame.mixer.Sound("first_copy/image/Sound/keydown_button.mp3")
        self.key_up_sound = pygame.mixer.Sound("first_copy/image/Sound/keyup_button.mp3")

        # start_버튼 이미지
        self.start_load = pygame.image.load("first_copy/image/start_load.png")
        self.start_msg = pygame.image.load("first_copy/image/start_msg.png")

        # 메뉴 스크린 주소
        self.menu_screen0_img = pygame.image.load("first_copy/image/background0.png")    # discript
        self.menu_screen1_img = pygame.image.load("first_copy/image/background1.png")    # start
        self.menu_screen2_img = pygame.image.load("first_copy/image/background2.png")    # exit

        # 메뉴 버튼 이미지
        self.left_mani = pygame.image.load("first_copy/image/menu0.png")    # 좌클릭 시
        self.mani = pygame.image.load("first_copy/image/menu1.png")
        self.right_mani = pygame.image.load("first_copy/image/menu2.png")    # 우클릭 시

        self.key_press = 1

        self.b = get(self.mani) # 버튼 1, 클래스 호출
        self.l = get(self.left_mani)
        self.r = get(self.right_mani)
        b_indi_center = self.b.individual_pos(self.screen_width / 2, self.screen_height - (self.screen_height / 8))
        self.b.center_pos(b_indi_center)
        l_indi_center = self.l.individual_pos(self.screen_width / 2, self.screen_height - (self.screen_height / 8))
        self.l.center_pos(l_indi_center)
        r_indi_center = self.r.individual_pos(self.screen_width / 2, self.screen_height - (self.screen_height / 8))
        self.r.center_pos(r_indi_center)

        # 설명서 이미지
        self.instruction = pygame.image.load("first_copy/image/instruction.png")
    
        # 색깔
        self.black = (0, 0, 0) # 검정
        self.white = (255, 255, 255) # 흰색

        # 노래 실행중 변수
        self.menu_music = 0
       
        # 게임 실행중 변수
        self.run = True

        # 게임 시작 변수
        self.start = False

        # 현재 상황, 장면(스크린) 변수 
        self.state = 0 # 게임준비, 1 = 메뉴스크린, 2 = 첫번째 게임 시작, 3 = 두번째 게임 시작, 4 = 세번째 게임 시작, 5 = 게임 오버 스크린 

        # 메뉴 버튼 초기 설정
        self.choose = 1

    # start_버튼 그리기
    def start_button_screen(self):
        # 시작화면 페이드
        s = fade(self.screen_width, self.screen_height, self.screen, self.start_load)
        m = fade(self.screen_width, self.screen_height, self.screen, self.start_msg)
        s.fade_in()
        m.fade_in()
        s.fade_out_start(self.white, self.start_msg)
        self.state = 1
        self.start = True

    # 메뉴 스크린 함수
    def menu_screen(self):
        if self.choose == 0:    # dis
            self.screen.blit(self.menu_screen1_img, (0, 0))
        if self.choose == 1:    # start
            self.screen.blit(self.menu_screen0_img, (0, 0))
        if self.choose == 2:    # Exit
            self.screen.blit(self.menu_screen2_img, (0, 0))

        if self.key_press == 0:
            self.l.blit(self.screen, self.left_mani)
        if self.key_press == 1:
            self.b.blit(self.screen, self.mani)
        if self.key_press == 2:
            self.r.blit(self.screen, self.right_mani)

            # self.l.blit(self.screen, self.left_mani)
            # self.r.blit(self.screen, self.right_mani)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("SH_mini Game")
set.__init__(set)

while set.run:
    click_pos = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set.run = False
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            print(click_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                set.key_down_sound.play()
                set.key_press -= 1
                if set.key_press < 0:
                    set.key_press = 0
            if event.key == pygame.K_RIGHT:
                set.key_down_sound.play()
                set.key_press += 1
                if set.key_press > 2:
                    set.key_press = 2
            if event.key == pygame.K_SPACE:
                set.next_key.play()
                if set.state == 1:
                    set.state = set.choose + 2
            if event.key == pygame.K_ESCAPE:
                if set.state == 2:
                    set.state = 1
                if set.state == 3:
                    set.state = 1
                if set.state == 4:
                    set.state = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                set.key_up_sound.play()
                set.key_press = 1
                if set.choose <= 0:
                    set.choose = 0
                else:
                    set.choose -= 1
            if event.key == pygame.K_RIGHT:
                set.key_up_sound.play()
                set.key_press = 1
                if set.choose >= 2:
                    set.choose = 2
                else:
                    set.choose += 1
            print(event.key)
            print(set.key_press)
            print(set.choose)
    set.screen.fill(set.black)

    if set.start == True:
        if set.state == 1:
            set.star_music.stop()
            set.menu_screen(set)
            if set.menu_music == 0:
                set.river_music.play()
                set.menu_music = 1

        # 첫 번째 게임 실행
        if set.state == 2:
            set.river_music.stop()
            g_2 = g2(set.screen, set.screen_width, set.screen_height, set.state, click_pos)
            if g_2.state == 1:
                set.state = 1
                set.menu_music = 0

        if set.state == 3:
            set.screen.blit(set.instruction, (0,0))
            
        if set.state == 4:
            set.run = False
            pygame.quit()
    else:
        if set.state == 0:
            set.star_music.play()
            set.start_button_screen(set)
        

    if click_pos != 0 :
        # set.click_button(set, click_pos)
        print("set.state = "+str(set.state))

    pygame.display.update()


pygame.display.update()

pygame.quit()
        