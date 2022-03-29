import time

#Define PID as dictionary of x, y , and f)
def PID(x, y, f):
    global kprop_x, kint_x, kder_x, kprop_y, kint_y, kder_y, previousRun_xerror, previousRun_yerror, xMemoryForP, yMemoryForP, xMemoryForI, yMemoryForI, xMemoryForD, yMemoryForD, flag, setpoint, sampletime
    # Define PID gain values as global variables to prevent them from resetting to zero each time function is called
    #Needs PID gain values for roll and pitch indivudally which are the rotations of the vehicle along the x and yaxis respectivley

    #Current gain values are arbitrary, these will most likely be changed 
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
    #Need to find error of x and y movement 
    xerror = float(x)*(180/3.141592653) - setpoint
    yerror = float(y)*(180/3.141592653) - setpoint

    currenttime = time.time()

    # following variables are reset during the first loop of the controller only

    if flag == 0:
        previousRunTime = 0
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

    #Includes actual PID calculations, the alg will be more accurately if it is sampled at regular intervals. Sample time can be changed to optimize controller
    if (dtime >= sampletime):
    #Following is proportional term 

        xMemoryForP = kprop_x * xerror
        yMemoryForP = kprop_y * yerror

    #Integral term
        xMemoryForI += xerror * dtime
        yMemoryForI += yerror * dtime
    


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


    #Calculate PID outputs in x and y directions using PID equation --> Kp*e(t) + Ki*integral(e(t)) + Kd*derivative(e(t))

    output_x = xMemoryForP + xMemoryForI * kint_x + kder_x * xMemoryForD
    output_y = yMemoryForP + yMemoryForI * kint_y + kder_y * yMemoryForD


    #Calculate the ESC pulses (1000us - 2000us PWM signal) for each of the motor.
    #Note that in Gazebo simulation backright in the code = frontright, backleft in the code  = backright, frontleft in the code = backleft, frontright in the code = frontleft	

    move_backright = 1500 + output_x + output_y

    move_backleft = 1500 + output_x - output_y

    move_frontleft = 1500 - output_x - output_y

    move_frontright = 1500 - output_x + output_y
	
    #THe following provides limits for the electronic speed control of the motor in case the PID controller goes out of control
    if(move_backright > 2000): move_backright = 2000
    if(move_backleft > 2000): move_backleft = 2000
    if(move_frontright > 2000): move_frontright = 2000
    if(move_frontleft > 2000): move_frontleft = 2000
    if(move_backright < 1100): move_backright = 1100
    if(move_backleft < 1100): move_backleft = 1100
    if(move_frontright < 1100): move_frontright = 1100
    if(move_frontleft < 1100): move_frontleft = 1100
	
    #Map the electronic speed control values to motor values
    motorvel_backright = ((move_backright - 1500)/25) + 50
    motorvel_backleft = ((move_backleft - 1500)/25) + 50
    motorvel_frontright = ((move_frontright - 1500)/25) + 50
    motorvel_frontleft = ((move_frontleft - 1500)/25) + 50

    f.data = [motorvel_frontright, -motorvel_frontleft, motorvel_backleft, -motorvel_backright]

    return f, xerror, yerror

