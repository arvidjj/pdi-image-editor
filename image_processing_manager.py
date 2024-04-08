import numpy as np
import cv2

class ImageProcessingManager():
  """
    Esta libreria contiene la implementación de los procesos internos del
    Editor de Imagenes.
    Desarrollador por: Angel Ojeda
  """

  DEFAULT_WIDTH = 512
  DEFAULT_HEIGHT = 512

  def __init__(self):
    super(ImageProcessingManager, self).__init__()

    # Por defecto tenemos una imagen blanca en la pila.
    initial_matrix = np.ones((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT, 3), np.uint8) * 255
    
    # Estructura de imagenes
    self.stack_images = [initial_matrix]
    
    # Estructura de puntos/lineas
    self.stack_lines = []

  
  def rgb_to_hex(self, rgb):
    """
      Conversor de un string hexadecimal a arreglos.
      Fuente: https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
    """
    #print(rgb)
    #return '%02x%02x%02x' % rgb
    #se tuvo que modificar la funcion para que aceptara un string
    rgb = rgb.lstrip('#')
    length = len(rgb)
    rgb = tuple(int(rgb[i:i+length//3], 16) for i in range(0, length, length//3))
    return rgb


  def last_image(self):
    """
      NO ALTERAR ESTA FUNCION
      Obtenemos la ultima imagen de nuestra estructura.
    """
    return self.stack_images[-1]

  def can_undo(self):
    """
      NO ALTERAR ESTA FUNCION
      Determinamos si la aplicación puede eliminar
      elementos de la pila.
      Debe haber por lo menos más de un elemento para que 
      se pueda deshacer la imagen
    """
    return len(self.stack_images) > 1

  def has_changes(self):
    """
      NO ALTERAR ESTA FUNCION
      Determinamos si la aplicación contiene
      elementos de la pila.
    """
    return len(self.stack_images) > 1

  def add_image(self, image_path):
    """
      Leemos una imagen con OpenCV
      Redimensionamos segun los parametros: DEFAULT_WIDTH y DEFAULT_HEIGHT
      Agregamos una nueva imagen redimensionada en la pila.

      Obs: No te olvides de vaciar las colecciones antes de cargar la imagen.
    """
    # TU IMPLEMENTACION AQUI
    self.stack_images.clear() #vaciar la pila

    image = cv2.imread(image_path) #leo la iamgen en c  olor
    resized_image = cv2.resize(image, (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))
    self.stack_images.append(resized_image)

  def save_image(self, filename):
    """
       Guardamos la ultima imagen
    """
    # TU IMPLEMENTACION AQUI
    new_image = self.stack_images[-1]
    #si el nombre de la imagen no incluye extension png o jpg, se le agrega
    if not filename.endswith('.png') and not filename.endswith('.jpg'):
      filename += '.png'
    cv2.imwrite(filename, new_image)

  def undo_changes(self):
    """
      Eliminamos el ultimo elemento guardado.
    """
    # TU IMPLEMENTACION AQUI
    self.stack_images.pop()


  def save_points(self, x1, y1, x2, y2, line_width, color):
    """
      Guardamos informacion de los puntos aqui en self.stack_lines.
    """
    # TU IMPLEMENTACION AQUI
    self.stack_lines.append([x1, y1, x2, y2, line_width, color])


  def add_lines_to_image(self):
    """
      Creamos una matriz, con un conjunto de lineas.
      Estas lineas se obtienen de self.stack_lines.

      Finalmente guardamos a nuestra pila de imagenes: self.stack_images.

      Ayuda: ver documentacion de "cv2.line" para dibujar lineas en una matriz
      Ayuda 2: no se olviden de limpiar self.stack_lines
      Ayuda 3: utilizar el metodo rgb_to_hex para convertir los colores
    """
    # TU IMPLEMENTACION AQUI
    nueva_imagen = self.stack_images[-1].copy() #crear nueva imagen con la nueva linea a partir de la ultima imagen guardad en el stack
    for linea in self.stack_lines:
        x1, y1, x2, y2, line_width, rgb_color = linea
        color_hex = self.rgb_to_hex(rgb_color) #pasar de hex a rgb el color
        cv2.line(nueva_imagen, (x1, y1), (x2, y2), color_hex, int(line_width)) #hay que convertir a integer algunos valores
    self.stack_images.append(nueva_imagen)
    self.stack_lines = []

  def black_and_white_image(self):
    """
      Hacemos una copia de la ultima imagen.
      La Convertimos covertimos a blanco y negro.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """
    last = self.stack_images[-1].copy()
    # TU IMPLEMENTACION AQUI
    last = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    return last

  def negative_image(self):
    """
      Hacemos una copia de la ultima imagen.
      Calculamos el negativo de la imagen.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """
    last = self.stack_images[-1].copy()
    # TU IMPLEMENTACION AQUI
    last = 255 - last
    return last

  def global_equalization_image(self):
    """
      Hacemos una copia de la ultima imagen.
      Equalizamos la imagen.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """
    last = self.stack_images[-1].copy()
    # TU IMPLEMENTACION AQUI
    last_ycrcb = cv2.cvtColor(last, cv2.COLOR_BGR2YCrCb)
    last_ycrcb[:,:,0] = cv2.equalizeHist(last_ycrcb[:,:,0])
    last = cv2.cvtColor(last_ycrcb, cv2.COLOR_YCrCb2BGR)
    last = cv2.cvtColor(last, cv2.COLOR_BGR2RGB)
    return last

  def CLAHE_equalization_image(self, grid=(8, 8), clipLimit=2.0):
    """
      Hacemos una copia de la ultima imagen.
      Equalizamos la imagen usando el algoritmo de CLAHE.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """
    last = self.stack_images[-1].copy()
    # TU IMPLEMENTACION AQUI
    last_ycrcb = cv2.cvtColor(last, cv2.COLOR_BGR2YCrCb)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=grid) #crear objeto clahe
    last_ycrcb[:,:,0] = clahe.apply(last_ycrcb[:,:,0]) #aplicar clahe a la imagen
    last = cv2.cvtColor(last_ycrcb, cv2.COLOR_YCrCb2BGR)
    last = cv2.cvtColor(last, cv2.COLOR_BGR2RGB)
    return last

  def contrast_and_brightness_processing_image(self, alpha, beta):
    """
      Hacemos una copia de la ultima imagen.
      Ajustamos la imagen segun parametros alpha y beta.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.

      Fuente teorica: http://szeliski.org/Book/drafts/SzeliskiBook_20100903_draft.pdf
      Pagina 103

      OpenCV:
      https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html

      Función en OpenCV:
      https://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#convertscaleabs
    """
    last = self.stack_images[-1].copy()
    # TU IMPLEMENTACION AQUI
    last = cv2.convertScaleAbs(last, alpha=alpha, beta=beta) #basic linear transform, opencv
    return last
