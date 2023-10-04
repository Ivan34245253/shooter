from pygame import *
from random import randint
mixer.init()
font.init()



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):            
            keys_pressed = key.get_pressed()
            if keys_pressed[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys_pressed[K_RIGHT] and self.rect.x < 595:
                self.rect.x += self.speed
    def fire(self):
            bullet = Bullet('bullet.png', 4, player1.rect.centerx-10, player1.rect.top, 15, 20)    
            bullets.add(bullet) 
            fire.play()           

                      

    
class Enemy(GameSprite):    
    def update(self):
        if self.rect.y < 500:
            self.rect.y += self.speed
        else: 
            self.rect.y = 0
            self.rect.x = randint(50,450)
            global miss 
            miss += 1
            
class Bullet(GameSprite):    
    def update(self):
        self.rect.y -= self.speed
        

       
     

            

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg') 

clock = time.Clock()
window = display.set_mode((700, 500)) 
display.set_caption('Лабиринт')
background = transform.scale(image.load('galaxy.jpg'),(700,500))                       

miss = 0
score = 0

bullets = sprite.Group()

player1 = Player('rocket.png', 10, 5,400, 80, 100)



font1 = font.Font(None, 24)
font2 = font.Font(None, 42)

textLose = font2.render("О нет, поражение(...", False,(180, 80, 80))     
textWin = font2.render("Ура, победа!", False,(10, 180, 80)) 


enemys = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(1,5), randint(50,450), 0, 80, 50)
    enemys.add(enemy)



game = True
play = True

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player1.fire()
    

    if sprite.spritecollide(player1, enemys, False) or miss >= 3:
        play = False
        window.blit(background,(0,0))
        window.blit(textLose,(210,200))
    elif score >= 10:
        play = False
        window.blit(background,(0,0))
        window.blit(textWin,(250,200))


    if play:
        window.blit(background,(0,0))
        text1 = font1.render(f"Счет: {score}", False,(180, 80, 80))     
        text2 = font1.render(f"Пропущено: {miss}", False,(180, 80, 80))  
        window.blit(text1,(0,0))
        window.blit(text2,(0,20)) 
        enemys.draw(window)
        enemys.update()
        player1.reset()
        player1.move()
        bullets.draw(window)
        bullets.update()

        colliders = sprite.groupcollide(bullets, enemys, True, True)
        for c in colliders:
            score +=1            
            enemy = Enemy('ufo.png', randint(1,5), randint(50,450), 0, 80, 50)
            enemys.add(enemy)
        
    
    

    

    display.update()
    clock.tick(60)  