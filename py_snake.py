#PYTHON SNAKE GAME
#practice simple game development and learn new techniques
#NEW TECHNIQUE -> TURTLE
"""IMPORT PACKAGES/MODULES"""
import time, random, turtle 
#NOTES ON TURTLE:
#turtle is a module/ graphics library that provides a way to create graphics and animations 
#turtle can be used for drawing, animation, event handling etc. You can control the turtle's color, shape etc.
#turtle works by the concept of a turtle moving around a canvas and leaving a trail behind it, similar to a pen.


#CREATE GAME SCREEN
#use turtle to draw initial screen, graphics are displayed on a screen.
#SCREEN CO-ORDS: use Cartesian coordinate system, origin (0,0) located at the center.
#Turtle starts at the center by default, you specify target position using (x,y) co-ords.
screen = turtle.Screen()
screen.title("PY-SNAKE GAME")
screen.setup(width=700, height=700)
screen.tracer(0)
screen.bgcolor("#1d1d1d")#RGB values ->29,29,29 / 1d1d1d close to black
#use turtle to draw the border of the screen
turtle.speed(5)
turtle.pensize(3)
turtle.penup()
turtle.goto(-310,250) #x and y values
turtle.pendown()
turtle.color("red")
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.right(90)
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.penup()
turtle.hideturtle() #makes turtle invisible

#CREATE SCORE
score = 0
delay = 0.1

#CREATE SNAKE
#use turtle to draw the snake
snake = turtle.Turtle()
snake.speed()
snake.shape("square")
snake.color("green")
snake.penup()
snake.goto(0, 0) #center position
snake.direction = "stop" #initialise snake direction


#CREATE SNAKE FOOD/MUNCHIES
#use turtle to draw fruit
fruit = turtle.Turtle()
fruit.speed(0)
fruit.shape("square")
fruit.color("white")
fruit.penup()
fruit.goto(30, 30)

old_fruit = []#keeps track of fruit that has been 'eaten' by snake

#CREATE SCOREBOARD DISPLAY
#use turtle
scoring = turtle.Turtle()
scoring.speed(0)
scoring.color("white")
scoring.penup()
scoring.hideturtle()
scoring.goto(0,300) #position turtle
scoring.write("SCORE: ", align="center", font=("Courier", 24, "bold"))#write text in current position

#DEFINE MOVEMENT
def snake_go_up():
    """if UP key is pressed"""
    #can't go up if currently moving down
    if snake.direction != "down":
        snake.direction = "up"

def snake_go_down():
    """if DOWN key is pressed"""
    #can't go down if currently going up
    if snake.direction != "up":
        snake.direction = "down"

def snake_go_left():
    """if LEFT key is pressed"""
    #can't go left if currently going right
    if snake.direction != "right":
        snake.direction = "left"

def snake_go_right():
    """if RIGHT key is pressed"""
    #can't go right if currently going left
    if snake.direction != "left":
        snake.direction = "right"

def snake_move():
    """function that allows snake movement"""
    #depending on the key press, move the snake
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y + 20)
    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y - 20)
    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x - 20)
    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x + 20)

#KEYBOARD BINDING
screen.listen()#set focus on Turtle screen
#call the corresponding function for each key press
screen.onkeypress(snake_go_up, "Up")
screen.onkeypress(snake_go_down, "Down")
screen.onkeypress(snake_go_left, "Left")
screen.onkeypress(snake_go_right, "Right")

#MAIN GAME LOOP
while True:
    screen.update()

    #snake eats food ie. collision
    if snake.distance(fruit) < 20:
        #assign random x and y values within the screen
        x = random.randint(-290, 270)
        y = random.randint(-240, 240)
        fruit.goto(x, y) #put the fruit at that position
        #increment the score value
        scoring.clear()
        score += 1
        #display the new score
        scoring.write("Score: {}".format(score), align="center", font=("Courier", 24, "bold"))
        delay -= 0.001

        #adding in new length to the snake, use fruit
        new_fruit = turtle.Turtle()
        new_fruit.speed(0)
        new_fruit.shape("square")
        #use same color as the snake
        new_fruit.color("green")
        new_fruit.penup()
        old_fruit.append(new_fruit)#add to list of 'eaten' fruit

    #adding length to snake
    for index in range(len(old_fruit) -1, 0, -1):
        a = old_fruit[index -1].xcor()
        b = old_fruit[index -1].ycor()

        old_fruit[index].goto(a, b)
    if len(old_fruit) > 0:
        a = snake.xcor()
        b = snake.ycor()
        old_fruit[0].goto(a, b)

    snake_move()

    #snake and border collision, stops the game
    #border collision, use x and y co-ord
    if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
        time.sleep(1)
        #display GAME OVER screen
        screen.clear()
        screen.bgcolor("turquoise")
        scoring.goto(0,0)
        scoring.write(" GAME OVER!! \n Your score: {}".format(score), align="center", font=("Courier", 30, "bold"))
    #self collision, snake body is old_fruit/ 'eaten' fruit
    for food in old_fruit:
        if food.distance(snake) < 20:
            time.sleep(1)
            #display GAME OVER screen
            screen.clear()
            screen.bgcolor("turquoise")
            scoring.goto(0,0)
            scoring.write(" GAME OVER!! \n Your score: {}".format(score), align="center", font=("Courier", 30, "bold"))
       
    time.sleep(delay)
    turtle.Terminator()#end game, stop execution of turtle graphics
