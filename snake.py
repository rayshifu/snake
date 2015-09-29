# -*- coding: cp936 -*-
from Tkinter import *

UP, LEFT, DOWN, RIGHT = (1, 2, 3, 4)
DEAD, PAUSE, RUNNING, EATED = (-1, 0, 1, 2)

class MyList():
    def __init__(self, length):
        self.length = length
        
class Snake():
    def __init__(self):
        self.world_width = 40
        self.world_height = 40
        self.snake_body = [[3,20],[2,20],[1,20]]
        self.snake_status = PAUSE
        self.snake_speed = 1
        self.snake_expand_step = 3
        self.snake_food_position = [20,20];
        self.snake_direction = RIGHT

    def sk_expand(self):
        len_snake_body = len(self.snake_body)
        for i in range(0,self.snake_expand_step):
            self.snake_body.append(self.snake_body[len_snake_body - 1])

    def sk_getstatus(self):
        return self.snake_status

    def sk_getfood(self):
        return self.snake_food_position

    def sk_run(self):
        self.snake_status = RUNNING
    
    def sk_pause(self):
        self.snake_status = PAUSE

    def sk_step(self):
        if self.snake_status == EATED:
            self.snake_status = RUNNING

        if self.snake_status == RUNNING:
            x, y = self.snake_body[0]
            if self.snake_direction == UP:
                tmp = [[x,y-1]]
            elif self.snake_direction == LEFT:
                tmp = [[x-1,y]]
            elif self.snake_direction == DOWN:
                tmp = [[x,y+1]]
            else:
                tmp = [[x+1,y]]
            self.snake_body = tmp + self.snake_body[0:len(self.snake_body)-1]
            
            if (x<0)or(x>=self.world_width):
                self.snake_status = DEAD
            elif (y<0)or(y>=self.world_height):
                self.snake_status = DEAD

            if self.snake_body[0] in self.snake_body[1:len(self.snake_body)]:
                self.snake_status = DEAD
        
            if self.snake_body[0] == self.snake_food_position:
                self.sk_expand()
                self.sk_newfood()
                self.snake_status = EATED

        return self.snake_body
        
    def sk_newfood(self):
        import random
        x = random.randint(0,self.world_width - 1);
        y = random.randint(0,self.world_height - 1);
        self.snake_food_position = [x,y]
        
    def sk_turn_up(self, event):
        if (self.snake_direction != DOWN)and(self.snake_direction != UP):
            self.snake_direction = UP
    
    def sk_turn_down(self, event):
        if (self.snake_direction != DOWN)and(self.snake_direction != UP):
            self.snake_direction = DOWN
        
    def sk_turn_left(self, event):
        if (self.snake_direction != RIGHT)and(self.snake_direction != LEFT):
            self.snake_direction = LEFT
        
    def sk_turn_right(self, event):
        if (self.snake_direction != RIGHT)and(self.snake_direction != LEFT):
            self.snake_direction = RIGHT

class Game():
    def __init__(self):
        self.wnd = Tk()
        self.wnd.geometry("240x260")
        self.snake = Snake()

        # 240 - 40*5 = 20
        self.topbase = 20
        self.leftbase = 20
        self.power = 5

        self.privstep = []
        self.snake_want_paint = []
        self.privfood = self.snake.sk_getfood()

        self.bgcolor = 'white'
        self.snake_color = 'black'
        self.food_color = 'red'
        
        Label(self.wnd,text = 'PythonCE Snake').pack()
      
        self.gamerectangle = Canvas(self.wnd,bg = 'white',width=234,height=234)
        self.gamerectangle.create_rectangle(10, 10, 230, 230, outline = 'black')
        self.gamerectangle.pack()

        self.wnd.bind('w', self.snake.sk_turn_up)
        self.wnd.bind('a', self.snake.sk_turn_left)
        self.wnd.bind('s', self.snake.sk_turn_down)
        self.wnd.bind('d', self.snake.sk_turn_right)

    def drawsnake(self, parm2, color):
        for i in range(len(parm2)):
            x, y = parm2[i]
            px = x * self.power + self.leftbase
            py = y * self.power + self.topbase
            qx = px + self.power
            qy = py + self.power
            self.gamerectangle.create_rectangle(px, py, qx, qy, fill = color, outline = self.bgcolor)
        
    def drawfood(self, parm2, color):
        x, y = parm2
        px = x * self.power + self.leftbase
        py = y * self.power + self.topbase
        qx = px + self.power
        qy = py + self.power
        self.gamerectangle.create_rectangle(px, py, qx, qy, fill = color, outline = self.bgcolor)

    def gameflush(self):
        pass
    
    def playsnake(self, master):
        if (self.snake.sk_getstatus() != DEAD)and(self.snake.sk_getstatus() != PAUSE):
            if self.snake.sk_getstatus() == EATED:
                self.drawfood(self.privfood, self.bgcolor)
                self.drawfood(self.snake.sk_getfood(), self.food_color)
                self.privfood = self.snake.sk_getfood()

            self.privstep = self.snake_want_paint
            self.drawsnake(self.snake_want_paint, self.bgcolor)
            self.snake_want_paint = self.snake.sk_step()
            self.drawsnake(self.snake_want_paint, self.snake_color)

        self.gameflush()
            
        self.wnd.after(90,self.playsnake,master)

    def launch(self):
        self.drawfood(self.snake.sk_getfood(), self.food_color)
        self.snake.sk_run()
        self.wnd.after(100,self.playsnake,self.wnd)
        self.wnd.mainloop()
        
game = Game()
game.launch()

