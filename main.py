import tkinter
from tkinter import *
import math
from copy import deepcopy

root = Tk()
x = tkinter.IntVar()
touched = False
root.title('grafika')
root.geometry("900x900")

myCanvas = Canvas(root, width=700, height=700, bg="white")
myCanvas.pack(anchor=W)


class Point:
    y: int = 0
    x: int = 0

    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y


first_point = Point(0, 0)
pointsOnPress = []
last_point = Point(0, 0)
line: Canvas
square: Canvas
circle: Canvas
global figure


class Figure:
    points = []
    lines = []

    def __init__(self, points):
        super().__init__()
        self.points = points

    def drawPoints(self):
        global pointsOnPress
        pointsOnPress = []
        newPoints = []
        f = open("wartosci", "w")

        P1.delete(0,len(P1.get()))
        P1.insert(END,str(int(self.points[0].x)) + "," + str(int(self.points[0].y)))

        P2.delete(0,len(P2.get()))
        P2.insert(END,str(int(self.points[1].x)) + "," + str(int(self.points[1].y)))

        P3.delete(0,len(P3.get()))
        P3.insert(END,str(int(self.points[2].x)) + "," + str(int(self.points[2].y)))

        P4.delete(0,len(P4.get()))
        P4.insert(END,str(int(self.points[3].x)) + "," + str(int(self.points[3].y)))

        for i in range(0, len(self.points)):
            line = myCanvas.create_line(self.points[i].x, self.points[i].y, self.points[(i + 1) % len(self.points)].x,
                                        self.points[(i + 1) % len(self.points)].y)
            newPoints.append(self.points[i])
            f.write(str(int(self.points[i].x)) + "," + str(int(self.points[i].y)) + "\n")
            self.lines.append(line)

    def getMaxPointsValue(self):
        maxX = 0
        maxY = 0
        for point in self.points:
            if point.x > maxX:
                maxX = point.x
            if point.y > maxY:
                maxY = point.y
        return maxX, maxY

    pass

    def getMinPointsValue(self):
        minX = 700
        minY = 700
        for point in self.points:
            if point.x < minX:
                minX = point.x
            if point.y < minY:
                minY = point.y
        return minX, minY

    def getCenter(self):
        maxX, maxY = self.getMaxPointsValue()
        minX, minY = self.getMinPointsValue()
        centerX = (maxX + minX) / 2
        centerY = (maxY + minY) / 2
        return centerX, centerY

    def onMove(self, deltaX, deltaY):
        for i in range(len(self.points)):
            self.points[i].x += int(deltaX)
            self.points[i].y += int(deltaY)
        for line in self.lines:
            myCanvas.move(line, deltaX, deltaY)
        self.drawPoints()

    def rotate(self, angle):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = self.getCenter()
        new_points = []
        for point in self.points:
            point.x -= cx
            point.y -= cy
            x_new = point.x * cos_val - point.y * sin_val
            y_new = point.x * sin_val + point.y * cos_val
            new_points.append(Point(x_new + cx, y_new + cy))
        self.points = new_points
        myCanvas.delete("all")
        self.drawPoints()

    def scale(self, n):
        myCanvas.delete("all")
        old_points = deepcopy(self.points)
        for i in range(0, len(self.points)):
            deltaX = old_points[i].x - old_points[(i + 1) % len(old_points)].x
            deltaY = old_points[i].y - old_points[(i + 1) % len(old_points)].y
            self.points[(i + 1) % len(self.points)].x = self.points[i].x - int(deltaX / n)
            self.points[(i + 1) % len(self.points)].y = self.points[i].y - int(deltaY / n)

            line = myCanvas.create_line(self.points[i].x, self.points[i].y, self.points[(i + 1) % len(self.points)].x,
                                        self.points[(i + 1) % len(self.points)].y)
            self.lines.append(line)
        self.drawPoints()


def getDistance(point1, point2):
    return math.sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))


def drawOnButtonClick():
    global P1, P2, P3, P4, figure, pointsOnPress
    myCanvas.delete("all")
    points = []
    if len(pointsOnPress) == 0:
        if P1.get().split(",")[0] != "":
            points.append(Point(int(P1.get().split(",")[0]), int(P1.get().split(",")[1])))
        if P2.get().split(",")[0] != "":
            points.append(Point(int(P2.get().split(",")[0]), int(P2.get().split(",")[1])))
        if P3.get().split(",")[0] != "":
            points.append(Point(int(P3.get().split(",")[0]), int(P3.get().split(",")[1])))
        if P4.get().split(",")[0] != "":
            points.append(Point(int(P4.get().split(",")[0]), int(P4.get().split(",")[1])))
        figure = Figure(points)
    else:
        figure = Figure(pointsOnPress)
    figure.drawPoints()




def press(event):
    global touched, first_point, figure, pointsOnPress

    if event.x <= 700 and event.y <= 700 and x.get() == 1:
        print("obrot")
    elif event.x <= 700 and event.y <= 700 and x.get() == 2:
        print("skalowanie")
    elif event.x <= 700 and event.y <= 700 and x.get() == 3:
        pointsOnPress.append(Point(event.x, event.y))
        print(pointsOnPress)


def on_move(event):
    global last_point, figure
    figure.onMove(event.x - last_point.x, event.y - last_point.y)

    last_point = Point(event.x, event.y)
def onMove(event):
    global last_point
    last_point = Point(event.x, event.y)

def pressRMB(event):
    global first_point


def drawChanges():
    global moveValue, roolValue, scaleValue, figure
    movex = moveValue.get().split(",")[0]
    movey = moveValue.get().split(",")[1]

    figure.onMove(movex,movey)
    if (x.get() == 2):
        figure.rotate(int(roolValue.get()))
    if (x.get() == 1):
        figure.scale(float(scaleValue.get()))


def onReleaseRMB(event):
    global last_point, line, first_point, figure
    value = last_point.x - first_point.x + last_point.y - first_point.y
    value = value / 1000
    if x.get() == 1:
        figure.scale(value)

    deltaX = abs(last_point.x - first_point.x)
    deltaY = abs(last_point.y - first_point.y)
    deltaX2 = pow(deltaX,2)
    deltaY2 = pow(deltaY,2)
    c = deltaX2 + deltaY2
    c = math.sqrt(c)
    if x.get() == 2:
        figure.rotate(math.degrees(math.asin(math.sin(deltaY/c))))







def on_startMoving(event):
    global last_point, first_point
    last_point = Point(event.x, event.y)
    first_point = Point(event.x, event.y)


myCanvas.bind('<Button-1>', press)
myCanvas.bind('<Button-3>', pressRMB)
myCanvas.bind('<Button-3>', onMove)
myCanvas.bind("<B2-Motion>", on_move)
myCanvas.bind("<Button-2>", on_startMoving)
myCanvas.bind("<ButtonRelease-3>", onReleaseRMB)
myCanvas.addtag_all("all")
frame = tkinter.Frame(root)
frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

frame = tkinter.Frame(root)
frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

lineButton = tkinter.Radiobutton(frame, text="Skalowanie", value=1, variable=x)
squareButton = tkinter.Radiobutton(frame, text="Obrot", value=2, variable=x)
circleButton = tkinter.Radiobutton(frame, text="Nowa Figura", value=3, variable=x)
drawOnCommandButton = tkinter.Button(frame, text="Rysuj", command=drawOnButtonClick)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)

P1text = Label(frame, text="P1X,P1Y")
P2text = Label(frame, text="P2X,P2Y")
P3text = Label(frame, text="P3X,P3Y")
P4text = Label(frame, text="P4X,P4Y")

f = open("wartosci", "r")
P1 = Entry(frame)
P1.insert(END, f.readline())
P2 = Entry(frame)
P2.insert(END, f.readline())
P3 = Entry(frame)
P3.insert(END, f.readline())
P4 = Entry(frame)
P4.insert(END, f.readline())
l11 = Label(frame, text="PrzesunięcieX,PrzesuniecieY")
l12 = Label(frame, text="Obrot")
l13 = Label(frame, text="Skalowanie")
l14 = Label(frame, text="Zmiana")
moveValue = Entry(frame)
moveValue.insert(END, "0,0")
roolValue = Entry(frame)
roolValue.insert(END, "0")
scaleValue = Entry(frame)
scaleValue.insert(END, "0")
drawChanges = tkinter.Button(frame, text="Zmień", command=drawChanges)

lineButton.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
squareButton.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
circleButton.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
drawOnCommandButton.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
P1text.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
P2text.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
P3text.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)
P4text.grid(row=1, column=3, sticky=tkinter.W + tkinter.E)
P1.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
P2.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
P3.grid(row=2, column=2, sticky=tkinter.W + tkinter.E)
P4.grid(row=2, column=3, sticky=tkinter.W + tkinter.E)
l11.grid(row=3, column=0, sticky=tkinter.W + tkinter.E)
l12.grid(row=3, column=1, sticky=tkinter.W + tkinter.E)
l13.grid(row=3, column=2, sticky=tkinter.W + tkinter.E)
l14.grid(row=3, column=3, sticky=tkinter.W + tkinter.E)
moveValue.grid(row=4, column=0, sticky=tkinter.W + tkinter.E)
roolValue.grid(row=4, column=1, sticky=tkinter.W + tkinter.E)
scaleValue.grid(row=4, column=2, sticky=tkinter.W + tkinter.E)
drawChanges.grid(row=4, column=3, sticky=tkinter.W + tkinter.E)

root.mainloop()
