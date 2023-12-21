import pygame
import math
from collections import deque
import matplotlib.pyplot as plt

""" dependencies
pip install pygame matplotlib
"""

# 초기화
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 진자 설정
L1, L2 = 200, 200  # 막대의 길이
m1, m2 = 20, 20  # 질량

#TODO: 초기 각도 설정
a1 = math.radians(45)
a2 = math.radians(-90)

# 궤적을 위한 설정
trail_length = 5 * 60  # 5초 동안의 프레임 (60 FPS 가정)
trail1 = deque(maxlen=trail_length)
trail2 = deque(maxlen=trail_length)

# 궤적 데이터 저장을 위한 리스트
positions_x1 = []
positions_y1 = []
positions_x2 = []
positions_y2 = []


# 진자 운동을 계산하는 함수
def calculate_pendulum(a1, a2, a1_v, a2_v, g=9.81):
    num1 = -g * (2 * m1 + m2) * math.sin(a1)
    num2 = -m2 * g * math.sin(a1 - 2 * a2)
    num3 = -2 * math.sin(a1 - a2) * m2
    num4 = a2_v ** 2 * L2 + a1_v ** 2 * L1 * math.cos(a1 - a2)
    den = L1 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
    a1_a = (num1 + num2 + num3 * num4) / den

    num1 = 2 * math.sin(a1 - a2)
    num2 = (a1_v ** 2 * L1 * (m1 + m2))
    num3 = g * (m1 + m2) * math.cos(a1)
    num4 = a2_v ** 2 * L2 * m2 * math.cos(a1 - a2)
    den = L2 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
    a2_a = (num1 * (num2 + num3 + num4)) / den

    return a1_a, a2_a


# 초기 각속도
a1_v, a2_v = 0, 0

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경
    screen.fill((255, 255, 255))

    # 진자 위치 계산
    x1 = L1 * math.sin(a1) + width / 2
    y1 = L1 * math.cos(a1) + height / 4
    x2 = x1 + L2 * math.sin(a2)
    y2 = y1 + L2 * math.cos(a2)

    # 궤적 저장
    trail1.append((x1, y1))
    trail2.append((x2, y2))

    # 궤적 데이터 저장
    positions_x1.append(x1)
    positions_y1.append(y1)
    positions_x2.append(x2)
    positions_y2.append(y2)

    # 궤적 그리기
    for point in trail1:
        pygame.draw.circle(screen, (0, 255, 0), (int(point[0]), int(point[1])), 2)
    for point in trail2:
        pygame.draw.circle(screen, (255, 0, 0), (int(point[0]), int(point[1])), 2)

    # 진자 그리기
    pygame.draw.line(screen, (0, 0, 0), (width / 2, height / 4), (x1, y1), 2)
    pygame.draw.circle(screen, (0, 0, 255), (int(x1), int(y1)), m1)
    pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)
    pygame.draw.circle(screen, (0, 0, 255), (int(x2), int(y2)), m2)

    # 진자 운동 계산
    a1_a, a2_a = calculate_pendulum(a1, a2, a1_v, a2_v)
    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# matplotlib을 사용하여 궤적 그리기
plt.figure(figsize=(10, 6))

# Y축 반전 및 X축 조정
adjusted_x1 = [x - width / 2 for x in positions_x1]
adjusted_y1 = [-y + height / 4 for y in positions_y1]
adjusted_x2 = [x - width / 2 for x in positions_x2]
adjusted_y2 = [-y + height / 4 for y in positions_y2]

plt.plot(adjusted_x1, adjusted_y1, label='Pendulum 1')
plt.plot(adjusted_x2, adjusted_y2, label='Pendulum 2')
plt.title('Double Pendulum Trajectory')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.show()
