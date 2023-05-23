import arcade
import arcade.gui
import random
import time
# Set how many rows and columns we will have
SPRITE_SCALING = 0.16
SPRITE_SCALING_bot = 0.15

ROW_COUNT = 8
COLUMN_COUNT = 8

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80

# This sets the margin between each cell
# and on the edges of the screen.``65
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN +150
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Example"


class Player(arcade.Sprite):
    """ Player Class """

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        # self.center_x += self.change_x
        # self.center_y += self.change_y

        # # Check for out-of-bounds
        # if self.left < 0:
        #     self.left = 1
        # elif self.right > SCREEN_WIDTH - 5:
        #     self.right = SCREEN_WIDTH - 5

        # if self.bottom < 0:
        #     self.bottom = 1
        # elif self.top > SCREEN_HEIGHT - 5:
        #     self.top = SCREEN_HEIGHT - 5


laser_sound = arcade.load_sound("laser.wav")
impact_sound = arcade.load_sound("impact.wav")

class WelcomeView(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("int.png")
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        ins_view = InstructionView()
        ins_view.on_show_view()
        self.window.show_view(ins_view)

class InstructionView(arcade.View):

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.background = arcade.load_texture("bg.png")
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        quit = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit.with_space_around(bottom=20))

        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.v_box))
        start_button.on_click = self.on_buttonclick1
        quit.on_click = self.on_buttonclick2

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width , 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH , SCREEN_HEIGHT,self.background)
#        arcade.draw_text("Two Player Snail Game", self.window.width / 2, self.window.height / 2,arcade.color.ANDROID_GREEN, font_size=30, anchor_x="center")
        self.uimanager.draw()

    def on_buttonclick1(self, event):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
    def on_buttonclick2(self, event):
        exit()




class GameView(arcade.View):
    row_count = 50
    col_count = 45
    row_count_bot = 645
    col_count_bot = 640
    Draw_list=[]
    list=[]
    move_back=[]
    score=0
    score_bot=0
    mind_list_down=[]
    mind_list_up=[]
    mind_list_left=[]
    mind_list_right=[]
    temp_list=[]
    # row1 = 0
    # col1 = 0
    # row2 = 5
    # col2 = 6
    # score = 0
    # score2 = 0
    # switch = 1
    # restricted_p1 = []
    # restricted_p2 = []

    def __init__(self):
        super().__init__()

        # Create a 2 dimensional array. A two-dimensional
        # array is simply a list of lists.
        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell
        self.player_list = None
        self.player_list_bot = None

        # Set up the player info
        self.player_sprite = None
        self.player_sprite_bot = None
        # self.player_list = None
        # self.player_sprite = None
        # self.splash_p1 = None
        # self.player_splash = None
        arcade.set_background_color(arcade.color.AMAZON)
    

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.player1_list = []
        self.player_list_bot = arcade.SpriteList()
        self.player2_list=[]

        # Set up the player
        self.player_sprite = Player("snail.png", SPRITE_SCALING)
        self.player_sprite.center_x = 45
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.player_sprite2 = Player("snail.png", SPRITE_SCALING)
        self.player_sprite2.center_x = 45
        self.player_sprite2.center_y = 50
        self.player_list.append(self.player_sprite2)
        position = (self.player_sprite2.center_x, self.player_sprite2.center_y)
        self.player1_list.append(position)

        #ddddd
        self.player_sprite_bot = Player("snail2.png", SPRITE_SCALING_bot)
        # self.player_sprite_bot.center_x = (WIDTH // 2) + MARGIN +595
        # self.player_sprite_bot.center_y = (WIDTH // 2) + MARGIN +595
        self.player_sprite_bot.center_x = 640
        self.player_sprite_bot.center_y = 645
        self.player_list_bot.append(self.player_sprite_bot)

        self.player_sprite_bot1 = Player("snail2.png", SPRITE_SCALING_bot)
        # self.player_sprite_bot1.center_x = (WIDTH // 2) + MARGIN +595
        # self.player_sprite_bot1.center_y = (WIDTH // 2) + MARGIN +595
        self.player_sprite_bot1.center_x = 640
        self.player_sprite_bot1.center_y = 645
        self.player_list_bot.append(self.player_sprite_bot1)
        position = (self.player_sprite_bot1.center_x, self.player_sprite_bot1.center_y)
        self.player2_list.append(position)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        # self.player_list.update()
        # self.splash_p1.update()
        self.player_list.update()
        self.player_list_bot.update()

    def Splash(self, center_x, center_y):
        self.player_sprite = Player("snail.png", SPRITE_SCALING)
        self.player_sprite.center_x = center_x
        self.player_sprite.center_y = center_y
        self.player_list.append(self.player_sprite)
        # self.player_splash = Player("splash.png", SPRITE_SCALING)
        # self.player_splash.center_x = center_x
        # self.player_splash.center_y = center_y
        # self.player_list.append(self.player_splash)

    # def Splash2(self, center_x, center_y):
    #     self.player_splash = Player("splash2.png", SPRITE_SCALING)
    #     self.player_splash.center_x = center_x
    #     self.player_splash.center_y = center_y
    #     self.player_list.append(self.player_splash)
    def Splash_bot(self,center_x,center_y):
        self.player_sprite_bot = Player("snail2.png", SPRITE_SCALING_bot)
        self.player_sprite_bot.center_x = center_x
        self.player_sprite_bot.center_y = center_y
        self.player_list_bot.append(self.player_sprite_bot)

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                color=arcade.color.LION

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)


        # Draw all the sprites.

        self.player_sprite.draw()
        self.player_list.draw()
        self.player_list_bot.draw()

        # output = f" User Score: {self.score}"
        # arcade.draw_text(text=output, start_x=10, start_y=30,
        #                  color=arcade.color.RED, font_size=14)
        # output = f" User2 Score: {self.score_bot}"
        # arcade.draw_text(text=output, start_x=540, start_y=620,
        #                  color=arcade.color.RED, font_size=14)


        output = f"Score"
        arcade.draw_text(text=output, start_x=85 * 8 + 15, start_y=85 * 6.5, color=arcade.color.BLACK,
                                 font_size=14)
        output = f"Player's"
        arcade.draw_text(text=output, start_x=85 * 8 + 15, start_y=85 * 5.5, color=arcade.color.BLACK,
                                 font_size=14)
        output = f"Person: {self.score}"
        arcade.draw_text(text=output, start_x=85*8+15, start_y=85*6.2, color=arcade.color.ANDROID_GREEN, font_size=14)
        output = f"Bot: {self.score_bot}"
        arcade.draw_text(text=output, start_x=85 * 8 + 15, start_y=85 * 6, color=arcade.color.BLIZZARD_BLUE,
                                 font_size=14)
        
        if self.score>=32:
            output2 = f"person wins"
            arcade.draw_text(text=output2, start_x=85 * 8 + 15, start_y=85 * 5, color=arcade.color.BLIZZARD_BLUE,
                                 font_size=14)
            if self.score==33:
                exit()
              
        if self.score_bot >=32:
            output2 = " Bot Wins"
            arcade.draw_text(text=output2, start_x=85 * 8 + 15, start_y=85 * 5, color=arcade.color.BLIZZARD_BLUE,
                                 font_size=14)
            if self.score_bot==33:
                exit()
        


    def on_key_press(self, key, modifiers):
        self.temp = (self.player_sprite.center_x, self.player_sprite.center_y)
        # print("player1",self.temp)
        # print('player1',self.player1_list)
        self.temp1 = 0
        self.temp2 = 0
        self.temp3=0
        if key == arcade.key.UP:
            if self.row_count <= 595:
                self.temp2 = self.temp[1]
                self.temp1 = self.temp[0]
                self.temp2 = self.temp2 + 85
                lul = (self.temp1, self.temp2)
                # print("next",lul)
                # self.temp[1]=self.temp1
                if (lul not in self.player1_list) and (lul not in self.player2_list):
                    self.player_sprite.center_y += 85
                    self.player1_list.append(lul)
                    self.row_count = self.player_sprite.center_y 
                    self.score += 1
                    bb=(self.row_count,self.player_sprite.center_y)
                    self.mind_list_up.append(bb)
                else:
                    for i in self.player1_list:
                        if self.temp1 == i[0]:
                            self.list.append(i)
                    # print('up', self.list)
                    for i in self.list:
                        self.move_back.append(i[1])
                    # g1=<len(self.move_back)-2
                    num=len(self.move_back)
                    g2=len(self.move_back)-1
                    while num !=0:
                        for i in self.move_back:
                            new=self.move_back[g2]-i
                            if new == -85:
                                self.temp_list.append(self.move_back[g2])
                                self.temp_list.append(i)
                                g2=self.move_back.index(i)
                        num-=1                     
                        
                        
                    aa = max(self.temp_list)
                    for i in self.list:
                        if aa == i[1]:
                            self.player_sprite.center_y = i[1]
                            self.row_count= self.player_sprite.center_y

                    self.list.clear()
                    self.move_back.clear()
                    self.temp_list.clear()
                self.temp1 = 0
                self.temp2 = 0


        if key == arcade.key.DOWN:
            if self.row_count >= 135:
                self.temp2 = self.temp[1]
                self.temp1 = self.temp[0]
                self.temp2 = self.temp2 - 85
                lul = (self.temp1, self.temp2)
                # print("down", lul)
                if (lul not in self.player1_list) and (lul not in self.player2_list):
                    self.player_sprite.center_y -= 85
                    self.player1_list.append(lul)
                    bb=(self.player_sprite.center_x,self.player_sprite.center_y)
                    self.mind_list_down.append(bb)
                    self.row_count =self.player_sprite.center_y
                    self.score += 1
                    # print("update down",self.mind_list_down)
                else:
                    for i in self.player1_list:
                        if self.temp1 == i[0]:
                            self.list.append(i)
                    # print('down', self.list)
                    # num1=self.list[0]
                    for i in self.list:
                        self.move_back.append(i[1])
                    
                    num=len(self.move_back)
                    g2=len(self.move_back)-1
                    while num !=0:
                        
                        for i in self.move_back:
                            new=self.move_back[g2]-i
                            if new == 85:
                                self.temp_list.append(self.move_back[g2])
                                self.temp_list.append(i)
                                g2=self.move_back.index(i)
                        num-=1                 
                        
                        
                    aa = min(self.temp_list)
                    # print("small list",self.move_back)
                    # aa = min(self.move_back)
                    # print("index",1+self.move_back.index(aa))
                    for i in self.list:
                        if aa == i[1]:
                            self.player_sprite.center_y = i[1]
                            self.row_count=self.player_sprite.center_y
                    self.list.clear()
                    self.move_back.clear()
                    self.temp_list.clear()
                self.temp1 = 0
                self.temp2 = 0

        if key == arcade.key.RIGHT:
            if self.col_count <= 595:
                self.temp2 = self.temp[1]
                self.temp1 = self.temp[0]
                self.temp1 = self.temp1 + 85
                lul = (self.temp1, self.temp2)
                # print("next", lul)
                if (lul not in self.player1_list) and (lul not in self.player2_list):
                    self.player_sprite.center_x += 85
                    self.player1_list.append(lul)
                    bb=(self.col_count,self.player_sprite.center_x)
                    self.mind_list_right.append(bb)
                    self.col_count =self.player_sprite.center_x
                    self.score += 1
                else:
                    for i in self.player1_list:
                        if self.temp2 == i[1]:
                            self.list.append(i)
                    # print('right', self.list)
                    # num1 = self.list[0]
                    for i in self.list:
                        self.move_back.append(i[0])
                    num=len(self.move_back)
                    g2=len(self.move_back)-1
                    while num !=0:
                        for i in self.move_back:
                            new=self.move_back[g2]-i
                            if new == -85:
                                self.temp_list.append(self.move_back[g2])
                                self.temp_list.append(i)
                                g2=self.move_back.index(i)
                        num-=1                         
                        
                        
                    aa = max(self.temp_list)
                    # aa = max(self.move_back)
                    for i in self.list:
                        if aa == i[0]:
                            self.player_sprite.center_x = i[0]
                            self.col_count=self.player_sprite.center_x
                    self.list.clear()
                    self.move_back.clear()
                    self.temp_list.clear()
                
                self.temp1 = 0
                self.temp2 = 0

        if key == arcade.key.LEFT:
            if self.col_count >= 130:
                self.temp2 = self.temp[1]
                self.temp1 = self.temp[0]
                self.temp1 = self.temp1 - 85
                lul = (self.temp1, self.temp2)
                # print("next", lul)
                if (lul not in self.player1_list) and (lul not in self.player2_list):
                    self.player_sprite.center_x -= 85
                    self.player1_list.append(lul)
                    bb=(self.col_count,self.player_sprite.center_x)
                    self.mind_list_left.append(bb)
                    self.col_count =self.player_sprite.center_x
                    self.score += 1
                    # print(self.mind_list_left)
                else:
                    for i in self.player1_list:
                        if self.temp2 == i[1]:
                            self.list.append(i)
                    # print('right', self.list)
                    for i in self.list:
                        self.move_back.append(i[0])
                    num=len(self.move_back)
                    g2=len(self.move_back)-1
                    while num !=0:
                        for i in self.move_back:
                            new=self.move_back[g2]-i
                            if new == 85:
                                self.temp_list.append(self.move_back[g2])
                                self.temp_list.append(i)
                                g2=self.move_back.index(i)
                        num-=1                        
                        
                        
                    aa = min(self.temp_list)
                    # aa = min(self.move_back)
                    
                    for i in self.list:
                        if aa == i[0]:
                            self.player_sprite.center_x = i[0]
                            self.col_count=self.player_sprite.center_x
                    self.list.clear()
                    self.move_back.clear()
                    self.temp_list.clear()
                self.temp1 = 0
                self.temp2 = 0


        self.Splash(self.player_sprite.center_x, self.player_sprite.center_y)
            
        key = random.randint(1, 4)
        self.temp_bot = (self.player_sprite_bot.center_x, self.player_sprite_bot.center_y)
        # print("player2",self.temp_bot)
        # print("player2",self.player2_list)
        self.temp1 = 0
        self.temp2 = 0
        if key == 2:
            if self.row_count_bot <= 595:
                self.temp2 = self.temp_bot[1]
                self.temp1 = self.temp_bot[0]
                self.temp2 = self.temp2 + 85
                lul = (self.temp1, self.temp2)
                # print("next_bot", lul)
                if (lul not in self.player2_list)  and (lul not in self.player1_list):
                    self.player_sprite_bot.center_y += 85
                    self.player2_list.append(lul)
                    self.row_count_bot = self.player_sprite_bot.center_y
                    self.score_bot += 1
                else:
                    # self.player_sprite_bot.center_y=self.player_sprite_bot.center_y
                    for i in self.player2_list:
                        if self.temp1 == i[0]:
                            self.list.append(i)
                    
                    for i in self.list:
                        self.move_back.append(i[1])
                    aa = max(self.move_back)
                    for i in self.list:
                        if aa == i[1]:
                            self.player_sprite_bot.center_y = i[1]
                            self.row_count_bot=self.player_sprite_bot.center_y
                    self.list.clear()
                    self.move_back.clear()
                    self.temp_list.clear()
                self.temp1 = 0
                self.temp2 = 0

        if key == 4:
            if self.row_count_bot >= 135:
                self.temp2 = self.temp_bot[1]
                self.temp1 = self.temp_bot[0]
                self.temp2 = self.temp2 - 85
                lul = (self.temp1, self.temp2)
                # print("next_bot", lul)
                if (lul not in self.player2_list) and (lul not in self.player1_list):
                    self.player_sprite_bot.center_y -= 85
                    self.player2_list.append(lul)

                    self.row_count_bot =self.player_sprite_bot.center_y
                    self.score_bot += 1

                else:
                    # self.player_sprite_bot.center_y=self.player_sprite_bot.center_y
                    for i in self.player2_list:
                        if self.temp1 == i[0]:
                            self.list.append(i)
                  
                    # num1=self.list[0]
                    for i in self.list:
                        self.move_back.append(i[1])
                    aa = min(self.move_back)
                    for i in self.list:
                        if aa == i[1]:
                            self.player_sprite_bot.center_y = i[1]
                            self.row_count_bot=self.player_sprite_bot.center_y
                    self.list.clear()
                    self.move_back.clear()
                self.temp1 = 0
                self.temp2 = 0

        if key == 1:
            if self.col_count_bot <= 595:
                self.temp2 = self.temp_bot[1]
                self.temp1 = self.temp_bot[0]
                self.temp1 = self.temp1 + 85
                lul = (self.temp1, self.temp2)
                # print("next_bot", lul)
                if (lul not in self.player2_list) and (lul not in self.player1_list):
                    self.player_sprite_bot.center_x += 85
                    self.player2_list.append(lul)

                    self.col_count_bot = self.player_sprite_bot.center_x
                    self.score_bot += 1
                else:
                    # self.player_sprite_bot.center_x=self.player_sprite_bot.center_x
                    for i in self.player2_list:
                        if self.temp2 == i[1]:
                            self.list.append(i)
                    
                    # num1 = self.list[0]
                    for i in self.list:
                        self.move_back.append(i[0])
                    aa = max(self.move_back)
                    for i in self.list:
                        if aa == i[0]:
                            self.player_sprite_bot.center_x = i[0]
                            self.col_count_bot=self.player_sprite_bot.center_x 
                    self.list.clear()
                    self.move_back.clear()
                self.temp1 = 0
                self.temp2 = 0

        if key == 3:
            if self.col_count_bot >= 130:
                self.temp2 = self.temp_bot[1]
                self.temp1 = self.temp_bot[0]
                self.temp1 = self.temp1 - 85
                lul = (self.temp1, self.temp2)
                # print("next_bot", lul)
                if (lul not in self.player2_list) and (lul not in self.player1_list):
                    self.player_sprite_bot.center_x -= 85
                    self.player2_list.append(lul)

                    self.col_count_bot =self.player_sprite_bot.center_x
                    self.score_bot += 1
                else:
                    self.player_sprite_bot.center_x=self.player_sprite_bot.center_x
                    for i in self.player2_list:
                        if self.temp2 == i[1]:
                            self.list.append(i)
                    
                    # num1 = self.list[0]
                    for i in self.list:
                        self.move_back.append(i[0])
                    aa = min(self.move_back)
                    for i in self.list:
                        if aa == i[0]:
                            self.player_sprite_bot.center_x = i[0]
                            self.col_count_bot=self.player_sprite_bot.center_x
                    self.list.clear()
                    self.move_back.clear()
                self.temp2 = 0
                self.temp1 = 0

        self.Splash_bot(self.player_sprite_bot.center_x, self.player_sprite_bot.center_y)




    def on_key_release(self, key, modifiers):

        """Called when the user releases a key. """



        # If a player releases a key, zero out the speed.

        # This doesn't work well if multiple keys are pressed.

        # Use 'better move by keyboard' example if you need to

        # handle this.

        if key == arcade.key.UP or key == arcade.key.DOWN:

            self.player_sprite.center_y = self.player_sprite.center_y

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:

            self.player_sprite.center_x = self.player_sprite.center_x

        if key == arcade.key.UP or key == arcade.key.DOWN:

            self.player_sprite_bot.center_y = self.player_sprite_bot.center_y

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:

            self.player_sprite_bot.center_x = self.player_sprite_bot.center_x
        
        

    


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()


main()