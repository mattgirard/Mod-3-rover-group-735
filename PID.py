import time

#Define PID as dictionary of roll, pitch, yaw, and f)
def PID(roll, pitch, yaw, f):

# Define PID gain values as global variables to prevent them from resetting to zero each time function is called
#Needs PID gain values for pitch roll and yaw indivudally which are the rotations of the vehicle along the x,y,z axis respectivley
#Consider if it is possible to only utlisze pitch and roll since yaw seems redundant as it is the z axis movement


kprop_pitch = 3 
kint_pitch =3 
kder_pitch = 3
kprop_roll = 3
kint_roll =3
kder_roll = 3
kprop_yaw =3
kint_yaw = 3
kder_yaw = 3
flag = 0
#Other variables below
#For sample time we can start with 0 but it mat be benefical to vary this during and as a result of testing
sampletime = 
setpoint = 0
#Need to find error of pitch roll and yaw
pitcherror = float(pitch)*(180/pi) - setpoint
rollerror = float(roll)*(180/pi) - setpoint
yawerror = float(yaw)*(180/pi) - setpoint

#Not sure why currTime is time.time() yet 
currenttime = time.time()

#----------------------------------------------------------------------------------------
#These following variables are reset during the first loop of the controller only

if flag == 0

previousRunTime = 0
previousRunpitcherror = 0
previousRunrollerror = 0
previousRunyawerror = 0

pitchMemoryForP = 0
rollMemoryForP = 0
yawMemoryForP = 0

pitchMemoryForI = 0
rollMemoryForI = 0
yawMemoryForI = 0

pitchMemoryForD = 0
rollMemoryForD = 0
yawMemoryForD = 0

# Adds a value and the variable and assigns the result to that variable
flag += 1
#-----------------------------------------------------------------------------------------------
#dt, dy(t) must be defined to be able to be used in the D term of the PID controller 

dtime = currenttime - previousRunTime
dpitcherror = pitcherror - previousRunpitcherror
drollerror = rollerror - previousRunrollerror
dyawerror = yawerror - previousRunyawerror

#"Heart of PID alg". the alg will be more accurately if it is sampled at regular intervals. Sample time can be changed to optimize controller
if (dtime >= sampletime):
    #Following is proportional term 
    pitchMemoryForP = kprop_pitch * pitcherror
    rollMemoryForP = kprop_roll * rollerror
    yawMemoryForP =   #Still not sure if Yaw is needed but can be easily added if necessary

    #Integral term
    pitchMemoryForI += pitcherror * dtime
    rollMemoryForI += rollerror * dtime
    yawMemoryForI += yawerror * dtime

    if(pitchMemoryForI > 400): pitchMemoryForI = 400
    if(pitchMemoryForI < -400): pitchMemoryForI = -400
    if(rollMemoryForI > 400): rollMemoryForI = 400
    if(rollMemoryForI < -400): rollMemoryForI = -400
    if(yawMemoryForI > 400): yawMemoryForI = 400
    if(yawMemoryForI < -400): yawMemoryForI = -400

    #Derivative term
    pitchMemoryForD = dpitcherror/dtime
    rollMemoryForD = drollerror/dtime
    yawMemoryForD = dyawerror/dtime

#Out of if statememnt store variables from most recent run into the previous variables to utilise in the next iterations of the loop
previousRunTime = currenttime
previousRunrollerror = rollerror
previousRunpitcherror = pitcherror
previousRunyawerror = yawerror

#Outputs based on collective PID equation for pitch roll and yaw
 
 outputPitch = pitchMemoryForP + kprop_pitch * 
    