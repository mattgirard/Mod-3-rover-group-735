import time

#Define PID as dictionary of roll, pitch, yaw, and f)
def PID(x, y, yaw, f):

# Define PID gain values as global variables to prevent them from resetting to zero each time function is called
#Needs PID gain values for pitch roll and yaw indivudally which are the rotations of the vehicle along the x,y,z axis respectivley
#Consider if it is possible to only utlisze pitch and roll since yaw seems redundant as it is the z axis movement

kprop_y = 3 
kint_y=3 
kder_y = 3
kprop_x = 3
kint_x =3
kder_x = 3
#kprop_yaw =0.1
#kint_yaw = 0
#kder_yaw = 0
flag = 0
#Other variables below
#For sample time we can start with 0 but it mat be benefical to vary this during and as a result of testing
sampletime = 0 
setpoint = 0
#Need to find error of pitch roll and yaw
yerror = float(pitch)*(180/pi) - setpoint
xerror = float(roll)*(180/pi) - setpoint
#yawerror = float(yaw)*(180/pi) - setpoint

#Not sure why currTime is time.time() yet 
currenttime = time.time()

#----------------------------------------------------------------------------------------
#These following variables are reset during the first loop of the controller only

if flag == 0:
    previousRunTime = 0
    previousRunyerror = 0
    previousRunxerror = 0
#previousRunyawerror = 0

    yMemoryForP = 0
    xMemoryForP = 0
#yawMemoryForP = 0

    yMemoryForI = 0
    xMemoryForI = 0
#yawMemoryForI = 0

    yMemoryForD = 0
    xMemoryForD = 0
#yawMemoryForD = 0

# Adds a value and the variable and assigns the result to that variable
    flag += 1
#-----------------------------------------------------------------------------------------------
#dt, dy(t) must be defined to be able to be used in the D term of the PID controller 

dtime = currenttime - previousRunTime
dyerror = yerror - previousRunyerror
dxerror = xerror - previousRunxerror
#dyawerror = yawerror - previousRunyawerror

#"Heart of PID alg". the alg will be more accurately if it is sampled at regular intervals. Sample time can be changed to optimize controller
if (dtime >= sampletime):
    #Following is proportional term 
    yMemoryForP = kprop_y * yerror
    xMemoryForP = kprop_x * xerror
    #yawMemoryForP =   #Still not sure if Yaw is needed but can be easily added if necessary

    #Integral term
    yMemoryForI += yerror * dtime
    xMemoryForI += xerror * dtime
    #yawMemoryForI += yawerror * dtime

    if(yMemoryForI > 400): yMemoryForI = 400
    if(yMemoryForI < -400): yMemoryForI = -400
    if(xMemoryForI > 400): xMemoryForI = 400
    if(xMemoryForI < -400): xMemoryForI = -400
    #if(yawMemoryForI > 400): yawMemoryForI = 400
    #if(yawMemoryForI < -400): yawMemoryForI = -400

    #Derivative term
    yMemoryForD = dyerror/dtime
    xMemoryForD = dxerror/dtime
    #yawMemoryForD = dyawerror/dtime

#Out of if statememnt store variables from most recent run into the previous variables to utilise in the next iterations of the loop
previousRunTime = currenttime
previousRunxerror = xerror
previousRunyerror = yerror
#previousRunyawerror = yawerror

#Outputs based on collective PID equation for pitch roll and yaw

#output = Kp*e(t) + Ki*integral(e(t)) + Kd*derivative(e(t))

output_x = xMemoryForP + xMemoryForI * kint_x + kder_x * xMemoryForD

output_y = yMemoryForP + yMemoryForI * kint_y + kder_y * yMemoryForD