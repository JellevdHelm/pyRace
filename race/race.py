import turtle
import time as tm
colors = ('red', 'yellow')


class Car:
    def __init__(self, track, color, s):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.speed(0)
        
        if color == 'red':
            self.turtle.shape("carShapeRed")
        else:
            self.turtle.shape("carShapeYellow")
        self.turtle.shapesize(0.4, 1.2, 5)

        self.track = track
        self.a = 25
        self.v = 0
        self.pos = 0
        self.oldPos = 0
        self.offset = 0
        self.aState = 0
        self.bState = 0
        self.crashState = 0
        self.crashPos = 0
        self.winner = 0
        self.crashCount = 0

        

        

    def checkSpeed(self):
        if self.v <= 70: #speedlimit in corners of 70
            return 1
        else:
            return 0

    def accelToggle(self, state): #toggle accellerate
        if state == 1:
            self.aState = 1
        else:
            self.aState = 0

    def brakeToggle(self, state): #toggle brakes
        if state == 1:
            self.bState = 1
        else:
            self.bState = 0

    def accel(self, deltaT): #accel if toggle is 1
        if self.aState == 1:
            if self.v >= 100:
                self.v = 100 #speedlimit of 100
            else:
                self.v += self.a * deltaT

    def brake(self, deltaT): #brake if toggle is 1
        if self.bState == 1:
            if self.v <= 0:
                self.v = 0 #lower limit of 0
            else:
                self.v += -self.a * deltaT

    def turnChecks(self, rotation):
        if self.winner: #check winstate. if winner skip speedcheck
            self.turtle.setheading(rotation)
            self.oldPos = self.pos

        elif self.checkSpeed(): #check speed
            self.turtle.setheading(rotation)
            self.oldPos = self.pos

        else: #crash the car if speed is too high
            self.crashState = 1
            self.crashPos = self.turtle.pos()

    def drive(self, deltaT, s, car):
        
        if car == 0: # set accel and brake toggles on keypress and release
            s.onkeypress(lambda: self.accelToggle(1), "a")
            s.onkeyrelease(lambda: self.accelToggle(0), "a")

            s.onkeypress(lambda: self.brakeToggle(1), 'z')
            s.onkeyrelease(lambda: self.brakeToggle(0), 'z')

        if car == 1:
            s.onkeypress(lambda: self.accelToggle(1), 'k')
            s.onkeyrelease(lambda: self.accelToggle(0), 'k')

            s.onkeypress(lambda: self.brakeToggle(1), 'm')
            s.onkeyrelease(lambda: self.brakeToggle(0), 'm')

        self.accel(deltaT) #run accel and brake if toggle is 1
        self.brake(deltaT)

        self.pos += int(self.v * deltaT)

        if self.crashState == 0: #check crashstate
            # corners
            if 292+self.offset <= self.pos <= 299+self.offset:
                self.turnChecks(90) #check winState and speed.

            elif 751+self.offset <= self.pos <= 758+self.offset:
                self.turnChecks(180)

            elif 1385+self.offset <= self.pos <= 1392+self.offset:
                self.turnChecks(270)

            elif 1608+self.offset <= self.pos <= 1615+self.offset:
                self.turnChecks(0)

            elif 1851+self.offset <= self.pos <= 1858+self.offset:
                self.turnChecks(270)

            elif 2082+self.offset <= self.pos <= 2089+self.offset:
                self.turnChecks(0)


            # straight
            if 0 <= self.pos <= 291+self.offset:
                self.turtle.setposition(self.pos, -262-self.offset)

            elif 291+self.offset <= self.pos <= 750+self.offset:
                self.turtle.setposition(292+self.offset, -262+(self.pos-self.oldPos))

            elif 750+self.offset <= self.pos <= 1384+self.offset:
                self.turtle.setposition(292-(self.pos-self.oldPos), 192+self.offset)

            elif 1384+self.offset <= self.pos <= 1605+self.offset:
                self.turtle.setposition(-347-self.offset, 192-(self.pos-self.oldPos))

            elif 1607+self.offset <= self.pos <= 1850+self.offset:
                self.turtle.setposition(-347+(self.pos-self.oldPos), -32-self.offset)
            
            elif 1850+self.offset <= self.pos <= 2080+self.offset:
                self.turtle.setposition(-92-self.offset, -32-(self.pos-self.oldPos))

            elif 2081+self.offset <= self.pos <= 2172+self.offset:
                self.turtle.setposition(-92+(self.pos-self.oldPos), -262-self.offset)

            elif self.pos > 2172+self.offset:
                self.pos = 0
                self.oldPos = 0
        
        else:
            if self.crashCount < 10: #if crashed spin for a while
                self.turtle.lt(10)
                self.turtle.setposition(self.crashPos)
                self.crashCount += 1

        #print(self.pos)


class Track:
    def __init__(self, game):
        self.game = game
        self.s = turtle.Screen()
        self.s.register_shape('shape4.gif')
        self.s.setup(1095, 670)

        #car compound shape
        shape = turtle.Shape("compound")
        poly1 = ((-10, 10),(-10, -10),(10, -10),(10, 10))
        poly2 = ((-8, 8),(8, 8),(8, 6),(-8, 6))
        shape.addcomponent(poly1, 'red', 'red')
        shape.addcomponent(poly2, 'blue', 'blue')
        self.s.register_shape("carShapeRed", shape)

        shape = turtle.Shape("compound")
        poly1 = ((-10, 10),(-10, -10),(10, -10),(10, 10))
        poly2 = ((-8, 8),(8, 8),(8, 6),(-8, 6))
        shape.addcomponent(poly1, 'yellow', 'yellow')
        shape.addcomponent(poly2, 'blue', 'blue')
        self.s.register_shape("carShapeYellow", shape)

        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.setposition(-150, 0)
        self.turtle.shape('shape4.gif')

        self.text = turtle.Turtle()
        self.style = ('Coutier', 30)
        self.text.hideturtle()
        
        self.cars = tuple(Car(self, color, self.s) for color in colors) #make car objects
        self.time = tm.time()

    def run(self):
        self.oldTime = self.time
        self.time = tm.time()
        self.deltaT = self.time - self.oldTime #calculate deltaTime
        self.written = 0

        if self.written == 0: # check if text has been written before
            if self.cars[0].crashState: #check crashState of car
                self.text.color('yellow')
                self.text.write('Yellow has won!!!', font=self.style, align='center')
                self.cars[1].winner = 1
                self.written = 1
            elif self.cars[1].crashState:
                self.text.color('red')
                self.text.write('Red has won!!!', font=self.style, align='center')
                self.cars[0].winner = 1
                self.written = 1


        #drive cars
        self.cars[0].drive(self.deltaT, self.s, 0)
        self.cars[1].drive(self.deltaT, self.s, 1)

        self.s.listen()
        self.s.update()
        tm.sleep(0.02)


class Game:
    def __init__(self):
        self.track = Track(self)


game = Game()
game.track.cars[0].turtle.setposition(0, -276)  # red
game.track.cars[1].turtle.setposition(0, -262)  # yellow
game.track.cars[0].offset = 14
while True:
    game.track.run()