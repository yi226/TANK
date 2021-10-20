# 坦克大战
import pygame
import time
import random

from pygame.sprite import Sprite

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)  # RGB
TEXT_COLOR = pygame.Color(255, 255, 255)
INIT_BLOOD = 4


# 定义精灵类基类
class BaseItem(Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)


class MainGame():
    window = None
    my_tank = None
    i = 0
    # 敌方坦克列表
    enemyTankList = []
    enemyTankCount = 5
    # 我方子弹列表
    mybulletlist = []
    # 敌方子弹列表
    enemybulletlist = []
    # 爆炸效果
    explodelist = []
    # 墙壁
    walllist = []

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置标题
        pygame.display.set_caption('坦克大战')
        # 初始化我方坦克
        MainGame.my_tank = Tank(350, 300)
        # 初始化敌方坦克
        self.createnemy()
        # 初始化墙壁
        self.creatwall()
        while True:
            # 减慢循环速度
            time.sleep(0.02)
            # 设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            self.getEvent()
            # 绘制文字
            MainGame.window.blit(self.getTextSuface('enemy:%d' % len(MainGame.enemyTankList)), (10, 10))
            MainGame.window.blit(self.getTextSuface('blood:%d' % MainGame.my_tank.live), (600, 450))
            # 调用坦克显示
            if MainGame.my_tank.live != 0:
                MainGame.my_tank.displayTank()
            else:
                self.defeat()
            # 显示敌方坦克
            self.blitEnemyTank()
            # 显示我方坦克子弹
            self.blitmybullet()
            # 显示敌方坦克子弹
            self.blitenemybullet()
            # 展示爆炸效果
            self.blitexplode()
            # 显示墙壁
            self.blitwall()
            # 调用坦克移动方法
            if not MainGame.my_tank.stop:
                MainGame.my_tank.move()
                MainGame.my_tank.hitwall()
                MainGame.my_tank.myhitenemy()
            if len(MainGame.enemyTankList) == 0 and MainGame.my_tank.live > 0:
                self.win()
            pygame.display.update()
        pass

    # 结束游戏
    def endGame(self):
        print('谢谢使用')
        exit()
        pass

    # 游戏失败
    def defeat(self):
        MainGame.enemyTankList.clear()
        MainGame.mybulletlist.clear()
        MainGame.enemybulletlist.clear()
        MainGame.walllist.clear()
        image = pygame.image.load('img/defeat.bmp')
        rect = image.get_rect()
        rect.left = 200
        rect.top = 150
        MainGame.window.blit(image, rect)

    # 游戏胜利
    def win(self):
        MainGame.walllist.clear()
        MainGame.mybulletlist.clear()
        MainGame.enemybulletlist.clear()
        image = pygame.image.load('img/win.png')
        rect = image.get_rect()
        rect.left = 100
        rect.top = 150
        MainGame.window.blit(image, rect)

    # 初始化敌方坦克
    def createnemy(self):
        top = 100
        # 循环生成
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    # 显示敌方坦克
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randmove()
                enemyTank.hitwall()
                enemyTank.enemyhitmy()
                if MainGame.i == 30:
                    enemybullet = Bullet(enemyTank, 'ENEMY')
                    MainGame.enemybulletlist.append(enemybullet)
                    MainGame.i = 0
                else:
                    MainGame.i += 1
            else:
                MainGame.enemyTankList.remove(enemyTank)

    # 初始化墙壁
    def creatwall(self):
        for i in range(4):
            wall = Wall(i * 210, 220)
            MainGame.walllist.append(wall)

    # 显示墙壁
    def blitwall(self):
        for wall in MainGame.walllist:
            wall.displayWall()

    # 显示我方子弹
    def blitmybullet(self):
        for mybullet in MainGame.mybulletlist:
            if mybullet.live:
                mybullet.displayBullet()
                mybullet.move()
                mybullet.hit()
                mybullet.hitwall()
            else:
                MainGame.mybulletlist.remove(mybullet)

    # 显示敌方坦克子弹
    def blitenemybullet(self):
        for enemybullet in MainGame.enemybulletlist:
            if enemybullet.live:
                enemybullet.displayBullet()
                enemybullet.move()
                enemybullet.hitmy()
                enemybullet.hitwall()
            else:
                MainGame.enemybulletlist.remove(enemybullet)

    # 展示爆炸效果
    def blitexplode(self):
        for explodement in MainGame.explodelist:
            if explodement.live:
                explodement.displayExplode()
            else:
                MainGame.explodelist.remove(explodement)

    # 获取事件
    def getEvent(self):
        eventlist = pygame.event.get()
        # 遍历事件
        for event in eventlist:
            # 判断按下的键
            # 若按退出关闭窗口
            if event.type == pygame.QUIT:
                self.endGame()
            # 键盘按下
            if event.type == pygame.KEYDOWN:
                if MainGame.my_tank.live == 0 or len(MainGame.enemyTankList) == 0:
                    if event.key == pygame.K_ESCAPE:
                        self.startGame()
                else:
                    # 判断上下左右
                    if event.key == pygame.K_LEFT:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        # print('左')
                    elif event.key == pygame.K_RIGHT:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        # print('右')
                    elif event.key == pygame.K_UP:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        # print('上')
                    elif event.key == pygame.K_DOWN:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        # print('下')
                    elif event.key == pygame.K_SPACE:
                        # 创建子弹
                        if len(MainGame.mybulletlist) < 3:
                            mybullet = Bullet(MainGame.my_tank, 'MY')
                            MainGame.mybulletlist.append(mybullet)
            # 松开按键
            if event.type == pygame.KEYUP:
                # 判断释放的键是上下左右
                if event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN or \
                        event.key == pygame.K_LEFT or \
                        event.key == pygame.K_RIGHT:
                    MainGame.my_tank.stop = True

    # 左上角文字绘制
    def getTextSuface(self, text):
        # 初始化字体
        pygame.font.init()
        # 获取字体对象
        font = pygame.font.SysFont('consolar', 24)
        # 绘制文字信息
        textsurface = font.render(text, True, TEXT_COLOR)
        return textsurface


class Tank(BaseItem):
    # 位置
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {
            'U': pygame.image.load('img/TANKU.png'),
            'D': pygame.image.load('img/TANKD.png'),
            'L': pygame.image.load('img/TANKL.png'),
            'R': pygame.image.load('img/TANKR.png'),
        }
        # 方向
        self.direction = 'U'
        # 根据当前图片方向获取图片
        self.image = self.images[self.direction]
        # 获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left top
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = 5
        # 坦克移动开关
        self.stop = True
        self.live = INIT_BLOOD
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        pass

    # 移动
    def move(self):
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        # 判断坦克方向
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed
        pass

    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    # 碰墙
    def hitwall(self):
        for wall in MainGame.walllist:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
        pass

    # 显示
    def displayTank(self):
        # 获取展示对象
        self.image = self.images[self.direction]
        # 调用blit方法
        MainGame.window.blit(self.image, self.rect)
        pass

    # 我方碰敌方
    def myhitenemy(self):
        for enemy in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemy):
                self.stay()


# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 加载图片集
        self.images = {
            'U': pygame.image.load('img/enemyU.png'),
            'D': pygame.image.load('img/enemyD.png'),
            'R': pygame.image.load('img/enemyR.png'),
            'L': pygame.image.load('img/enemyL.png'),
        }
        # 随机生成方向
        self.direction = self.randDirection()
        # 获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step = 40
        self.live = True
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        pass

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
        pass

    def randmove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 40
        else:
            self.move()
            self.step -= 1

    def enemyhitmy(self):
        if pygame.sprite.collide_rect(self, MainGame.my_tank):
            self.stay()


# 子弹
class Bullet(BaseItem):
    def __init__(self, tank, bullettype):
        if bullettype == 'MY':
            self.image = pygame.image.load('img/bullet.png')
        elif bullettype == 'ENEMY':
            self.image = pygame.image.load('img/bullet0.png')
        self.rect = self.image.get_rect()
        # 坦克方向决定子弹方向
        self.direction = tank.direction
        # 子弹位置
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top - self.rect.width / 2 + tank.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top - self.rect.width / 2 + tank.rect.width / 2
        # 速度
        self.speed = 6
        # 子弹状态
        self.live = True
        pass

    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
        pass

    # 展示
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)
        pass

    # 子弹与敌方坦克碰撞
    def hit(self):
        for enemytank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemytank, self):
                enemytank.live = False
                self.live = False
                # 爆炸
                explode = Explode(enemytank)
                MainGame.explodelist.append(explode)

    # 子弹与己方坦克
    def hitmy(self):
        if pygame.sprite.collide_rect(MainGame.my_tank, self):
            MainGame.my_tank.live -= 1
            self.live = False
            # 爆炸
            explode = Explode(MainGame.my_tank)
            MainGame.explodelist.append(explode)

    # 子弹碰撞墙壁
    def hitwall(self):
        for wall in MainGame.walllist:
            if pygame.sprite.collide_rect(self, wall):
                self.live = False


# 墙壁
class Wall(BaseItem):
    def __init__(self, left, top):
        self.image = pygame.image.load('img/WALL.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        pass

    # 展示墙壁
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)
        pass


# 爆炸效果
class Explode():
    def __init__(self, tank):
        # 位置由坦克位置决定
        self.rect = tank.rect
        self.images = [
            pygame.image.load('img/explode0.jpg'),
            pygame.image.load('img/explode1.jpg'),
            pygame.image.load('img/explode2.jpg'),
            pygame.image.load('img/explode3.jpg'),
            pygame.image.load('img/explode.png')
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True
        pass

    # 展示爆炸
    def displayExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0
        pass


if __name__ == '__main__':
    MainGame().startGame()
