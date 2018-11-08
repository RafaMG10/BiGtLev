 # px, py and pz are the position of the levitation point
 # the center of the array is (0, 0, 0)

import math
import serial
import transducer

M_PI = math.pi
lamb = float(8.575e-3)    #// 343 [m/s] / 40,000 [Hz] = 8.575 [mm]
pitch = float(16.5e-3)        # pitch between transducers is 10.5 [mm]



px = 0.0
py = 0.0
pz = 0.003
phases = [0] * 256 

def calcPhases(px,py,pz):

    for j in range(1,16):
        for i in range(1,16):

            addr = i + j * 16
            dx = px - ((i - 7.5) * pitch)
            dy = py - ((j - 7.5) * pitch)
            dz = pz;
            r = math.sqrt(dx * dx + dy * dy + dz * dz) #// distance between the levitation point and one transducer
            theta = -2.0 * M_PI * r / lamb

            re = math.cos(theta)
            im = math.sin(theta)
            phase = math.atan2(im, re)
            if i < 8:
                phase = phase + M_PI                            #// add the signature to create twin trap
        
            phases[addr] = phase
        
    return phases


def discritizePhase(phase, phaseMax = 32):
    TWO_PI = 2 * (M_PI)
    modPhase = math.fmod(phase, TWO_PI)
    if (modPhase < 0):
        modPhase = modPhase + TWO_PI
    normalizedPhase = modPhase / TWO_PI

    discretePhase = int(normalizedPhase * phaseMax)
    return discretePhase

def discretizeMessage(message, phaseMax=32):
    clone_message = []
    for i in message:
        discrit = discritizePhase(i)
        clone_message.append(discrit)

    return clone_message



# matrix_calibration = [ 6, 6, 12, 8, 11, 27, 0, 8, 9, 25, 24, 25, 9, 25, 8, 11, 10, 9, 10, 6, 10, 12, 26, 28, 29, 12, 24, 26, 11, 26, 11, 10, 26, 11, 10, 27, 12, 13, 13, 10, 26, 11, 10, 12, 27, 27, 27, 0, 11, 28, 10, 9, 29, 9, 27, 27, 28, 10, 25, 26, 9, 26, 26, 26, 23, 11, 28, 11, 23, 27, 27, 10, 11, 10, 11, 15, 40, 10, 9, 13, 27, 27, 9, 23, 11, 27, 12, 27, 12, 25, 27, 11, 12, 26, 10, 10, 0, 26, 11, 11, 10, 28, 11, 10, 27, 11, 27, 13, 13, 12, 28, 23, 28, 12, 12, 0, 9, 26, 29, 26, 28, 10, 12, 27, 27, 26, 25, 24, 11, 11, 26, 12, 0, 0, 12, 12, 10, 27, 26, 12, 26, 28, 8, 12, 15, 12, 11, 28, 0, 0, 9, 26, 26, 26, 12, 11, 28, 27, 26, 10, 8, 27, 26, 27, 0, 0, 24, 11, 10, 11, 0, 10, 0, 12, 27, 11, 27, 11, 29, 29, 0, 0, 27, 12, 26, 28, 9, 27, 27, 10, 27, 9, 27, 28, 11, 12, 28, 10, 14, 10, 27, 0, 26, 12, 12, 28, 28, 28, 10, 12, 27, 11, 10, 29, 11, 9, 28, 12, 13, 11, 16, 28, 11, 27, 11, 29, 28, 28, 27, 26, 13, 27, 22, 27, 26, 24, 26, 27, 28, 9, 29, 13, 27, 9, 7, 27, 12, 26, 10, 11, 10, 24, 13, 29, 12, 0]
# matrix_calibration = [ 7, 7, 13, 9, 12, 28, 0, 9, 10, 26, 25, 26, 10, 26, 9, 12, 11, 10, 11, 7, 11, 13, 27, 29, 30, 13, 25, 27, 12, 27, 12, 11, 27, 12, 11, 28, 13, 14, 14, 11, 27, 12, 11, 13, 28, 28, 28, 0, 12, 29, 11, 10, 30, 10, 28, 28, 29, 11, 26, 27, 10, 27, 27, 27, 24, 12, 29, 12, 24, 28, 28, 11, 12, 11, 12, 16, 41, 11, 10, 14, 28, 28, 10, 24, 12, 28, 13, 28, 13, 26, 28, 12, 13, 27, 11, 11, 0, 27, 12, 12, 11, 29, 12, 11, 28, 12, 28, 14, 14, 13, 29, 24, 29, 13, 13, 0, 10, 27, 30, 27, 29, 11, 13, 28, 28, 27, 26, 25, 12, 12, 27, 13, 0, 0, 13, 13, 11, 28, 27, 13, 27, 29, 9, 13, 16, 13, 12, 29, 0, 0, 10, 27, 27, 27, 13, 12, 29, 28, 27, 11, 9, 28, 27, 28, 0, 0, 25, 12, 11, 12, 0, 11, 0, 13, 28, 12, 28, 12, 30, 30, 0, 0, 28, 13, 27, 29, 10, 28, 28, 11, 28, 10, 28, 29, 12, 13, 29, 11, 15, 11, 28, 0, 27, 13, 13, 29, 29, 29, 11, 13, 28, 12, 11, 30, 12, 10, 29, 13, 14, 12, 17, 29, 12, 28, 12, 30, 29, 29, 28, 27, 14, 28, 23, 28, 27, 25, 27, 28, 29, 10, 30, 14, 28, 10, 8, 28, 13, 27, 11, 12, 11, 25, 14, 30, 13, 0]
matrix_calibration = [ 7, 7, 13, 9, 12, 28, 0, 11, 10, 26, 25, 27, 10, 26, 8, 12, 10, 8, 11, 6, 11, 13, 28, 29, 30, 14, 27, 30, 15, 30, 16, 15, 31, 16, 15, 0, 17, 18, 18, 15, 31, 17, 16, 17, 1, 1, 1, 0, 18, 2, 15, 15, 3, 14, 1, 1, 2, 16, 31, 0, 15, 0, 31, 0, 29, 16, 2, 17, 29, 0, 0, 15, 17, 16, 17, 20, 13, 15, 14, 17, 0, 0, 13, 27, 15, 31, 15, 30, 15, 29, 31, 15, 15, 29, 13, 13, 14, 29, 14, 14, 13, 31, 14, 13, 30, 14, 0, 16, 16, 15, 31, 28, 30, 15, 15, 1, 13, 29, 31, 28, 31, 12, 15, 29, 30, 29, 28, 28, 11, 12, 27, 12, 0, 0, 12, 12, 11, 0, 26, 11, 26, 28, 6, 11, 16, 11, 11, 27, 0, 0, 8, 24, 25, 26, 10, 10, 27, 27, 26, 10, 9, 27, 25, 26, 0, 0, 24, 10, 10, 10, 29, 10, 11, 12, 28, 11, 27, 12, 29, 28, 0, 0, 26, 11, 25, 27, 9, 26, 26, 10, 27, 8, 26, 27, 10, 11, 27, 9, 12, 10, 26, 8, 25, 12, 11, 28, 26, 27, 8, 26, 10, 26, 26, 12, 27, 24, 11, 28, 28, 27, 31, 11, 26, 10, 27, 10, 10, 9, 41, 39, 27, 9, 5, 10, 10, 8, 10, 11, 12, 24, 12, 28, 10, 24, 22, 10, 27, 8, 25, 26, 24, 6, 28, 11, 26, 0]
def map_matrix(mat):

    #matrix_1 = [19,20,4,1,17,18,2,3,51,52,36,33,49,50,34,35]
    matrix_1 = mat
    matrix_2 = []
    matrix_3 = []
    matrix_4 = []

    section1_m1 = []
    section2_m1 = []
    section3_m1 = []
    
    section1_m2 = []
    section2_m2 = []
    section3_m2 = []
    
    section1_m3 = []
    section2_m3 = []
    section3_m3 = []

    section1_m4 = []
    section2_m4 = []
    section3_m4 = []

    
    for x in matrix_1:
        matrix_2.append(x + 4)
        section1_m1.append(x + (64) )
        section2_m1.append(x + (64*2))
        section3_m1.append(x + (64*3))
    for x in matrix_2:
        matrix_3.append(x+4)
        section1_m2.append(x + (64) )
        section2_m2.append(x + (64*2))
        section3_m2.append(x + (64*3))
    for x in matrix_3:
        matrix_4.append(x+4)
        section1_m3.append(x + (64) )
        section2_m3.append(x + (64*2))
        section3_m3.append(x + (64*3))
    for x in matrix_4:
        section1_m4.append(x + (64) )
        section2_m4.append(x + (64*2))
        section3_m4.append(x + (64*3))  

    matrix = matrix_1+section1_m1+section2_m1+section3_m1+matrix_2+section1_m2+section2_m2+section3_m2+matrix_3+section1_m3+section2_m3+section3_m3+matrix_4+section1_m4+section2_m4+section3_m4
    num = range(1,257)
    copy_matrix = []

    for i in num:
        index = matrix.index(i)
        copy_matrix.append(index+1)
    
    matrix = copy_matrix 
    return matrix

def boardPosition(location):

    # mm -> meters
    center_board = 16.5*15
    vector_new_position = [center_board , -center_board]

    i = 0
    line = []
    for y in range(16):
        for x in range(16):
            location.append([(-x)+vector_new_position[0], y + vector_new_position[1], 0])
            line.append([(-x)+vector_new_position[0], y + vector_new_position[1], 0])
        print str(line) + 'end'
        line = []
        
    # print location


def sendAmpl(message, val):

    for x in range(1,len(message)-1):
        message[x] = val

def sendPattern(ser,message):
    values = bytearray(message)

    ser.write(values)

if __name__ == '__main__':
    # ser = serial.Serial('/dev/tty.wchusbserial1460',115200, timeout = 1) # open serial port
    # print(ser.name)

    # print 'Is it open? ' + str(ser.is_open)

    # # I create the map buffer
    # head_matrix = [19,20,4,1,17,18,2,3,51,52,36,33,49,50,34,35]
    # map_mat = map_matrix(head_matrix)

    bigBoardPosition = []

    boardPosition(bigBoardPosition)
    # messega to send
    # message = [32] * 258;
    # header = 255
    # last = 254
    # message[0] = header
    # message[len(message)-1] = last
    
    # #  start the tweezer
    
    # px = 0.0
    # py = 0.0
    # pz = 0.004
    
    # message_phases = []
    # message_phases = calcPhases(px,py,pz)
    # message_phases = discretizeMessage(message_phases)

    # tweezer = [32] * 256
    # # print message_phases
    # # print len(message_phases)


   
    #     # if(i == 2):
    #     #     print 'index ' + str(index)
    #     #     print 'message_phases[i] ' + str(message_phases[i])
    #     #     print 'matrix_calibration[i] ' + str(matrix_calibration[i])
    #     #     print 'cal ' + str(cal)

    # # print 'message phases '    
    # # print message;
    # word = ''
    # while (word!='q'):
    #     word = raw_input("w = 0 amplitude or tweezer ")
    #     if(word == '0'):
    #         sendAmpl(message,32)
    #     else:
    #          for i in range(0,len(map_mat)):
    #             index = map_mat[i]
    #             cal = int(message_phases[i]+matrix_calibration[i])
    #             message[index] = cal
        
    #     sendPattern(ser, message)

        