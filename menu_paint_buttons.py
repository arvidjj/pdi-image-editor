from tkinter.ttk import Frame, Button, Entry, Style, Label
from tkinter import *
import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
from tkinter import simpledialog
from file_manager import FileManager

class MenuPaintButtonGroup(Frame):
  DEFAULT_COLOR = '#000000' # Black
  DEFAULT_PEN_SIZE = 2.0
  THIN_PENSIZE = 2.0
  THICK_PENSIZE = 8.0
  PENCIL_SIZE = 1.0

  def __init__(self, root, canvas, img_processing_manager):
    super().__init__(root)
    self.root = root
    self.canvas = canvas
    self.img_processing_manager = img_processing_manager
    self.pen_size = self.THICK_PENSIZE
    self.stack = []
    self.temp_lines = []
    self.init()

  def init(self):
    self.master.title('FIUNI Paint')
    Style().configure("TButton", margin=(50, 20, 50, 20), font='serif 10' )

    title_label = Label(self, text="Herramientas", padx=5, pady=10)
    title_label_2 = Label(self, text="Colores", padx=5, pady=10)
    # label_color = Label(self, text="Color actual", pady=10)

    self.thick_brush_button = Button(self, text='Pincel Grueso', width=20, padx=5, pady=10, command=self.use_thick_brush)

    # Declaring button for zoom
    self.thin_brush_button = Button(self, text='Pincel Fino', width=20, padx=5, pady=10, command=self.use_thin_brush)

    # Declaring eraser button
    self.eraser_button = Button(self, text='Borrador', width=20, padx=5, pady=10, command=self.use_eraser)

    # Declaring pencil button
    self.pencil_button = Button(self, text='Lapiz', width=20, padx=5, pady=10, command=self.use_pencil)

    title_label.grid(column=1, rowspan=2, sticky=tk.N)
    self.thick_brush_button.grid(column=1, rowspan=2, sticky=tk.N)
    self.thin_brush_button.grid(column=1, rowspan=2, sticky=tk.N)
    self.eraser_button.grid(column=1, rowspan=2)
    self.pencil_button.grid(column=1, rowspan=2)

    self.canvas_color = tk.Canvas(self, width=64, height=32, bg=self.DEFAULT_COLOR)
    self.color_picker_button = Button(self, text='Elija Color', command=self.use_color_picker)

    Label(self, text="Color Actual").grid(column=1, sticky=tk.N, padx=5, pady=10)

    #title_label_2.grid(column=1, rowspan=2, sticky=tk.N)
    self.canvas_color.grid(column=1, row=11, sticky=tk.W)
    self.color_picker_button.grid(column=1, row=11, sticky=tk.E)

    self.old_x = None
    self.old_y = None
    # self.line_width = self.choose_size_button.get()
    self.color = self.DEFAULT_COLOR
    self.eraser_on = False
    self.pen_mode = False
    self.active_button = self.thick_brush_button
    self.active_button.config(relief=tk.SUNKEN)
    self.root.config(cursor='dot')
    self.canvas.bind('<Button-1>', self.start_painting)
    self.canvas.bind('<B1-Motion>', self.painting)
    self.canvas.bind('<ButtonRelease-1>', self.stop_painting)

  def use_thick_brush(self):
    self.root.config(cursor='dot')
    self.activate_button(self.thick_brush_button, pen_size=self.THICK_PENSIZE)

  def use_thin_brush(self):
    self.root.config(cursor='dot')
    self.activate_button(self.thin_brush_button, pen_size=self.THIN_PENSIZE)

  def use_eraser(self):
    self.root.config(cursor='dotbox')
    self.activate_button(self.eraser_button, eraser_mode=True, pen_size=self.THICK_PENSIZE)

  def use_pencil(self):
    self.root.config(cursor='pencil')
    self.activate_button(self.pencil_button, pen_mode=True, pen_size=self.PENCIL_SIZE)

  def use_color_picker(self):
    self.root.config(cursor='hand1')
    self.color = askcolor(color=self.color)[1]
    self.canvas_color.delete('all')
    self.canvas_color.configure(bg=self.color)

  def activate_button(self, some_button, eraser_mode=False, pen_mode=False, pen_size=DEFAULT_PEN_SIZE):
    self.active_button.config(relief=tk.RAISED)
    some_button.config(relief=tk.SUNKEN)
    self.active_button = some_button
    self.eraser_on = eraser_mode
    self.pen_size = pen_size
    self.pen_mode = pen_mode

  def start_painting(self, event):
    pass

  def painting(self, event):
    self.line_width = self.pen_size
    paint_color = self.DEFAULT_COLOR
    if self.eraser_on:
      paint_color = '#FFFFFF'
    elif self.pen_mode:
      paint_color = self.DEFAULT_COLOR
    else:
      paint_color = self.color

    if self.old_x and self.old_y:
      temp_line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
      self.canvas.add_temp_line(temp_line)
      self.img_processing_manager.save_points(self.old_x, self.old_y, event.x, event.y, self.line_width, paint_color)

    self.old_x = event.x
    self.old_y = event.y

  def stop_painting(self, event):
    self.old_x, self.old_y = None, None
    self.canvas.stack_lines()
    self.canvas.delete('temp_line_objects')
    self.img_processing_manager.add_lines_to_image()

class EnhancementButtonGroup(Frame):
  """docstring for EnhancementButtonGroup"""
  def __init__(self, root, canvas, img_processing_manager):
    super().__init__(root)
    self.root = root
    self.canvas = canvas
    self.img_processing_manager = img_processing_manager
    self.frame_image = None
    self.init()

  def init(self):
    Label(self, text="Filtros").grid(column=1, rowspan=2, sticky=tk.N, padx=5, pady=10)
    self.black_and_white_button = Button(self, text='Blanco y Negro', command=self.use_black_and_white_filter, width=20, padx=5, pady=10)
    self.black_and_white_button.grid(column=1, rowspan=2, sticky=tk.N)

    self.negative_button = Button(self, text='Negativo', command=self.use_negative_filter, width=20, padx=5, pady=10)
    self.negative_button.grid(column=1, rowspan=2, sticky=tk.N)

    Label(self, text="Mejoras").grid(column=1, rowspan=2, sticky=tk.N, padx=5, pady=10)

    self.equalize_button = Button(self, text='Equalizacion Global', command=self.use_global_equalization, width=20, padx=5, pady=10)
    self.equalize_button.grid(column=1, rowspan=2, sticky=tk.N)

    self.equalize_clahe_button = Button(self, text='Ecualización por Seccion', command=self.equalize_image_by_grid, width=20, padx=5, pady=10)
    self.equalize_clahe_button.grid(column=1, rowspan=2, sticky=tk.N)

    Label(self, text="Ajustes").grid(column=1, rowspan=2, sticky=tk.N, padx=5, pady=10)
    Label(self, text="Brillo").grid(column=1, row=17, sticky=tk.W, padx=5, pady=5)
    Label(self, text="Contraste").grid(column=1, row=17, sticky=tk.E, padx=5, pady=5)

    self.size_brightness = Scale(self, from_=0, to=100, orient=VERTICAL, command=lambda value: self.use_brightness(value))
    self.size_brightness.grid(column=1, row=18, sticky=tk.E)
    self.beta = 0
        
    self.size_contrast = Scale(self, from_=10, to=30, orient=VERTICAL, command=lambda value: self.use_contrast(value))
    self.size_contrast.grid(column=1, row=18, sticky=tk.W)
    self.alpha = 1.0

    self.bright_constrast_button = Button(self, text='Brillo y Constraste', command=self.use_bright_and_constrast, width=20, padx=5, pady=10)
    self.bright_constrast_button.grid(column=1, rowspan=2, sticky=tk.N)

  def use_black_and_white_filter(self):
    bw_image = self.img_processing_manager.black_and_white_image()
    image =  ImageTk.PhotoImage(image=Image.fromarray(bw_image))
    self.canvas.add_image(image)
    self.root.mainloop()

  def use_negative_filter(self):
    negative = self.img_processing_manager.negative_image()
    image =  ImageTk.PhotoImage(image=Image.fromarray(negative))
    self.canvas.add_image(image)
    self.root.mainloop()

  def use_global_equalization(self):
    global_eq_img = self.img_processing_manager.global_equalization_image()
    image =  ImageTk.PhotoImage(image=Image.fromarray(global_eq_img))
    self.canvas.add_image(image)
    self.root.mainloop()


  def equalize_image_by_grid(self):
    answer = simpledialog.askinteger("Tamaño de la grilla", "¿Cual es el Tamaño de la grilla?", parent=self, minvalue=0, maxvalue=512)
    if answer is not None:
      clahe_eq_img = self.img_processing_manager.CLAHE_equalization_image(grid=(answer, answer))
      image =  ImageTk.PhotoImage(image=Image.fromarray(clahe_eq_img))
      self.canvas.add_image(image)
      self.root.mainloop()

  def use_brightness(self, value):
    self.alpha = int(value)

  def use_contrast(self, value):
    self.beta = float(value)

  def use_bright_and_constrast(self):
    adjusted_img = self.img_processing_manager.contrast_and_brightness_processing_image(self.alpha, self.beta)
    image =  ImageTk.PhotoImage(image=Image.fromarray(adjusted_img))
    self.canvas.add_image(image)
    self.root.mainloop()

class MenuAction(Frame):
  def __init__(self, root, canvas, img_processing_manager):
    super().__init__(root)
    self.root = root
    self.canvas = canvas
    self.img_processing_manager = img_processing_manager
    self.init()
    #Shortcuts
    self.root.bind("<Control-z>", self.undo_image)

  def init(self):
    Style().configure("TButton", margin=(50, 20, 50, 20), font='serif 10' )

    self.open_button = Button(self, text='Abrir', padx=5, pady=10, width=10, command=self.upload_image)
    self.save_button = Button(self, text='Guardar', padx=5, pady=10, width=10, command=self.save_image)
    self.undo_button = Button(self, text='Deshacer', padx=5, pady=10, width=10, command=self.undo_image)

    self.open_button.grid(row=0, column=0)
    self.save_button.grid(row=0, column=1)
    self.undo_button.grid(row=0, column=2)

  def upload_image(self):
    FileManager.upload_image(self.root, self.canvas, self.img_processing_manager)

  def save_image(self):
    FileManager.save_image(self.root, self.canvas, self.img_processing_manager)

  def undo_image(self, event=None):
    print('can undo', self.img_processing_manager.can_undo())
    if self.img_processing_manager.can_undo():
      list_lines = self.canvas.pop()
      for line in list_lines:
        self.canvas.delete(line)
      self.img_processing_manager.undo_changes()

  def quit(self):
    FileManager.quit(self.root, self.canvas)
