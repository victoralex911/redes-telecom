import Tkinter, ImageTk, Image
import numpy as np
import math

w, h = 800, 600
colors = ["red","green","blue"]
iter = 0

# Clase Antena, proporciona las herramientas para pintar los puntos donde se localiza una antena.

class Antena:
    
    # Se inicializa un objeto antena con su posición "x" y "y", el rango máximo de señal,
    # su canvas para pintar y el color asignado.
    
    def __init__(self, x, y, rango, canvas, color):
        self.color = color
        self.x = x
        self.y = y
        self.rango = rango/2
        self.canvas = canvas
        print "Antena:", self.x, self.y

    # Función para pintar el punto de la antena.
    
    def pintar(self):
        self.rec = self.canvas.create_rectangle(self.x-5,self.y-5,self.x+5,self.y+5, fill=self.color)
    
    # Función para pintar los rangos de señal alcanzados para la localización del receptor.
    # el parametro dist sirve para mantener el rango de las señales.
    
    def printAntena(self, dist):
        if dist < self.rango:
            self.ov = self.canvas.create_oval(self.x+(dist),self.y+(dist),self.x-(dist),self.y-(dist), outline=self.color)
        else:
            self.ov = self.canvas.create_oval(self.x+(self.rango),self.y+(self.rango),self.x-(self.rango),self.y-(self.rango), outline=self.color)
    
    # Función para borrar la antena, si el parámetro all es falso solo eliminará el elipse
    # que representa la señal.

    def borrarAntena(self, all = True):
        if all:
            self.canvas.delete(self.ov)
            self.canvas.delete(self.rec)
        else:
            self.canvas.delete(self.ov)

# Se calcula la distancia euclidiana entre 2 puntos.

def distancia(p1, p2):
    x1,y1 = p1
    y2, x2 = p2
    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)

# Se calcula la trilateración entre los 3 puntos y un punto p que es el punto del receptor.

def trilat(xA, yA, xB, yB, xC, yC, p):
    P1 = np.array([xA, yA])
    P2 = np.array([xB, yB])
    P3 = np.array([xC, yC])
    ex = (P2 - P1)/(np.linalg.norm(P2 - P1))
    i = np.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(np.linalg.norm(P3 - P1 - i*ex))
    ez = np.cross(ex,ey)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(ey, P3 - P1)
    D1 = distancia((xA,yA),p)
    D2 = distancia((xB,yB),p)
    D3 = distancia((xC,yC),p)
    x = (pow(D1,2) - pow(D2,2) + pow(d,2))/(2*d)
    y = ((pow(D1,2) - pow(D3,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)
    try:
        z = math.sqrt(pow(D1,2) - pow(x,2) - pow(y,2))
        triPt = P1 + x*ex + y*ey + z*ez
        triPt.tolist()
        print triPt[1], triPt[0]
    except:
        print "Error"

# Se coloca una antena al dar clic izquierdo

def ponerAntenta(event):
    global canvas, iter, antenas
    if len(antenas) < 3:
        A = Antena(event.x,event.y,500, canvas, colors[iter])
        iter+=1
        if iter > 2:
            iter = 0
        A.pintar()
        antenas.append(A)

# Se coloca el punto del receptor y se pintan los rangos alcanzados de las antenas.

def printAntenas(event):
    global antenas,rec
    try:
        canvas.delete(rec)
    except:
        pass
    p = (event.x, event.y)
    rec = canvas.create_rectangle(event.x-5,event.y-5,event.x+5,event.y+5, fill="black")
    lista = []
    for antena in antenas:
        try:
            antena.borrarAntena(False)
        except:
            pass
        lista.append(antena.x)
        lista.append(antena.y)
        antena.printAntena(distancia((antena.x,antena.y),(event.y,event.x)))
    trilat(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5], p)
    print "Real:",event.x,event.y

# Se borra las antenas del mapa.

def borrarAntenas():
    global antenas, canvas
    for antena in antenas:
        antena.borrarAntena()
    antenas = []
    reset()

# Se reinicia el canvas

def reset():
    global canvas
    image = canvas.create_image(0, 0, image = photo, anchor = "nw")
    canvas.tag_bind(image, '<Button-2>', ponerAntenta)
    canvas.tag_bind(image, '<Button-1>', printAntenas)
    canvas.pack()

# Inicio

if __name__ == "__main__":
    antenas = []
    tk = Tkinter.Tk()
    tk.title('Triangulacion')
    B = Tkinter.Button(tk, text ="Reiniciar", command = borrarAntenas)
    B.pack()
    rec = None
    canvas = Tkinter.Canvas(tk, width = w, height = h, background = None)
    photo = ImageTk.PhotoImage(Image.new("RGB", (w,h), (255,255,255)))
    reset()
    tk.mainloop()