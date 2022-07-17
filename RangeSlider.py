import customtkinter
import tkinter as tk

class RangeSlider(object):
    HEIGHT = 10
    WIDTH = 4
    RADIUS = 2 * WIDTH  # peut être indépendant de WIDTH
    OFFSET = RADIUS + 1  # valeur minimale
    Y_POS = OFFSET + HEIGHT/2  # valeur minimale

    LEFT = 0   # ids: doivent être
    RIGHT = 1  #      différents

    COLORS =  {
                "inside": "#4A4D50",
                "outside": "#AAB0B5",
                "unselected": "#1F6AA5",
                "selected": "#144870"
            }

    def __init__(self, master, min_=0, max_=100, size=500, num_decimals=0):
        self.master = customtkinter.CTkFrame(master)
        self.convertion_factor = (max_ - min_) / size
        self.num_decimals = num_decimals
        self.canvas=tk.Canvas(self.master, width=size+2*self.OFFSET, height=self.HEIGHT+2*self.OFFSET)

        self.canvas.create_arc(self.OFFSET, self.OFFSET-self.WIDTH/2+self.HEIGHT/2, self.OFFSET+self.WIDTH, self.OFFSET+self.WIDTH/2+self.HEIGHT/2-1, start=90, extent=180, fill=self.COLORS["outside"], outline=self.COLORS["outside"])
        self.canvas.create_arc(self.OFFSET+size-self.WIDTH, self.OFFSET-self.WIDTH/2+self.HEIGHT/2, self.OFFSET+size, self.OFFSET+self.WIDTH/2+self.HEIGHT/2-1, start=270, extent=180, fill=self.COLORS["outside"], outline=self.COLORS["outside"])

        self.L_LIMIT = self.WIDTH/2 + self.OFFSET
        self.R_LIMIT = size-self.WIDTH/2 + self.OFFSET
        self.R_value = tk.StringVar()
        self.L_value = tk.StringVar()
        self.L_point = 1*size/3 + self.OFFSET
        self.R_point = 2*size/3 + self.OFFSET

        self.L_line = self.canvas.create_line(self.L_LIMIT, self.Y_POS, self.L_point, self.Y_POS, fill=self.COLORS["outside"], width=self.WIDTH)
        self.C_line = self.canvas.create_line(self.L_point, self.Y_POS, self.R_point, self.Y_POS, fill=self.COLORS["inside"], width=self.WIDTH)
        self.R_line = self.canvas.create_line(self.R_point, self.Y_POS, self.R_LIMIT, self.Y_POS, fill=self.COLORS["outside"], width=self.WIDTH)

        self.color_circle = self.COLORS["unselected"]
        self.L_circle = self._create_circle(self.L_point, self.Y_POS, self.RADIUS, color=self.color_circle)
        self.R_circle = self._create_circle(self.R_point, self.Y_POS, self.RADIUS, color=self.color_circle)

        self.canvas.pack()
        self._update_public_values()

        self.canvas.bind("<ButtonPress-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.dragging = False
        self.closest = self.LEFT

    def _on_click(self, event):
        self.dragging = True
        self.color_circle = self.COLORS["selected"]

    def _on_move(self, event):
        out_of_scope = event.x < self.L_LIMIT - self.RADIUS/4 or event.x > self.R_LIMIT + self.RADIUS/4
        if out_of_scope:
            return
        if self.dragging:
            self._update_closest(event.x)
            self._move(event.x)

    def _on_release(self, event):
        self.dragging = False
        self.canvas.delete(self.L_circle)
        self.canvas.delete(self.R_circle)
        self.color_circle = self.COLORS["unselected"]
        self.L_circle = self._create_circle(self.L_point, self.Y_POS, self.RADIUS, color=self.color_circle)
        self.R_circle = self._create_circle(self.R_point, self.Y_POS, self.RADIUS, color=self.color_circle)

    def _update_closest(self, x):
        L_dist = abs(self.L_point - x)
        R_dist = abs(self.R_point - x)
        if L_dist < R_dist:
            self.closest = self.LEFT
        else:
            self.closest = self.RIGHT

    def _move(self, new_x):
        if self.closest == self.LEFT:
            self.canvas.delete(self.L_line)
            self.canvas.delete(self.L_circle)
            self.L_point = new_x
            self.L_line = self.canvas.create_line(self.L_LIMIT, self.Y_POS, self.L_point, self.Y_POS, fill=self.COLORS["outside"], width=self.WIDTH)
            self.L_circle = self._create_circle(self.L_point, self.Y_POS, self.RADIUS, color=self.color_circle)
        elif self.closest == self.RIGHT:
            self.canvas.delete(self.R_line)
            self.canvas.delete(self.R_circle)
            self.R_point = new_x
            self.R_line = self.canvas.create_line(self.R_point, self.Y_POS, self.R_LIMIT, self.Y_POS, fill=self.COLORS["outside"], width=self.WIDTH)
            self.R_circle = self._create_circle(self.R_point, self.Y_POS, self.RADIUS, color=self.color_circle)
        self._update_public_values()
        self.canvas.delete(self.C_line)
        self.C_line = self.canvas.create_line(self.L_point, self.Y_POS, self.R_point, self.Y_POS, fill=self.COLORS["inside"], width=self.WIDTH)
        self.canvas.tag_lower(self.C_line)

    def _create_circle(self, x, y, r, color=None):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color)

    def _update_public_values(self):
        new_L_value = (self.L_point - self.OFFSET) * self.convertion_factor
        new_R_value = (self.R_point - self.OFFSET) * self.convertion_factor
        if self.num_decimals > 0:
            new_L_value = round(new_L_value, self.num_decimals)
            new_R_value = round(new_R_value, self.num_decimals)
        else:
            new_L_value = int(new_L_value)
            new_R_value = int(new_R_value)
        self.L_value.set(new_L_value)
        self.R_value.set(new_R_value)

    def grid(self, row, column, padx=0, pady=0):
        self.master.grid(row=row, column=column, padx=padx, pady=pady)

    @property
    def L_IntVar(self):
        return self.L_value

    @property
    def R_IntVar(self):
        return self.R_value

    @property
    def range(self):
        return (float(self.L_value.get()), float(self.R_value.get()))


if __name__ == "__main__":
    root = tk.Tk()
    label = tk.Label(root, text="Test Slider").grid(row=0, column=0, columnspan=4, sticky="new")
    double_slider = RangeSlider(root, size=200)
    double_slider.grid(row=1, column=1)

    tk.Label(root, textvariable=double_slider.L_IntVar, width=4).grid(row=1, column=0, sticky="e")
    tk.Label(root, textvariable=double_slider.R_IntVar, width=4).grid(row=1, column=3, sticky="w")

    root.mainloop()
