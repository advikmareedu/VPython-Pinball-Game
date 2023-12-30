from vpython import *
#Web VPython 3.2
#Use the 'z' and 'x' keys to move the paddles to hit the pinball up, 
#try to hit the bumpers to increase your score, 
#do not let the pinball hit the ground
#you have 3 lives
scene.bind('keydown', keydown_fun)     # Function for key presses
import random
starting_position = vec(0,-1,0)
leftwall =  box(size=vec(1,1,18),
            pos= vec(0,-1,0)+vec(-4,1,0),
            color = color.green
            )
rightwall = box(size=vec(1,1,18),
            pos= vec(0,-1,0)+vec(4,1,0),
            color = color.red
            )
topwall = box(size=vec(8,1,1),
            pos= vec(0,-1,0)+vec(0,1,-9),
            color = color.white
            )
bottomwall = box(size=vec(8,1,1),
            pos= vec(0,-1,0)+vec(0,1,9),
            color = color.black
            )
               

ground = box(size = 1.0*vec(8, 1, 18),
            pos = starting_position,
            color = vec(0.5,0.5,0)
            )

scoreBumper = sphere(size = vec(1,1,1),
            pos = starting_position + vec(2,1,-3),
            color= color.white          
            )
pyr = pyramid (size = vec(1,1,1),
            pos = starting_position + vec(-2,1,-1),
            axis = vec(0,1,0),
            color= color.blue
            )
cyl = cylinder (size = vec(1,1,1),
            pos = starting_position + vec(1,1,2),
            axis = vec(0,1,0),
            color= color.yellow
            )

counter = box(size = vec(1,1,1),
                pos = vec(0,-3,0),
                axis = vec(0,0,0),
                coloer = color.white,
                opacity = 0
                )
def makeball(starting_position,starting_vel,starting_acc):
    """ makeball makes a ball appear on the screen
        Argument: starting_position is a vector that puts the pinball in its location,
                    starting_vel is a vector that represents the initial velocity of the ball,
                    starting_acc is a vector that represents the pinball's initial acceleration
    """
    pinball = sphere(size = vec(0.5,0.5,0.5),
                pos = starting_position+vec(2,0,0),
                accel = vec(0,0,0.1),
                color= color.red
                )
               
    pinball.vel=starting_vel
     
    return pinball
               
L = label( pos=vec(0,0.25,-10), text='Score: ' + counter.axis.z )
ball = makeball(vec(0,0,0),vec(0,0,0))

leftholder = box(size=vec(4,1,1),
                    pos=vec(-3,0,5),
                    axis = vec(1,0,1)
                    )
                    
rightholder = box(size=vec(4,1,1),
                    pos=vec(3,0,5),
                    axis = vec(-1,0,1)
                    )
rightarmpos=vec(1.5,0,6.5)
l=1.25
h=0.5
w=0.5
rightarm = cylinder(pos=vector(rightarmpos),
                  axis=vector(-0.5,0,1),
         length=l, height=h, width=w,
         turn=vec(0,0,0))

arr = arrow(pos=vec(rightarmpos),
            axis = vec(0,1,0),
            shaftwidth = 0.1)
   
leftarmpos  = vec(-1.5,0,6.5)  
leftarm = cylinder(pos=vector(leftarmpos),
                  axis=vector(0.5,0,1),
         length=l, height=h, width=w,
         turn=vec(0,0,0))

arr = arrow(pos=vec(leftarmpos),
            axis = vec(0,1,0),
            shaftwidth = 0.1)
 # Avoids changing the view automatically

scene.width = 640                      # Make the 3D canvas larger
scene.height = 480
scene.background = vec(1,1,1)
RATE = 100                # The number of times the while loop runs each second
dt = 1.0/(1.0*RATE)      # The time step each time through the while loop
  # Avoids changing the view automatically
scene.forward = vec(0, -14, -14)  # Ask for a bird's-eye view of the scene...


# This is the "event loop" or "animation loop"
# Each pass through the loop will animate one step in time, dt
#
while True:
   
    rate(RATE)
   
   
    leftholdercollision()
    rightholdercollision()
    ball.pos = ball.pos + ball.vel*dt
    wall_collisions(ball)
    bumpercollisions(pyr)
    bumpercollisions(cyl)
    bumpercollisions(scoreBumper)
    leftarm.axis += leftarm.turn
    rightarm.axis += rightarm.turn
    leftarm.length = l
    rightarm.length = l
    leftreset(leftarm)
    rightreset(rightarm)
    armcollision()
    
    ball.vel.z +=0.1
    

#ball wall collision function
def wall_collisions(ball):
    """wall_collisions makes the ball bounce off the wall and increase the counter
        when this happens
       Argument: ball is a sphere, Ball must have a .vel field and a .pos field.
    """
    if ball.pos.z < topwall.pos.z:           # Hit--check for z
        ball.pos.z = topwall.pos.z           # Bring back into bounds
        ball.vel.z *= -1.0                 # Reverse the z velocity
        counter.axis.z +=1
        L.text = 'Score: ' + counter.axis.z

    # If the ball hits wallB
    if ball.pos.x < leftwall.pos.x:           # Hit--check for x
        ball.pos.x = leftwall.pos.x           # Bring back into bounds
        ball.vel.x *= -1.0                 # Reverse the x velocity
   
    if ball.pos.x > rightwall.pos.x:           # Hit--check for x
        ball.pos.x = rightwall.pos.x           # Bring back into bounds
        ball.vel.x *= -1.0
    
    if ball.pos.z > bottomwall.pos.z:           # Hit--check for z
        ball.pos.z = bottomwall.pos.z           # Bring back into bounds
        ball.vel.z *= 0
        X = random.choice(list(range(-4,4)))
        ball.pos = vec(X,0,0)
        counter.axis.x +=1
        if counter.axis.x > 3:
            gameover = label( pos=vec(0,0.25,0), text='GAME OVER :(')
            ball.pos=vec(0,0,19)
   
    

        
def keydown_fun(event):
    """This function is called each time a key is pressed."""
    # ball.color = randcolor()  # This turns out to be very distracting!
    key = event.key
    

    amount = 0.42               # "Strength" of the keypress's velocity changes
    if key == 'up' or key in 'wWiI':
        ball.vel = ball.vel + vec(0, 0, -amount)
    elif key == 'left' or key in 'aAjJ':
        ball.vel = ball.vel + vec(-amount, 0, 0)
    elif key == 'down' or key in 'sSkK':
        ball.vel = ball.vel + vec(0, 0, amount)
    elif key == 'right' or key in "dDlL":
        ball.vel = ball.vel + vec(amount, 0, 0)
    elif key in ' rR':
        ball.vel = vec(0, 0, 0) # Reset! via R or the spacebar, " "
        ball.pos = vec(0, 0, 0)
    elif key == 'x':
        rightarm.turn = vec(-0.1,0,-0.1)
    elif key == 'z':
        leftarm.turn = vec(0.1,0,-0.1)

        
def bumpercollisions(bumper):
    """bumpercollisions increases the score each time a bumper is hit and
        makes the ball bounce off the bumpers
        Argument: bumper is a shape
    """
    d=0.5
    if abs(ball.pos.z - bumper.pos.z)<=d:
        if abs(ball.pos.x - bumper.pos.x)<=d:
            ball.vel.z *= -1.0
            counter.axis.z +=1
            L.text = 'Score: ' + counter.axis.z
    if abs(ball.pos.x - bumper.pos.x)<=d:
        if abs(ball.pos.z - bumper.pos.z)<=d:
            ball.vel.x *= -1.0
            counter.axis.z +=1
            L.text = 'Score: ' + counter.axis.z
def leftholdercollision():
        """leftholdercollision makes the ball bounce off the left gray wall
        """
        Z = ball.pos.z
        X = ball.pos.x
        xvel= (ball.vel.x)
        zvel= (ball.vel.z)
        if X<-1:
            if abs(Z -X -6 - sqrt(2))<0.25:
                ball.vel.x = zvel
                ball.vel.z = -xvel

def rightholdercollision():
        """rightholdercollision makes the ball bounce off the right gray wall
        """
        Z = ball.pos.z
        X = ball.pos.x
        xvel= (ball.vel.x)
        zvel= (ball.vel.z)
        if X>1:
            if abs(Z -(-X +6 + sqrt(2)))<0.25:             
                ball.vel.x = zvel
                ball.vel.z = -xvel
                
            
def leftreset(object):
    """leftreset brings the left paddle back to its original position
        Argument: object is the left paddle
    """
    if object.axis.z <= 0:
        object.turn = -object.turn
    
    if object.axis.x <0:
        object.turn = vec(0,0,0)
        
def rightreset(object):
    """rightreset brings the right paddle back to its original position
        Argument: object is the right paddle
    """
    if object.axis.z <= 0:
        object.turn = -object.turn
    
    if object.axis.x >0:
        object.turn = vec(0,0,0)
        
def armcollision():
    """armcollision makes the ball travel in a direction after hit by the paddle
    """
    zl= leftarm.axis.z
    xl = leftarm.axis.x
    lpx = leftarm.pos.x
    lpz = leftarm.pos.z
    if ball.pos.x<lpx+xl:
        if ball.pos.z>lpz+zl:
            ball.vel.z = ball.vel.z*-1
    
    zr = rightarm.axis.z
    xr = rightarm.axis.x
    rpx = rightarm.pos.x
    rpz = rightarm.pos.z
    if ball.pos.x>rpx+xr:
        if ball.pos.z>rpz+zr:
            ball.vel.z *= -1


        

        
        
    

            
    
    