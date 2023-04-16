''' This code is meant to test the valves of the Agrobot to ensure that the correct valve is turned on based on the string received from Imagerec
    This utilizes the python package "PYFIRMATA()" to communicate with the arduino and uses values of 0 (OFF) or 1 (ON) to represent the valves
    
    Author: Rajalakshmi Narasimhan (rajalakshmi.nr6@gmail.com)
'''

#importing the required packages

import pyfirmata
import numpy as np
import time # used to write the delay() statement in arduino
import random # not used but just in case we need it to test random valves

#Similar to the main body for arduino 
if __name__ == '__main__':

    '''INFO FOR SYNTAX 
        It treates the Arduino board as an object called BOARD and has functions that can be used with it.
        INTILIAZING PINS: object_at_pin = board.digital[PIN_NUMBER]
        WRITING TO A PIN: object_at_pin.write(ON/OFF)
    '''

    # Initiating communication with Arduino
    board = pyfirmata.Arduino('COM3') #the port arduino is connected to the laptop
    print("Communication Successfully started") 

    #defining constant values
    spraytime = 1 #the time for which the sprayer should spray
    ON = 1
    OFF = 0
    no_of_valves = 9

    #defining some lists/arrays that we use
    pin_nos = [3,4,5,6,7,8,9,10,11] # information about the pins that are connected
    valve_array = [] #will link the valve number to the pin that it corresponds to          Ex: [VALVE1,VALVE2....] and VALVE1 is set to pin 3 

    #setting up pin info for all the valves
    for i in range(no_of_valves):
        valve_name = 'VALVE'+str(i+1)
        valve_name = board.digital[pin_nos[i]]
        valve_array.append(valve_name)

    ''' FUNCTION: Reset()
        PARAMETERS: none
        OBJECTIVE: to set the intial state - state where all the valves are off
        RETURNS: none 
    '''
    def reset():
        for valve in valve_array:
            valve.write(OFF)

    ''' FUNCTION: all_valves()
        PARAMETERS: spraytime - Time for which it sprays
        OBJECTIVE: To spray all the valves in sequence, without receiving an string
        RETURNS: none 
    '''
    def all_valves(spraytime):
        print("The valve spray test has started")
        valve_string = "000000000"
        for index in range(len(valve_string)):
            print("Now testing valve",index+1)
            valve_array[index].write(ON)
            time.sleep(spraytime)       # IN ARDUINO: delay(time)
            valve_array[index].write(OFF)
            time.sleep(delaytime)

    ''' FUNCTION: turn_on_valve()
        PARAMETERS: string_received - It is a string of 0/1 which indicates which valve should be turned on
                    spraytime - Time for which it sprays
                    delaytime - Time for which it turns off before spraying again
        OBJECTIVE: To spray the correct valve for a fixed time
        RETURNS: none 
    '''
    def turn_on_valve(string_received, spraytime):
        print("The valve test has started")
        for index in range(len(string_received)):
            valve_status = string_received[index]
            if valve_status == 1:
                valve_array[index].write(ON)
        time.sleep(spraytime)       # IN ARDUINO: delay(time)

        for index in range(len(string_received)):
            valve_status = string_received[index]
            if valve_status == 1:
                valve_array[index].write(OFF)
        time.sleep(spraytime)

    ''' FUNCTION: pulse_valve():
        PARAMETERS: string_received - It is an string of 0/1 which indicates which valve should be turned on
                    intial_spraytime - The start time for which the valve sprays
                    min_spraytime - The minimum spray time
                    percentReduction - The percentage by which thespray time decreases every iteration
                    no_of_pulses - no of pulses for each spray time 
        OBJECTIVE: Pulses specified valve on and off for a given number of times and then reduces the spray time by given percentage
    '''
    def pulse_valve(string_received, intial_spraytime=3, min_spraytime=1, percentReduction=25, no_of_pulses=3): #with arbitary default values
        print("Pulse valves test has started")
        spraytime = intial_spraytime
        while spraytime >= min_spraytime:
            for j in range(no_of_pulses):
                turn_on_valve(string_received,spraytime)
        spraytime -= spraytime*(percentReduction/100)

    ''' Adapted from Gus' code
        FUNCTION: maxvalvestest():
        PARAMETERS: spraytime - The start time for which the valve sprays
        OBJECTIVE: Turns increasing number of valves on and then off
    '''
    def maxvalvestest(valve_array, spraytime):
        print("Max valves test has started")
        range_of_valve = []
        for v in range(len(valve_array)): 
            range_of_valve.append(v)
            turn_on_valve(range_of_valve)


    #This is essentially the loop in arduino, where the functions are execute.

    while True: 
        reset()
        str_received = "01100000"   #the string of 0/1 we receive to know which valve to turn on



        #all_valves(spraytime)
        #turn_on_valve(str_received,spraytime)    

        pulse_valve(str_received)
        # maxvalvestest(valve_array)

        reset()