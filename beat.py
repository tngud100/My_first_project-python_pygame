from random import *
import decimal
import pygame
from class_get import *

class g2(var):
    def __init__(self, screen, screen_width, screen_height, state, click_pos):
        super().__init__(screen, screen_width, screen_height, state, click_pos)
        # 외부에서 가져와야될 이미지 및 파일
        self.ready_nomal = pygame.image.load("image/ready_screen_nomal.png") # ready_screen_draw 배경
        self.ready_easy = pygame.image.load("image/ready_screen_easy.png") # ready_screen_draw 배경
        self.ready_hard = pygame.image.load("image/ready_screen_hard.png") # ready_screen_draw 배경
        self.ingame_background = pygame.image.load("image/ingame_screen.png")# ingame 배경
        self.game_over_background1 = pygame.image.load("image/game_over_screen_no.png")# game_over 배경
        self.game_over_background2 = pygame.image.load("image/game_over_screen_yes.png")# game_over 배경
        self.nomal_note = pygame.image.load("image/nomal_note.png")
        self.side_note = pygame.image.load("image/side_note.png")
        self.note_pad = pygame.image.load("image/note_pad.png") # 노트패드
        self.nomal_note_pad = pygame.image.load("image/nomal_note_pad.png") # 노말 노트를 맞추는 패드
        self.side_note_pad = pygame.image.load("image/side_note_pad.png") # 사이드 노트를 맞추는 패드
        self.pad_line = pygame.image.load("image/pad_line.png") # 패드라인
        self.red_line = pygame.image.load("image/red_line.png")
        self.exerlent_img = pygame.image.load("image/Exerlent.png")
        self.good_img = pygame.image.load("image/good.png")
        self.bad_img = pygame.image.load("image/bad.png")


        self.music = pygame.mixer.music.load("image/Sound/빠른 비트.mp3") # ingame 노래
        self.rhythm_start = pygame.mixer.Sound("image/Sound/Dj 스크레치.mp3")
        # self.kick_sound = pygame.mixer.Sound("image/Sound/귀여운 퍽.mp3")
        # self.high_edge_sound = pygame.mixer.Sound("image/Sound/MP_슬레이트 치기.mp3")
        
        # 폰트
        self.combo_font = pygame.font.Font(None, 120)

        # 색깔
        self.White = (255, 255, 255)

        # note
        self.note_list = [] # 노트가 들어가 있는 변수
        self.note_grid = [0,0,0,0] # 노트가 생길 수 있는 칸 
        self.note_state = 2 # 2 = Bad, 1 = good, 0 = Exerlent
        self.i = 0     # 노트 만들기 위한 반복 루트 변수

        s = get(self.side_note) # side노트 사이즈
        n = get(self.nomal_note) # nomal노트 사이즈
        
        self.note_y_pos = [] # 노트 y축 좌표
        self.note_speed = 13

        self.note1_x_pos = self.screen_width / 2 - s.object_width * 2   # 노트1 x_pos
        self.note2_x_pos = self.screen_width / 2 - n.object_width       # 노트2 x_pos
        self.note3_x_pos = self.screen_width / 2                        # 노트3 x_pos
        self.note4_x_pos = self.screen_width / 2 + s.object_width       # 노트4 x_pos
        
        # note_pad
        self.p = get(self.note_pad) # 사이즈 가져오기
        self.note_pad_y_pos = self.screen_height - (self.screen_height / 8) # 노트 패드 y위치
        self.p.individual_pos(self.screen_width / 2, self.note_pad_y_pos)
        self.note_pad_state = 0 # 기본, 1 = 노말, 2 = 사이드

        # 키값 변수
        self.key_press = [0,0,0,0] # d,f,j,k 키값 변수
        self.score_press = 0

        # Score 변수
        self.erase = 0  # 맞춘 노트패드 지우기
        self.approximate = 60 # good을 받을 수 있는 +- 값
        self.Exerlent_range = [self.note_pad_y_pos - self.p.object_height, self.note_pad_y_pos]
        self.score_state = 0 # 1 = Exer, 2 = good, 3 = bad
        self.note_sequence_list = [0]   # 노트가 생성될 때 노트의 높이를 저장 하는 리스트
        self.m = 0  # sequence_list 변수가 append 할 수 있도록 해주는 변수
        self.h = 0  # 점수 로직을 위한 count변수
        self.Exerlent = 0
        self.good = 0
        self.bad = 0
        self.score = 0

        # beat
        self.whole_time = 78 # 노래 전체 시간
        self.part_time = [15,30, 37, 45, 60, 75,78] # 15초, 15초, 7초, 8초, 15초, 15초      --> 비트가 바뀌는 파트
        self.part_beat = []
        # [1.0, 0.7, 0.5, 0.25]
        # [0.8, 0.65, 0.4, 0.2]
        # [0.5, 0.3, 0.25, 0.15]
         # 1/4, 1/4(엇박), 1/8, 1/16 박자 + part6 = 'part4' + 'part1']    --> 사용되는 비트
        self.beat = [0,0,0,0,0,0,0]
        self.beat_time_list = [] # 실제 비트시간이 들어가는 리스트
        self.a = True   # 비트 만들기 위한 반복 루프 변수

        self.difficulty = 1 # 노멀, 0 = 이지, 2 = 하드
        self.screen_state = 0 # 준비 화면, 1 = 게임중, 2 = 게임 오버
        self.start_time = 0 # 시작 시간
        # 리스트별 인덱스 카운트, 화면에 동시 존재 할 수 있는 노트가 최대 count(note_count)만큼 나옴
        self.note_count = [0,0,0,0,0,0,0,0]
        self.frame = pygame.time.Clock() # 프레임설정
        self.over_state = 0
        self.time = 0
        
        pygame.mixer.init()
        
        # 두번째 게임이 실행 중
        while self.state == 2:
            self.fps = self.frame.tick(60) # 프레임 130
            self.run()
            pygame.display.update() # 게임화면을 다시 그리기!



    def run(self):
        for self.event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
                if self.event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
                    set.run = False # 게임이 진행중이 아님
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_SPACE:
                        if self.screen_state == 0:
                            self.rhythm_start.play()
                            pygame.time.delay(2000)
                            self.screen_state = 1
                            pygame.mixer.music.play()
                            self.start_time = pygame.time.get_ticks() # 시작 시간
                            print("START : "+str(self.part_beat))
                            self.music_sheet(self.part_beat)
                        if self.screen_state == 2:
                            if self.over_state == 0:
                                self.state = 1
                            if self.over_state == 1:
                                self.screen_state = 0
                    if self.event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        if self.screen_state == 0:
                            self.state = 1
                        if self.screen_state == 1:
                            self.screen_state = 0
                    # 키값 받기
                    if self.event.key == pygame.K_LEFT:
                        if self.screen_state == 0: 
                            self.difficulty -= 1    # 0 = 이지, 1 = 노말, 2 = 하드
                            if self.difficulty < 0:
                                self.difficulty = 0
                        if self.screen_state == 2:
                            self.over_state = 1
                    if self.event.key == pygame.K_RIGHT:
                        if self.screen_state == 0:
                            self.difficulty += 1
                            if self.difficulty > 2:
                                self.difficulty = 2
                        if self.screen_state == 2:
                            self.over_state = 0
                    if self.event.key == pygame.K_d:
                        if self.screen_state == 1:
                            self.key_press[0] = 1
                            self.Score(0)   
                    if self.event.key == pygame.K_f:
                        if self.screen_state == 1:
                            self.key_press[1] = 1
                            self.Score(1)      
                    if self.event.key == pygame.K_j:
                        if self.screen_state == 1: 
                            self.key_press[2] = 1
                            self.Score(2)    
                    if self.event.key == pygame.K_k:
                        if self.screen_state == 1: 
                            self.key_press[3] = 1
                            self.Score(3)
                    print(self.key_press)
                      
                
                if self.event.type == pygame.KEYUP:
                    if self.event.key == pygame.K_d:
                        if self.screen_state == 1:
                            self.key_press[0] = 0
                    if self.event.key == pygame.K_f:
                        if self.screen_state == 1: 
                            self.key_press[1] = 0
                    if self.event.key == pygame.K_j:
                        if self.screen_state == 1: 
                            self.key_press[2] = 0
                    if self.event.key == pygame.K_k:
                        if self.screen_state == 1: 
                            self.key_press[3] = 0


        if self.screen_state == 0: # 게임 준비 화면
            self.screen_state = 0
            pygame.mixer.music.stop()
            self.ready_screen_draw()

        if self.screen_state == 2: # 게임 오버
            self.game_over_draw()
        
        if self.screen_state == 1: # 게임 중
            self.ingame_draw()


    def ready_screen_draw(self): # 0 = 이지, 1 = 노말, 2 = 하드
        # 리스트 초기화 및 비트 설정
        if self.difficulty == 0:
            self.screen.blit(self.ready_easy, (0,0))
            self.part_beat = [1.0, 0.8, 0.5, 0.3]
        if self.difficulty == 1:
            self.screen.blit(self.ready_nomal, (0,0))
            self.part_beat = [0.8, 0.6, 0.4, 0.2]
        if self.difficulty == 2:
            self.screen.blit(self.ready_hard, (0,0))
            self.part_beat = [0.5, 0.4, 0.3, 0.15]
        self.note_count = [0,0,0,0,0,0,0,0]
        self.beat = [0,0,0,0,0,0,0]
        self.beat_time_list = []
        self.note_y_pos = []
        self.note_list = []
        self.note_sequence_list = [0]
        self.m = 0
        self.h = 0
        self.i = 0
        self.bad = 0
        self.good = 0
        self.Exerlent = 0
        self.score = 0

    def ingame_draw(self):
        self.time = (pygame.time.get_ticks() - self.start_time)/ 1000
        self.time1 = round(self.time,1)
        if self.time1 >= 45:
            self.time1 = round(self.time,2)
            self.time1 = round(decimal.Decimal(self.time1),2)   # 부동소수점 보완

        if self.time1 >= self.part_time[6]: # 게임 클리어 시간
            self.screen_state = 2

        self.screen.blit(self.ingame_background, (0,0)) # 배경 화면 그리기
        self.p.blit(self.screen, self.note_pad) # 노트 패드 그리기
        pygame.draw.circle(self.screen, (255, 255, 255), (self.screen_width/2,self.Exerlent_range[0] - self.approximate),5,5)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.screen_width/2,self.Exerlent_range[0]),5,5)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.screen_width/2,self.Exerlent_range[1]),5,5)

        # 노트 라인 그리기
        if self.key_press[0] == 1:
            self.screen.blit(self.pad_line, (self.note1_x_pos, 10))
            self.p.blit(self.screen, self.side_note_pad)
        if self.key_press[1] == 1:
            self.screen.blit(self.pad_line, (self.note2_x_pos, 10))
            self.p.blit(self.screen, self.nomal_note_pad)
        if self.key_press[2] == 1:
            self.screen.blit(self.pad_line, (self.note3_x_pos, 10))
            self.p.blit(self.screen, self.nomal_note_pad)
        if self.key_press[3] == 1:
            self.screen.blit(self.pad_line, (self.note4_x_pos, 10))
            self.p.blit(self.screen, self.side_note_pad)
        
        # 점수 콤보 그리기
        cell_text = self.combo_font.render(str(self.score), True, self.White)
        text_rect = cell_text.get_rect(center = (self.screen_width / 2, 200))
        self.screen.blit(cell_text, text_rect)

        # 점수 현황 그리기
        if self.score_state == 0:
            pass
        if self.score_state == 1:
            self.screen.blit(self.exerlent_img, (self.note2_x_pos, 100))
        if self.score_state == 2:
            self.screen.blit(self.good_img, (self.note2_x_pos + 50, 100))
        if self.score_state == 3:
            self.screen.blit(self.bad_img, (self.note2_x_pos + 50, 100))
        

        # 비트시간초를 지나면 노트 y값 넘겨주면서 다음 노트 그리기
        if self.note_count[0] <= len(self.note_list) - 5:
            if self.time1 > self.beat_time_list[self.note_count[0]]:
                if self.time1 >= self.beat_time_list[self.note_count[1]]:
                    if self.time1 >= self.beat_time_list[self.note_count[2]]:
                        if self.time1 >= self.beat_time_list[self.note_count[3]]:
                            if self.time1 >= self.beat_time_list[self.note_count[4]]:
                                if self.time1 >= self.beat_time_list[self.note_count[5]]:
                                    if self.time1 >= self.beat_time_list[self.note_count[6]]:
                                        self.note_count[7] = self.note_count[6]
                                    self.note_count[6] = self.note_count[5]
                                self.note_count[5] = self.note_count[4]
                            self.note_count[4] = self.note_count[3]
                        self.note_count[3] = self.note_count[2]
                    self.note_count[2] = self.note_count[1]
                self.note_count[1] = self.note_count[0]
                self.note_count[0] = self.note_count[0] + 1
                self.note_sequence_list.append(0)   # 노트가 생길 때 마다 리스트에 변수 추가
                self.m += 1
                
            # 비트시간초 지나기 전에 떨어지는 노트 그리기
            if self.time1 <= self.beat_time_list[self.note_count[0]]:
                self.auto_draw(self.note_count[0])
                if self.time1 > self.beat_time_list[self.note_count[1]]: # 2번째 노트(노트 스피드가 2배가 되는것을 방지)
                    self.auto_draw(self.note_count[1])
                if self.time1 > self.beat_time_list[self.note_count[2]]: # 3번째 노트(노트 스피드가 2배가 되는것을 방지)
                    self.auto_draw(self.note_count[2])
                    self.auto_draw(self.note_count[3])
                    if self.time1 > self.part_time[1]:
                        self.auto_draw(self.note_count[4])
                        self.auto_draw(self.note_count[5])
                        self.auto_draw(self.note_count[6])
                        self.auto_draw(self.note_count[7])

        else:
            self.auto_draw(self.note_count[0])
            self.auto_draw(self.note_count[1])
            self.auto_draw(self.note_count[2])
            self.auto_draw(self.note_count[3])
            self.auto_draw(self.note_count[4])
            self.auto_draw(self.note_count[5])
            self.auto_draw(self.note_count[6])
            self.auto_draw(self.note_count[7])
        

        # 노트들이 나오는 순서대로 리스트에 append 후, y_pos를 저장
        if self.note_sequence_list[0] <= self.screen_height:
            self.note_sequence_list[0] += self.note_speed
        if len(self.note_sequence_list) >= 2:
            if len(self.note_sequence_list) >= 3:
                if len(self.note_sequence_list) >= 4:
                    if len(self.note_sequence_list) >= 5:
                        if len(self.note_sequence_list) >= 6:
                            if len(self.note_sequence_list) >= 7:
                                if len(self.note_sequence_list) >= 8:
                                    if self.note_sequence_list[self.m - 7] <= self.screen_height:
                                        self.note_sequence_list[self.m - 7] += self.note_speed
                                if self.note_sequence_list[self.m - 6] <= self.screen_height:
                                    self.note_sequence_list[self.m - 6] += self.note_speed
                            if self.note_sequence_list[self.m - 5] <= self.screen_height:
                                self.note_sequence_list[self.m - 5] += self.note_speed
                        if self.note_sequence_list[self.m - 4] <= self.screen_height:
                            self.note_sequence_list[self.m - 4] += self.note_speed
                    if self.note_sequence_list[self.m - 3] <= self.screen_height:
                        self.note_sequence_list[self.m - 3] += self.note_speed
                if self.note_sequence_list[self.m - 2] <= self.screen_height:
                    self.note_sequence_list[self.m - 2] += self.note_speed
            if self.note_sequence_list[self.m] <= self.screen_height:
                self.note_sequence_list[self.m] += self.note_speed
            if self.note_sequence_list[self.m - 1] <= self.screen_height:
                self.note_sequence_list[self.m - 1] += self.note_speed
            
        # bad score
        if self.h < len(self.note_sequence_list)- 1:
            if self.note_sequence_list[self.h] >= self.screen_height:
                self.bad += 1
                self.score_state = 3
                self.h += 1
                self.score = 0
        
        # print(self.score_state)
        print(self.h)
        # print(self.note_count)
        print(self.note_sequence_list)
        # # print(self.note_y_pos[self.note_count[0]], self.note_y_pos[self.note_count[1]], self.note_y_pos[self.note_count[2]], self.note_y_pos[self.note_count[3]])
        # print(self.note_y_pos)
        # # print(self.bad)
        # print(self.erase)


    def game_over_draw(self):
        if self.over_state == 0:
            self.screen.blit(self.game_over_background1, (0,0))     # no
        if self.over_state == 1:
            self.screen.blit(self.game_over_background2, (0,0))     # yes

    # 범위에 맞게 키를 눌렀는지, 점수 변수들 업데이트
    def Score(self, k):
        if self.note_y_pos[self.h] < self.screen_height:
            if self.key_press[k] == 1:  # 몇번 째 키를 눌렀는지
                if self.note_list[self.h][k] == self.note_state:    # 키값 위치가 노트위치랑 일치하는지
                    # Exerlent
                    if self.Exerlent_range[0] <= self.note_y_pos[self.h] < self.Exerlent_range[1]: # 범위에 맞게
                        self.Exerlent += 1
                        self.note_list[self.h][k] = 0
                        self.score_state = 1
                        self.h += 1
                        self.score += 1
                    # good
                    if self.Exerlent_range[0] - self.approximate <= self.note_y_pos[self.h] < self.Exerlent_range[0]: # 범위에 맞게
                        self.good += 1
                        self.note_list[self.h][k] = 0
                        self.score_state = 2
                        self.h += 1
                        self.score += 1
        print(self.h)
        # print("Exerlent = "+ str(self.Exerlent))
        # print("good = "+ str(self.good))
        # print("bad = "+ str(self.bad))
        # print("erase = "+ str(self.erase))
        # print("m = " + str(m))
        # print(self.note_count)
        # print(self.note_y_pos[self.note_count[0]], self.note_y_pos[self.note_count[1]], self.note_y_pos[self.note_count[2]], self.note_y_pos[self.note_count[3]])
    

    # def bad_score(self, m):
    #     if self.note_y_pos[self.note_count[m]] >= self.screen_height:
    #         self.bad += 1
            # self.score_state = 3
            
    # def score_range(self, m, k):
        # if len(self.note_sequence_list[m]) < 
        # if k == 0:
        #     if self.note_list[self.note_count[m]][k] == self.note_state:
        #         # Exerlent
        #         if self.Exerlent_range[0] <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[1]:
        #             if self.key_press[k] == 1:
        #                 self.Exerlent += 1
        #                 self.note_list[self.note_count[m]][k] = 1
        #                 self.score_state = 1
        #         # good
        #         if self.Exerlent_range[0] - self.approximate <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[0]:
        #             if self.key_press[k] == 1:
        #                 self.good += 1
        #                 self.note_list[self.note_count[m]][k] = 0
        #                 self.score_state = 2
        # if k == 1:
        #      if self.note_list[self.note_count[m]][k] == self.note_state:
        #          # Exerlent
        #         if self.Exerlent_range[0] <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[1]:
        #             if self.key_press[k] == 1:
        #                 self.Exerlent += 1
        #                 self.note_list[self.note_count[m]][k] = 1
        #                 self.score_state = 1
        #         # good
        #         if self.Exerlent_range[0] - self.approximate <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[0]:
        #             if self.key_press[k] == 1:
        #                 self.good += 1
        #                 self.note_list[self.note_count[m]][k] = 0
        #                 self.score_state = 2

        # if k == 2:
        #      if self.note_list[self.note_count[m]][k] == self.note_state:
        #         # Exerlent
        #         if self.Exerlent_range[0] <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[1]:
        #             if self.key_press[k] == 1:
        #                 self.Exerlent += 1
        #                 self.note_list[self.note_count[m]][k] = 1
        #                 self.score_state = 1
        #         # good
        #         if self.Exerlent_range[0] - self.approximate <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[0]:
        #             if self.key_press[k] == 1:
        #                 self.good += 1
        #                 self.note_list[self.note_count[m]][k] = 0
        #                 self.score_state = 2

        # if k == 3:
        #      if self.note_list[self.note_count[m]][k] == self.note_state:
        #          # Exerlent
        #         if self.Exerlent_range[0] <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[1]:
        #             if self.key_press[k] == 1:
        #                 self.Exerlent += 1
        #                 self.note_list[self.note_count[m]][k] = 1
        #                 self.score_state = 1
        #         # good
        #         if self.Exerlent_range[0] - self.approximate <= self.note_y_pos[self.note_count[m]] < self.Exerlent_range[0]:
        #             if self.key_press[k] == 1:
        #                 self.good += 1
        #                 self.note_list[self.note_count[m]][k] = 0
        #                 self.score_state = 2
    # 노트 그리기 함수화
    def auto_draw(self, j):
        if self.note_y_pos[j] <=  self.screen_height:
            if self.note_list[j][0] == self.note_state:
                self.screen.blit(self.side_note, (self.note1_x_pos, self.note_y_pos[j]))
            if self.note_list[j][1] == self.note_state:
                self.screen.blit(self.nomal_note, (self.note2_x_pos, self.note_y_pos[j]))
            if self.note_list[j][2] == self.note_state:
                self.screen.blit(self.nomal_note, (self.note3_x_pos, self.note_y_pos[j]))
            if self.note_list[j][3] == self.note_state:
                self.screen.blit(self.side_note, (self.note4_x_pos, self.note_y_pos[j]))
            self.note_y_pos[j] += self.note_speed
 
    def music_sheet(self, part_beat):
        self.part_beat = part_beat
        print(self.part_beat)
        # 비트 만들기
        while self.a:
            self.beat[0] = self.beat[1] + self.part_beat[0]
            self.beat[1] = self.beat[0] + self.part_beat[1]
            self.beat[0] = round(self.beat[0],1)
            self.beat[1] = round(self.beat[1],1)
            if self.beat[1] < self.part_time[0]: # 0 ~ 15 초 구간
                self.beat_time_list.append(self.beat[0]) # 1초
                self.beat_time_list.append(self.beat[1]) # 0.7초 

            if self.beat[1] >= self.part_time[0]: # 1/8 박자    # 15~ 30초 구간
                self.beat[2] = self.beat[2] + self.part_beat[2]
                if self.part_time[0] <= self.beat[2] <= self.part_time[1]:
                    self.beat_time_list.append(self.beat[2]) # 0.5초 

                if self.beat[2] >= self.part_time[1]:   # 1/4 박자     # 30 ~ 37 초 구간
                    self.beat[3] = self.beat[3] + self.part_beat[0]
                    self.beat[3] = round(self.beat[3],1)
                    if self.part_time[1] < self.beat[3] <= self.part_time[2]:
                        self.beat_time_list.append(self.beat[3]) # 1초

                    if self.beat[3] >= self.part_time[2]:    # 1/8 박자     # 38 ~ 45 초 구간
                        self.beat[4] = self.beat[4] + self.part_beat[2]
                        if self.part_time[2] < self.beat[4] <= self.part_time[3]:
                            self.beat_time_list.append(self.beat[4]) # 0.5초 

                        if self.beat[4] >= self.part_time[3]:    # 1/16 박자        # 45 ~ 60 초 구간
                            self.part_beat[3] = decimal.Decimal(self.part_beat[3])
                            self.beat[5] = round(decimal.Decimal(self.beat[5]),2)
                            self.beat[5] = self.beat[5] + self.part_beat[3]
                            if self.part_time[3] < self.beat[5] <= self.part_time[4]:
                                self.beat_time_list.append(self.beat[5]) # 0.25초 
                            
                            if self.beat[5] >= self.part_time[4]:
                                self.part_beat[3] = decimal.Decimal(self.part_beat[3])
                                self.beat[6] = round(decimal.Decimal(self.beat[6]),2)
                                self.beat[6] = self.beat[6] + self.part_beat[3]
                                if self.part_time[4] < self.beat[6] <= self.part_time[5]:
                                    self.beat_time_list.append(self.beat[6]) # 0.25초 

                                if self.beat[6] >= self.part_time[5]:

                                    # 노트 만들기
                                    if self.i < len(self.beat_time_list) - 1:
                                        n = randrange(0,4)
                                        self.note_grid[n] = self.note_state
                                        self.note_list.append(self.note_grid)
                                        self.note_grid = [0,0,0,0]
                                        self.note_y_pos.append(0)   # y좌표 리스트
                                        self.i += 1
                                    
                                    else:
                                        break