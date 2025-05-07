from tkinter import Tk, Canvas, Button, Label
import time as time

def read_word(canvas: Canvas, mot: str, y: int, h: int, w: int, color: str = "black"):
    x = 0
    assert mot.count("H") + mot.count("U") + mot.count("D") == len(mot)
    dy = lambda y: 0 if y == "H" else -h if y == "U" else h
    for letter in mot:
        nx = x + w
        ny = y + dy(letter)
        canvas.create_line(x, y, nx, ny, fill=color)
        x = nx
        y = ny
        
def words(n: int, crossings: list[int]) -> list[str]:
    out_words = ["H"] * n
    pi = list(range(n))
    for cross in crossings:
        permutate = pi[cross]
        permutateNext = pi[cross + 1]
        out_words = [c + ("D" if i == permutate else "U" if i == permutateNext else "H") + "H" for i, c in enumerate(out_words)]
        pi[cross], pi[cross + 1] = pi[cross + 1], pi[cross]
    return out_words
        
def draw_words(canvas: Canvas, out_words: list[str], color: list[str]):
    W = int( canvas.winfo_width() / len(out_words[0]))
    H = int( canvas.winfo_height() / (len(out_words) + 1))
    canvas.delete("all")
    for i, word in enumerate(out_words):
        read_word(canvas, word, H*(i+1), H, W, color[i])
        


if __name__ == "__main__":
    root = Tk("Hello")
    canvas = Canvas(root, width=300, height=150)
    canvas.grid(column=1, row=0, columnspan=2, padx = 10, pady=10)
    canvas.update()
    colors = ["black", "red", "green", "blue"]
    crossings = [2, 1, 1, 0, 2]
    out_words = words(4, crossings)
    draw_words(canvas, out_words, colors)
    def swap_colors():
        global colors
        cp = []
        for i in range(1, len(colors) + 1):
            cp.append(colors[i % len(colors)])
        colors = cp
        draw_words(canvas, out_words, colors)
    Label(root, text="Croisements:").grid(column=1, row=1)
    Label(root, text=str(crossings)).grid(column=2, row=1)
    Button(root, text="Quit", command=lambda: root.quit()).grid(column=1, row=2)
    Button(root, text="Colors", command = lambda : swap_colors()).grid(column=2, row=2)
    root.mainloop()
        