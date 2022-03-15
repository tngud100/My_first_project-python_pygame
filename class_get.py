import pygame
import math


class get:
    # 객체 사이즈 받기
    def __init__(self, object):
        self.object = object
        self.object_width = object.get_width()
        self.object_height = object.get_height()
    
    # 객체 개별 pos좌표
    def individual_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.indi_center = self.x_pos, self.y_pos
        return self.x_pos, self.y_pos

    # 객체 중앙기준 좌표 설정 후 그림.
    def blit(self, default_screen, draw_object): #-> individual_pos 사용 후 그림 함수
        draw_object_x = self.indi_center[0]
        draw_object_y = self.indi_center[1]
        draw_object_x = draw_object_x - (self.object_width / 2)
        draw_object_y = draw_object_y - (self.object_height / 2)
        draw_object_pos = (draw_object_x, draw_object_y)
        default_screen.blit(draw_object, draw_object_pos)

    # 스크린 정 중앙 pos좌표
    def center_pos(self, screen_size):
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        self.object_x = (screen_width / 2) - (self.object_width / 2)
        self.object_y = (screen_height / 2) - (self.object_height / 2)
        self.object_center = (self.object_x, self.object_y)

    # 받은 객체 중앙에 그리기
    def blit_center(self, default_screen, draw_object): #-> center_pos 사용 후 그림함수
        draw_object_pos = self.object_center
        default_screen.blit(draw_object, draw_object_pos)

    # 선택 인자에 따른 객체 그리기 -> 메뉴 버튼 선택 효과 * 
    def choice(self, screen, small_object, big_object, list_var):

        self.screen = screen
        self.small_object = small_object
        self.big_object = big_object
        self.list_var = list_var

        if list_var == 0:
            self.blit(self.screen, self.small_object)
        else:
            self.blit(self.screen, self.big_object)

class fade:
    def __init__(self, screen_width, screen_height, screen, blited_screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.blited_screen = blited_screen
        self.win = pygame.Surface((self.screen_width, self.screen_height))

    def fade_out(self, color):
        self.win.fill(color)
        for alpha in range(0,300):
            self.win.set_alpha(alpha)
            self.screen.blit(self.blited_screen, (0,0))
            self.screen.blit(self.win, (0,0))
            pygame.display.update()

    def fade_out_start(self, color, msg):
        self.win.fill(color)
        for alpha in range(0,300):
            self.win.set_alpha(alpha)
            self.screen.blit(self.blited_screen, (0,0))
            self.screen.blit(msg, (0,0))
            self.screen.blit(self.win, (0,0))
            pygame.display.update()

    def fade_in(self):
        self.win.blit(self.blited_screen, (0,0))
        for alpha in range(0, 100):
            self.win.set_alpha(alpha)
            self.win.blit(self.blited_screen, (0,0))
            self.screen.blit(self.win, (0, 0))
            pygame.display.update()
        


class gun_n_bullet:
    def __init__(self, screen, mousepoint, gun, character, character_pos, bullet_shot):
        # 총알 발사 여부
        self.bullet_shot = bullet_shot
        # 마우스 포인트
        self.mouse_point  = mousepoint
        # 스크린 정보 받기
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_center = ((self.screen_width / 2), (self.screen_height / 2))

        # 캐릭터 정보 받기
        self.character = character
        self.character_width = self.character.get_width()
        self.character_height = self.character.get_height()
        self.character_pos = character_pos        # 캐릭터 중앙 pos
        self.character_x = self.character_pos[0]
        self.character_y = self.character_pos[1]

        # 총알 rect와 시작 위치
        self.gun = gun
        self.gun_start_pos = self.character_pos
        self.gun_rect = gun.get_rect()
        self.gun_width = gun.get_width()
        self.gun_height = gun.get_height()

        # 원의 반지름
        self.circle_radius = self.character_width / 2

    # 총 틀 그리기
    def gun_frame_circle(self, border, color):
        self.border = border
        self.color = color
        self.circle_pos = (self.screen_center[0] - self.character_x), (self.screen_center[1] - self.character_y)
        pygame.draw.circle(self.screen, self.color, self.circle_pos, self.circle_radius, border)

    # 총 위치 그리기 로직                       
    def gun_shoot(self):
        self.mouse_point = pygame.mouse.get_pos()
        self.m_x = (self.screen_center[0] - self.mouse_point[0]) - self.character_x
        self.m_y = (self.screen_center[1] - self.mouse_point[1]) - self.character_y

        self.m_x1= self.m_x **2 
        self.m_y1 = self.m_y **2

        if self.m_x == 0:
            self.x = 0
            self.y = self.m_y
            if self.y > 0:
                self.blit_x = self.screen_center[0] 
                self.blit_y = self.screen_center[1] - self.circle_radius
            else:
                self.blit_x = self.screen_center[0] 
                self.blit_y = self.screen_center[1] + self.circle_radius
        else:
            n = math.atan(self.m_y / self.m_x)
            self.x = math.cos(n)
            self.y = math.sin(n)

        self.circle_to_center = self.m_x1 + self.m_y1
        
        self.th = (self.circle_radius)**2 / self.circle_to_center
        
        if self.circle_to_center > self.circle_radius**2:
            if self.m_x > 0:
                self.blit_x = self.screen_center[0] - (self.circle_radius * self.x) 
                self.blit_y = self.screen_center[1] - (self.circle_radius * self.y)
            elif self.m_x < 0:
                self.blit_x = self.screen_center[0] + (self.circle_radius * self.x) 
                self.blit_y = self.screen_center[1] + (self.circle_radius * self.y) 
        else:
            self.blit_x = self.mouse_point[0] + self.character_x
            self.blit_y = self.mouse_point[1] + self.character_y


    
    # 총 그리기 ---> gun_shoot함수 사용 후 그리기
    def gun_draw(self, screen, gun):
        self.screen = screen

        self.mouse_point_blit = (self.blit_x - self.gun_width / 2 - self.character_x), (self.blit_y - self.gun_height / 2 - self.character_y)

        self.screen.blit(gun, self.mouse_point_blit)

    # 총알 그리기
    def bullet_draw(self, bullet_x, bullet_y, bullet_color):
        self.bullet_color = bullet_color
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        # # 각도 * 총알 스피드
        # self.bullet_x -= self.bullet_to_x * b.x
        # self.bullet_y -= self.bullet_to_y * b.y

        if self.bullet_shot == False:
            self.bullet_x = self.blit_x - self.character_x
            self.bullet_y = self.blit_y - self.character_y
            pygame.draw.circle(self.screen, self.bullet_color,(self.bullet_x, self.bullet_y),5)
        if self.bullet_shot == True:
            self.bullet_x = self.screen_center[0] - self.character_pos[0] - self.bullet_x
            self.bullet_y = self.screen_center[1] - self.character_pos[1] - self.bullet_y
            pygame.draw.circle(self.screen, self.bullet_color,(self.bullet_x, self.bullet_y),5)

class character:
    # 캐릭터 정보 가져오기
    def __init__(self, character):
        self.character = character
        self.character_width = self.character.get_width()
        self.character_height = self.character.get_height()
        
    # 캐릭터 중앙 좌표, 스크린 중앙 좌표
    def center_pos(self, screen_width, screen_height, to_x, to_y):
        self.to_x = to_x
        self.to_y = to_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_x_center = self.screen_width / 2
        self.screen_y_center = self.screen_height / 2
        self.screen_center = self.screen_x_center, self.screen_y_center

        self.character_x = self.character_width / 2 + self.to_x
        self.character_y = self.character_height / 2 + self.to_y
        self.character_center = self.character_x, self.character_y
    
        self.screen_center_blit_pos = (self.screen_x_center - self.character_x), (self.screen_y_center  - self.character_y)# 스크린 중앙에 캐릭터 중앙 배치 좌표

    # 스크린의 pos좌표에 캐릭터 그리기
    def character_blit(self, screen, character, pos):
        self.screen = screen
        self.charater = character
        self.pos = pos
        self.screen.blit(self.character, self.pos)
    
        

            
class var:
    # 스크린, 게임상태, 클릭위치 가져오기
    def __init__(self, screen, screen_width, screen_height, state, click_pos):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = state
        self.click_pos = click_pos
        