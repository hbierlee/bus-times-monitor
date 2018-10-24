from sense_hat import SenseHat
sense = SenseHat()


def display_quadrant(time, color_a, color_b, lights):
    size = len(lights) - 1
    for i in range(len(lights)):
        if time < 16 and i == 0:
            lights[size] = color_b
        elif time >= (size - i) + 1:
            lights[size - i] = color_a
        else:
            lights[size - i] = color_b
    return lights


def busA(time):
    # bus-line 4, going direction A [green leds]
    green = [0, 128, 0]
    white = [255, 255, 255]
    busALights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return display_quadrant(time, green, white, busALights)


def busB(time):
    # top-right: bus-line 4, going direction B [blue leds]
    blue = [0, 0, 255]
    white = [255, 255, 255]
    busBLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return display_quadrant(time, blue, white, busBLights)


def busC(time):
    # down-left: bus-line 12, going direction A [yellow leds]
    yellow = [255, 255, 0]
    white = [255, 255, 255]
    busCLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return display_quadrant(time, yellow, white, busCLights)


def busD(time):
    # down-right: bus-line 12, going direction B [red leds]
    red = [255, 0, 0]
    white = [255, 255, 255]
    busDLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return display_quadrant(time, red, white, busDLights)


def display_first(a):
    counter = 0
    for i in range(0, 4):
        for j in range(0, 4):
            print(str(i) + "\t" + str(j))
            #print(a[counter])
            sense.set_pixel(i, j, a[counter])
            counter += 1


def display_second(a):
    counter = 0
    for i in range(4, 8):
        for j in range(0, 4):
            #print(a[counter])
            #print(str(i) + "\t" + str(j))
            sense.set_pixel(i, j, a[counter])
            counter += 1


def display_third(a):
    counter = 0
    for i in range(0, 4):
        for j in range(4, 8):
            #print(a[counter])
            #print(str(i) + "\t" + str(j))
            sense.set_pixel(i, j, a[counter])
            counter += 1


def display_fourth(a):
    counter = 0
    for i in range(4, 8):
        for j in range(4, 8):
            #print(a[counter])
            #print(str(i) + "\t" + str(j))
            sense.set_pixel(i, j, a[counter])
            counter += 1

def display(timeA, timeB, timeC, timeD):
    display_first(busA(timeA))
    display_second(busB(timeB))
    display_third(busC(timeC))
    display_fourth(busD(timeD))
