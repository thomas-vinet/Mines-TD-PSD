from tkinter import Tk, Canvas, Button, Label, Event
import time as time
from random import shuffle, randint

class Data:
    
    def __init__(self, wires: int, crossings: list[int]):
        self.__wires = wires
        self.__crossings = crossings
        
    def crossings(self):
        return self.__crossings
    
    def wires(self):
        return self.__wires
    
    def compute_words(self) -> list[str]:
        words = ["H"] * self.wires()
        pi = list(range(self.wires()))
        for cross in self.crossings():
            if cross == None:
                words = [c + "HH" for c in words]
                continue
            permutate = pi[cross]
            permutateNext = pi[cross + 1]
            words = [c + ("D" if i == permutate else "U" if i == permutateNext else "H") + "H" for i, c in enumerate(words)]
            pi[cross], pi[cross + 1] = pi[cross + 1], pi[cross]
        return words

    def randomize(self, wires = 8, crossings = 8):
        self.__wires = wires
        self.__crossings = [randint(0, wires - 2) for _ in range(crossings)]
        
    def reidemeister(self, m: int) -> int:
        crossing = self.__crossings[m]
        for i in range(m+1, len(self.__crossings)):
            c = self.__crossings[i]
            if c == crossing:
                return i
            if c in (crossing - 1, crossing + 1):
                return -1
        return -1
    
    def reide2(self, m: int):
        v = self.reidemeister(m)
        if v != -1:
            self.__crossings = self.__crossings[:m] + [None] + self.__crossings[m+1:v] + [None] + self.__crossings[v+1:]

class App:
    
    colors = ["black","red","blue","green","brown","pink","orange","cyan"]
    
    def __init__(self, data: Data, canvas_width: int=300, canvas_height: int = 150):
        self.__root = Tk("Entrelacs")
        self.__canvas = Canvas(self.__root, width=canvas_width, height=canvas_height)
        self.__canvas.grid(column=1, row=0, columnspan=3)
        self.__canvas.update()
        self.__data = data
        Label(self.__root, text="Croisements:").grid(column=1, row=1)
        self.__label_crossings = Label(self.__root, text=str(self.__data.crossings()))
        self.__label_crossings.grid(column=3, row=1)
        Button(self.__root, text="Quit", command=lambda: self.__root.quit()).grid(column=1, row=2)
        Button(self.__root, text="Entrelacs", command=lambda: self.generate_data()).grid(column=2, row=2)
        Button(self.__root, text="Colors", command = lambda : self.swap_colors()).grid(column=3, row=2)
        self.__root.bind("<Button-1>", self.apply_reide2)
        self.redraw()
        
    def swap_colors(self):
        shuffle(App.colors)
        self.redraw()
        
    def generate_data(self):
        self.__data.randomize()
        self.redraw()
        
    def redraw(self):
        self.__canvas.delete("all")
        words = self.__data.compute_words()
        W = int( self.__canvas.winfo_width() / len(words[0]))
        H = int( self.__canvas.winfo_height() / (len(words) + 1))
        for index, word in enumerate(words):
            self.draw_word(word, (index+1)*H, W, H, App.colors[index])
        self.__label_crossings.config(text=f"{self.__data.crossings()}")
        
    def draw_word(self, word: str, y: int, w, h, color: str):
        x = 0
        dy = lambda y: 0 if y == "H" else -h if y == "U" else h
        for letter in word:
            nx = x + w
            ny = y + dy(letter)
            self.__canvas.create_line(x, y, nx, ny, fill=color)
            x = nx
            y = ny
        
    def run_forever(self):
        self.__root.mainloop() 
        
    def apply_reide2(self, e: Event):
        pos = e.x // int( self.__canvas.winfo_width() / (2*len(self.__data.crossings()) + 1))
        if pos % 2 == 0:#H pos
            return
        self.__data.reide2(int((pos-1)/2))
        self.redraw()
        

if __name__ == "__main__":
    App(Data(4, [2, 1, 1, 0, 2])).run_forever()
        