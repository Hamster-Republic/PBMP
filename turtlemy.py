import turtle

t = turtle.Turtle()
t.speed(5)

digits = {
    "1": [(0,0), (0,100)],
    "2": [(0,50)]
    "5": [(50,100), (0,100), (0,50), (50,50), (50,0), (0,0)],
    "6": [(50,100), (0,100), (0,0), (50,0), (50,50), (0,50)]
}

number = "156"

for digit in number:
    t.penup()
    t.goto(0, 0)
    t.pendown()

    for x, y in digits[digit]:
        t.goto(x, y)

    t.penup()
    t.goto(70, 0)

turtle.done()