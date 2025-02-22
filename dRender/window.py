from tkinter import Canvas, Tk


class Surface (Canvas):
    def __init__(self, width=400, height=400, master=Tk(), title="APP"):
        self.width = width
        self.height = height
        master.title(title)
        # master.resizable(False, False)
        super().__init__(master=master, width=width, height=height, background="#E0F2F7")
        self.pack(expand=True, fill='both')
        self.focus_set()

    def setOnClick(self, func):
        self.bind("<Button-1>", func)
        return self

    def setKeyPress(self, func):
        self.bind("<Key>", func)
        return self

    def run(self):
        self.mainloop()
