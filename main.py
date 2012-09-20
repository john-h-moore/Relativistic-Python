__author__ = "John H Moore"
__date__ = "19 September 2012"

import math
import sys
import ship
import terra

#All these are initialized to -1
a = -1				#acceleration
ev = -1				#exhaust velocity of the engines
mr = -1				#mass ratio (ratio of propellant mass:everything else)
pTime = -1			#proper time (time from spaceship's frame of reference)
tTime = -1			#terra time (time from Terra's frame of reference)
d = -1				#distance (in light years)
v = -1				#velocity
gamma = -1			#time dilation factor gamma

#Speed of light in m/s
def cAbs():
    return 299792458.0

#1 year in seconds
def secs():
    return 31556926.0

#1 light year in meters
def LY():
    return 9.46 * math.pow(10, 15)

#Have we gotten all the user input?
def checkDone():
    choice = ""
    answer = None
    print("Do you have more information to enter?")
    choice = raw_input("[Y] or [N]: ")
    if (choice == "Y") or (choice == "y"):
        answer = True
    elif (choice == "N") or (choice == "n"):
        print("\n")
        answer = False
    else:
        print("You have entered an invalid choice")
    return answer

#What's the ship's acceleration?
def getAccel():
    a = float(raw_input("Enter the acceleration in m/s^2\n(1 g = 9.81 m/s^2): "))
    return a

#What's the ship's mass ratio?
def getMR():
    mr = float(raw_input("Enter the mass ratio (dimensionless number): "))
    return mr

#What's the ship's exhaust velocity in m/s?
def getEV():
    ev = float(raw_input("Enter the exhaust velocity in m/s: "))
    return ev

#What's the proper time? (i.e. the time that passes in the ship's frame of reference)
#Input is in years
def getPTime():
    pTime = float(raw_input("Enter the proper time in years: "))
    return pTime

#What's the Terra time?  (i.e. the time that passes on Terra)
#Input is in years
def getTTime():
    tTime = float(raw_input("Enter Terra time in years: "))
    return tTime

#What's the distance to the destination (in light years)?
def getDist():
    d = float(raw_input("Enter the distance in lightyears: "))
    return d

#Convert years to seconds
def seconds(t):
    return float(t*secs())

#Convert seconds to years
def years(t):
    return float(t/secs())

#Convert light years to meters
def meters(d):
    return float(d*LY())

#Convert meters to light years
def lightyears(d):
    return float(d/LY())

#Calculate the ship's velocity as a percentage of the speed of light
def psl(v, C):
    return float(v/C)

#User menu for entering ship data
#isDone var used to see if the user has any more data to enter
def shipMenu():
    choice = -1
    isDone = False
    global a
    global ev
    global mr
    global pTime
    print("\n** SHIP MENU **")
    while isDone == False:
        print("What information do you have about the ship?")
        print("[1] Acceleration")
        print("[2] Mass Ratio")
        print("[3] Exhaust Velocity")
        print("[4] Proper Time (ship's frame of reference")
        choice = int(raw_input("Enter your selection: "))
        if choice == 1:
            a = getAccel()
        elif choice == 2:
            mr = getMR()
        elif choice == 3:
            ev = getEV()
        elif choice == 4:
            pTime = getPTime()
        else:
            print ("You have entered an invalid choice")
        isDone = not(checkDone())


#User menu for entering Terra data
#isDone var used to see if the user has any more data to enter
def terraMenu():
    choice = -1
    isDone = False
    global tTime
    global d

    print("** TERRA MENU **")
    while isDone != True:
        print("What information do you have about Terra?")
        print("[1] Distance")
        print("[2] Terra Time")
        print("[3] No Data")
        choice = int(raw_input("Enter your selection: "))
        if choice == 1:
            d = getDist()
        elif choice == 2:
            tTime = getTTime()
        elif choice == 3:
            break
        else:
            print ("You have entered an invalid choice")
        isDone = not(checkDone())

#Gathers information from the user via shipMenu() and terraMenu()
#Performs all calculations
def calculate():
    shipMenu()
    terraMenu()
    global a
    global ev
    global mr
    global pTime
    global tTime
    global gamma
    global d
    global v
    
    C = cAbs()
    
	#If acceleration is less than 0, we can't do anything
    while (a <= 0):
        print("Error!  Acceleration must be positive")
        a = accel()

	#Print solutions based on user data
	#Calculations only performed if initial value == -1
	#Otherwise the user provided the value for that variable
    print("** SOLUTIONS **")

	#Calculate Terra Time in years
	#tt1, tt2, and tt3 calculations all performed
	#if any of these is greater than 0, it is the correct answer
    if(tTime == -1):
        tt1 = terra.tObj1(a, seconds(pTime), C)
        tt2 = -1
        tt3 = -1
        if (mr > 0) and (ev > 0):
            tt2 = terra.tObj2(ev, mr, a, C)
        if (d > 0):
            tt3 = terra.tObj3(a, meters(d), C)

        if tt1 > 0:
            tTime = years(tt1)
        elif tt2 > 0:
            tTime = years(tt2)
        elif tt3 > 0:
            tTime = years(tt3)
        else:
            print("Error!  You have not input enough data")
            sys.exit(1)

	#Calculate pTime - only requires tTime
    print "tTime: ", round(tTime, 2)

    if (pTime == -1):
        pTime = years(ship.pTime1(a, seconds(tTime), C))

    print "pTime: ", round(pTime, 2)

	#Calculate distance in light years (if not provided)
    if (d == -1):
        d = lightyears(terra.tDist1(a, seconds(pTime), C))
	
    print "d: ", round(d, 2)

	#Calculate velocity as a percentage of the speed of light
	#This number is never provided
    v = psl(terra.tVFin1(a, seconds(pTime), C), C)

    print "v: ", round(v, 2)

	#Calculate time dilation factor gamma
	#This number is never provided
    gamma = ship.gamma1(a, seconds(pTime), C)

    print "gamma: ", round(gamma, 2)

if __name__ == "__main__":
    calculate()
