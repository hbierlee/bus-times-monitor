# from sense_hat import SenseHat
# sense = SenseHat()


def assigner(time, color_a, color_b, lights):
    size = len(lights) - 1
    for i in range(len(lights)):
        if i == 0:
            lights[size] = color_a
        elif i >= time:
            lights[size - i] = color_b
        else:
            lights[size - i] = color_a
    return lights


def busA(time):
    # bus-line 4, going direction A [green leds]
    green = [0, 128, 0]
    white = [255, 255, 255]
    busALights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return assigner(time, green, white, busALights)


def busB(time):
    # top-right: bus-line 4, going direction B [blue leds]
    blue = [0, 0, 255]
    white = [255, 255, 255]
    busBLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return assigner(time, blue, white, busBLights)


def busC(time):
    # down-left: bus-line 12, going direction A [yellow leds]
    yellow = [255, 255, 0]
    white = [255, 255, 255]
    busCLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return assigner(time, yellow, white, busCLights)


def busD(time):
    # down-right: bus-line 12, going direction B [red leds]
    red = [255, 0, 0]
    white = [255, 255, 255]
    busDLights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    return assigner(time, red, white, busDLights)


def combine(a, b, c, d):
    return [busA(a), busB(b), busC(c), busD(d)]


def main():
    #sense.set_pixels(combine(80, 5, 15, 55))
    print combine(80, 5, 15, 55)


if __name__ == '__main__':
    main()
