import random, math, turtle
import matplotlib.pyplot as pyplot
import turtle

def angle(x, y):
    ''' This function find the current angle of the particle with respect to the origin
        Parameter:
                  x: coordinate of x
                  y: coordinate of y
        Return:
                The angle of the particle
    '''
    if x == 0:                  # avoid dividing by zero
        x = 0.001
    angle = math.degrees(math.atan(y / x))
    if angle < 0:
        if y < 0:
            angle = angle + 360 # quadrant IV
        else:
            angle = angle + 180 # quadrant II
    elif y < 0:
        angle = angle + 180     # quadrant III
    return angle

def setupWalls(tortoise, openingDegrees, scale, radius):
    ''' This function draws the partial crcle, which is the boundary of the particle
        Parameter:
                   tortoise: name of tutle
                   opneningDegrees: the degree of the angle that particle can escape
                   scale: length of the turtle's step 
                   radius: radius of the cirlce
        Return:
                   None
                   
    '''
    screen = tortoise.getscreen()
    screen.mode("logo")             # east is 0 degrees
    screen.tracer(5)                # speed up drawing

    tortoise.up()                   # draw boundary with
    tortoise.width(0.015 * scale)   # shaded background
    tortoise.goto(radius * scale, 0)
    tortoise.down()
    tortoise.pencolor("lightyellow")
    tortoise.fillcolor("lightyellow")
    tortoise.begin_fill()
    tortoise.circle(radius * scale)
    tortoise.end_fill()
    tortoise.pencolor("black")
    tortoise.circle(radius * scale, 360 - openingDegrees)
    tortoise.up()
    tortoise.home()

    tortoise.pencolor("blue")       # particle is a blue circle
    tortoise.fillcolor("blue")
    tortoise.shape("circle")
    tortoise.shapesize(0.75, 0.75)

    tortoise.width(1)               # set up for walk
    tortoise.pencolor("green")
    tortoise.speed(0)
    tortoise.down() # comment this out to hide trail

def escape(openingDegrees, tortoise, draw):
    '''This function creates a simulation of random walks and draw the turtle
       Parameters:
                   openingDegrees: the degree of the angle that particle can escape
                   tortoise: name of the turtle
                   draw: a flag variable that draws turtle
        Return:
                number of steps

    '''
    # opening is between 360 - openingDegrees and 360
    x = 0                                       # initialize (x, y) = (0, 0)
    y = 0
    radius = 1                                  # moving in unit radius circle
    
    stepLength = math.pi / 128                  # std dev of each step

    if draw:
        scale = 300                             # scale up drawing
        setupWalls(tortoise, openingDegrees, scale, radius)

    steps = 0                                   # number of steps so far
    escaped = False                             # has particle escaped yet?

    while not escaped:                          # Test when the turtle is within the boundaries
        steps += 1
        prevX = x # set the previous position of the particle at x axis
        prevY = y # set the previous position of the particle 
        x = x + random.gauss(0, stepLength) # create a random walk simulation on x axis 
        y = y + random.gauss(0, stepLength) # create a random walk simulation on y axis
        if draw:
            tortoise.goto(x*scale,y*scale)
        radius = math.sqrt(x*x + y*y) # set up radius for the circle
        if radius > 1: # determine whether the particle has escaped the circle yet
            currentAngle = angle(x,y)
            if currentAngle > (360 - openingDegrees):
                escaped = True # this is when the particle has escaped and the loop ends
            else: # this is when the particle hits the wall
                x = prevX
                y = prevY
                steps += 1
                if draw:
                    tortoise.goto(x*scale,y*scale)

        if draw:
            if escaped:                         # make particle escape
                x = x + 10 * (x - prevX)        # in current direction
                y = y + 10 * (y - prevY)
                tortoise.color("red")
            tortoise.goto(x * scale, y * scale) # move particle

    if draw:
        screen = tortoise.getscreen()           # update screen to compensate
        screen.update()                         # for high tracer value
    return steps

def escapeMonteCarlo(openingDegrees, trials):
    ''' This function find the average distances from given trials
        Parameters:
                    openingDegrees: the angle degree for the open in the circle
                    trials: number of random walks in each simulation
        Return:
                    Average distances
    '''
    totalSteps = 0
    for trial in range(trials):
        draw=True
        if not draw: 
            steps=escape(openingDegrees, None, draw)
        else:
            tortoise=turtle.Turtle()# visualize the random walk by using turtle if draw is True
            steps = escape(openingDegrees, tortoise, draw)
        totalSteps = totalSteps + steps
    return totalSteps / trials

def plotEscapeStepsOriginal(minOpening, maxOpening, openingStep, trials):
    ''' This function plots the average distances traveled by random walks
        Parameter:
                   minOpening: the minimum opening steps for the plot
                   maxOpening: the maximum opening steps for the plot
                   openingSteps: the range of each steps
                   trials: the number of random walks in each simulation
        Return:
                   None
    '''
    stepsList = [] # create three empty lists called "stepsList", "timeList", and "theoryList"
    timeList = []
    theoryList = []
    stepRange = range(minOpening, maxOpening + 1, openingStep) # create the range between each iteration
    for step in stepRange:
        avgSteps = escapeMonteCarlo(step, trials)
        stepsList.append(avgSteps) # append the stepsList list with the average number of steps
        timeList.append(step) # append the timeList list with the number of iterations
        radian = step*math.pi/180 # convert from degree to radian
        theoryList.append(0.5-2*math.log(math.sin(radian/4))) # append the theoryList with the function that adjusts the step size

    pyplot.plot(timeList, stepsList, label = "Simulation")
    pyplot.plot(timeList, theoryList, label = "Theoretical")
    pyplot.legend(loc = "center right")
    pyplot.xlabel("Opening angle")
    pyplot.ylabel("Time to escape")
    pyplot.show() # plot the graph


def plotEscapeSteps(minOpening, maxOpening, openingStep, trials):
    ''' This function is the corrected version of the above function, with the value (pi/180)^2
        Parameter:
                   minOpening: the minimum opening steps for the plot
                   maxOpening: the maximum opening steps for the plot
                   openingSteps: the range of each steps
                   trials: the number of random walks in each simulation
        Return:
                   None
    '''
    stepsList = []  # create three empty lists called "stepsList", "timeList", and "theoryList"
    timeList = []
    theoryList = []
    stepRange = range(minOpening, maxOpening + 1, openingStep)  # create the range between each iteration
    for step in stepRange:
        avgSteps = escapeMonteCarlo(step, trials)
        avgSteps = avgSteps * (math.pi/ 128)**2 # multiply the result with sqaure of stepLength to make the function more "correct"
        stepsList.append(avgSteps) # append the stepsList list with the average number of steps
        timeList.append(step)   # append the timeList list with the number of iterations
        radian = step*math.pi/180 # convert from degree to radian
        theoryList.append(0.5-2*math.log(math.sin(radian/4))) # append the theoryList with the function that adjusts the step size

    pyplot.plot(timeList, stepsList, label = "Simulation")
    pyplot.plot(timeList, theoryList, label = "Theoretical")
    pyplot.legend(loc = "center right")
    pyplot.xlabel("Opening angle")
    pyplot.ylabel("Time to escape")
    pyplot.show() # plot the graph

def main():
    plotEscapeStepsOriginal(10,180,50,100) # easy but wrong scale
    plotEscapeSteps(10,180,50,100) # easy and on correct scale
    plotEscapeSteps(10,180,10,1000) # full solution (will take several minutes to run)

main()
