import imageio

# Crea un archivo de animación usando imageio
filename = 'animation.gif'
writer = imageio.get_writer(filename, mode='I', fps=30)

# Comprueba si el archivo de animación está vacío
if writer.get_length == 0:
    print("El archivo de animación está vacío")
else:
    print("El archivo de animación tiene", writer.get_length, "fotogramas")