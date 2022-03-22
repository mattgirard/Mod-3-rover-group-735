from re import X
from qset_lib import Rover
from time import sleep
import math as m


def Direction_find(htt, dtt):   #This is a function that will scan all the lidar sensors and once there is a lidar sensor without an obstruction, it will set the rover in that directon
    lidar_found=0
    for x in range(lidar/2):    #Checking if the surrounding lidar sensors also see an obstruction; once a lidar sensor without an obstruction is found than the rover will move in that direction
        if distance.lidar[16-x]>=ddt:
            move in direction of lidar[16-x]
            lidar_found= 1  #if a sensor with no obstruction is found than this loop will be exitted and the variable "lidar_found" is set to 1 (True)
            FavoredDirection= 'LEFT'
            break
    
        if distance.lidar[16+x]>=ddt:
            move in direction of lidar[16+x]
            lidar_found= 1
            FavoredDirection= 'RIGHT'
            break

    if lidar_found == 0:
        Rotate rover 90 desrees in FavoredDirection
        Direction_find(htt, dtt)


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

htt= m.atan([Target['x'] - Rover['x']]/[Target['y'] - Rover['y']])
dtt= m.sqrt(float(pow(Target['x'] - Rover['x'], 2) + pow(Target['y'] - Rover['y'], 2)))

lidar= []  #not sure how sensors are labeled, but assuming that they are numbered in order
#going to use the notation of lidar[1], lidar[2], lidar[3], etc for sensors. lidar[1] being most left sensor and lidar[32] being furthest right sensor

Turn rover (hht-rover.heading) #turn the rover to face the target. (hht-rover.heading) is how much the rover needs to turn

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
