import time

#Define PID as dictionary of x, y , and f)
def PID(x, y, f):
    global kprop_x, kint_x, kder_x, kprop_y, kint_y, kder_y, previousRun_xerror, previousRun_yerror, xMemoryForP, yMemoryForP, xMemoryForI, yMemoryForI, xMemoryForD, yMemoryForD, flag, setpoint, sampletime
# Define PID gain values as global variables to prevent them from resetting to zero each time function is called
#Needs PID gain values for roll and pitch indivudally which are the rotations of the vehicle along the x and yaxis respectivley

    #Current gain values are arbitrary
    kprop_x = 80
    kint_x = 0.002
    kder_x = 89
    kprop_y = kprop_x
    kint_y= kint_x
    kder_y = kder_x

    flag = 0
#For sample time we can start with 0 but it mat be benefical to vary this during and as a result of testing
    sampletime = 0 
    setpoint = 0
#Need to find error of pitch roll and yaw
    xerror = float(x)*(180/3.141592653) - setpoint
    yerror = float(y)*(180/3.141592653) - setpoint

    currenttime = time.time()

# following variables are reset during the first loop of the controller only

    if flag == 0:
        previousRun_Time = 0
        previousRun_xerror = 0
        previousRun_yerror = 0

        xMemoryForP = 0
        yMemoryForP = 0
   
        xMemoryForI = 0
        yMemoryForI = 0

        xMemoryForD = 0
        yMemoryForD = 0
# Adds a value and the variable and assigns the result to that variable
        flag += 1
#-----------------------------------------------------------------------------------------------
#dt, dy(t) must be defined to be able to be used in the D term of the PID controller 

    dtime = currenttime - previousRunTime
    dxerror = xerror - previousRun_xerror
    dyerror = yerror - previousRun_yerror

#"Heart of PID alg". the alg will be more accurately if it is sampled at regular intervals. Sample time can be changed to optimize controller
    if (dtime >= sampletime):
    #Following is proportional term 

        xMemoryForP = kprop_x * xerror
        yMemoryForP = kprop_y * yerror

    #Integral term
        xMemoryForI += xerror * dtime
        yMemoryForI += yerror * dtime
    
    #yawMemoryForI += yawerror * dtime

        if(xMemoryForI > 400): xMemoryForI = 400
        if(xMemoryForI < -400): xMemoryForI = -400
        if(yMemoryForI > 400): yMemoryForI = 400
        if(yMemoryForI < -400): yMemoryForI = -400

    #Derivative term

    xMemoryForD = dxerror/dtime
    yMemoryForD = dyerror/dtime
    
#Out of if statememnt store variables from most recent run into the previous variables to utilise in the next iterations of the loop
    previousRunTime = currenttime
    previousRun_xerror = xerror
    previousRun_yerror = yerror

#Outputs based on collective PID equation for pitch roll and yaw
#output = Kp*e(t) + Ki*integral(e(t)) + Kd*derivative(e(t))

output_x = xMemoryForP + xMemoryForI * kint_x + kder_x * xMemoryForD
output_y = yMemoryForP + yMemoryForI * kint_y + kder_y * yMemoryForD

