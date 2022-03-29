from re import X
from qset_lib import Rover
from time import sleep
import math as m


def Direction_find(htt, dtt):   #This is a function that will scan all the lidar sensors and once there is a lidar sensor without an obstruction, it will set the rover in that directon
    lidar_found=0
    for x in range(lidar/2):    #Checking if the surrounding lidar sensors also see an obstruction; once a lidar sensor without an obstruction is found than the rover will move in that direction
        if lidar[16-x]>=dtt:
            move_to_lidar(-x)
            lidar_found= 1  #if a sensor with no obstruction is found than this loop will be exitted and the variable "lidar_found" is set to 1 (True)
            FavoredDirection= 'LEFT'
            break
    
        if lidar[16+x]>=dtt:
            move_to_lidar(x)
            lidar_found= 1
            FavoredDirection= 'RIGHT'
            break

    if lidar_found == 0:
        if FavoredDirection == 'RIGHT': 
            heading90= rover.heading + 90
            if heading90 > 360: heading90-= 360
        
        if FavoredDirection == 'LEFT': 
            heading90= rover.heading - 90
            if heading90 < 0: heading90+= 360

        while (rover.heading != heading90):
            if FavoredDirection == 'RIGHT':
                left_wheel_speed= 1
                right_wheel_speed= 0

            if FavoredDirection == 'LEFT':
                left_wheel_speed= 0
                right_wheel_speed= 1

            sleep(0.5)


        Direction_find(htt, dtt)


def move_to_lidar(x): #a function that moves the rover in the direction of a given lidar sensor
    new_heading= rover.heading + (90/32)*x #calculates a new heading that the rover is hoping to achieve based off of variable "x", which is the displacement of lidar sensors from the rovers heading
    if new_heading < 0: #if the new heading is a negative number, than it needs to be "looped" around back to 360 degrees.
        new_heading= 360+new_heading

    while rover.heading != new_heading: #turning the rover to face the direction of the desired lidar sensor 
        if new_heading>rover.heading:
            left_side_speed= 1
            right_side_speed= 0
    
        if new_heading<rover.heading:
            left_side_speed= 0
            right_side_speed= 1
        sleep(0.2)
   
    left_side_speed = 1 #moves rover forwards
    right_side_speed = 1
    sleep(0.5)

def face_target(htt, roverHeading):
    left, right= roverHeading
    for i in range(360): #checking to see which direction has the shortest turn radius
        left-= 1
        right+= 1
        if left == 0: left= 360
        if right == 360: right = 0
        if left == htt: direction = left
        if right == htt: direction = right
    
    while (roverHeading != htt):
        if direction == right:
            left_wheel_speed= 1
            right_wheel_speed= 0

        if direction == left:
            left_wheel_speed= 0
            right_wheel_speed= 1


def main ():
    Target= {
        'x': float('X'),
        'y': float('Y')
    }

    Rover= {
        'x': float('rover.x'),
        'y': float('rover.y')
    }

    FavoredDirection= 'RIGHT'
    GOAL= False

    htt= m.atan([Target['x'] - Rover['x']]/[Target['y'] - Rover['y']]) #heading to target
    dtt= m.sqrt(float(pow(Target['x'] - Rover['x'], 2) + pow(Target['y'] - Rover['y'], 2))) #distance to target

    lidar= []  #not sure how sensors are labeled, but assuming that they are numbered in order
    #going to use the notation of lidar[1], lidar[2], lidar[3], etc for sensors. lidar[1] being most left sensor and lidar[32] being furthest right sensor

    face_target(htt, rover.heading) #turn the rover to face the target.

    while GOAL is False:
        if lidar[16] < dtt:   #if the lidar sensor tells us that something is inbetween the rover and the target
            Direction_find(htt, dtt)
        elif GOAL is True:
            exit

    sleep(1)


#the following is the example code for referance

def main():
    rover = Rover()

    i = 0

    left_side_speed = 1
    right_side_speed = 1

    while i < 1000:
        print("X: " + rover.x + " Y: " + rover.y + " Heading: " + rover.heading)
        for dist in rover.laser_distances:
            if dist < 0.1:
                print("TOO CLOSE")
        rover.send_command(left_side_speed, right_side_speed)
        i = i + 1
        sleep(0.01)


if __name__ == "__main__":
    main()
