import imageio
import os

# Crea una lista de imágenes
images = []
for file_name in os.listdir('saved_images\\hexagonB2S345_blinker'):
    if file_name.endswith('.png'):
        file_path = os.path.join('saved_images\\hexagonB2S345_blinker', file_name)
        images.append(imageio.v2.imread(file_path))

# Genera el gif
imageio.mimsave('gif_name.gif', images, fps=1)
