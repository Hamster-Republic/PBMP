import turtle
import math

# Настройка экрана
screen = turtle.Screen()
screen.bgcolor("lightblue")  # Цвет фона - небо
screen.title("Морской пейзаж")

# Создаем черепаху
t = turtle.Turtle()
t.speed(10)  # Ускоряем рисование
t.hideturtle()  # Скрываем черепаху

# Функция для рисования моря
def draw_sea():
    t.penup()
    t.goto(-400, -100)  # Начальная позиция для моря
    t.pendown()
    t.fillcolor("blue")
    t.begin_fill()
    for _ in range(2):
        t.forward(800)
        t.right(90)
        t.forward(300)
        t.right(90)
    t.end_fill()

# Функция для рисования солнца
def draw_sun():
    t.penup()
    t.goto(-200, 150)
    t.pendown()
    t.fillcolor("yellow")
    t.begin_fill()
    t.circle(50)  # Рисуем круг (солнце)
    t.end_fill()

# Функция для рисования облака
def draw_cloud(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(3):
        t.circle(20)  # Рисуем три круга для облака
        t.penup()
        t.forward(30)
        t.pendown()
    t.end_fill()

# Функция для рисования пальмы
def draw_palm_tree():
    # Ствол
    t.penup()
    t.goto(150, -100)
    t.pendown()
    t.fillcolor("brown")
    t.begin_fill()
    t.setheading(90)  # Направление вверх
    t.forward(150)  # Длина ствола
    t.left(90)
    t.forward(10)
    t.left(90)
    t.forward(150)
    t.left(90)
    t.forward(10)
    t.end_fill()

    # Листья
    t.fillcolor("green")
    for _ in range(5):  # Рисуем 5 листьев
        t.penup()
        t.goto(150, 50)
        t.setheading(90)
        t.left(45 + _ * 20)  # Разные углы для листьев
        t.pendown()
        t.begin_fill()
        t.forward(80)
        t.left(45)
        t.forward(20)
        t.left(135)
        t.forward(90)
        t.end_fill()

# Функция для рисования лодки
def draw_boat():
    t.penup()
    t.goto(-50, -150)
    t.pendown()
    t.fillcolor("brown")
    t.begin_fill()
    t.setheading(0)
    t.forward(100)  # Корпус лодки
    t.left(135)
    t.forward(20 * math.sqrt(2))
    t.left(45)
    t.forward(60)
    t.left(45)
    t.forward(20 * math.sqrt(2))
    t.end_fill()

    # Парус
    t.penup()
    t.goto(0, -150)
    t.setheading(90)
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    t.forward(80)
    t.right(135)
    t.forward(60)
    t.right(90)
    t.forward(60)
    t.end_fill()

# Рисуем элементы пейзажа
draw_sea()
draw_sun()
draw_cloud(-100, 100)
draw_cloud(50, 120)
draw_palm_tree()
draw_boat()

# Завершаем программу
t.hideturtle()
screen.mainloop()