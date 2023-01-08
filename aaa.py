import tkinter as tk
import tkinter.filedialog

# Crea la ventana principal de la aplicación
root = tk.Tk()

# Define una función que se llamará cuando se haga clic en el botón "Guardar video"
def save_video() -> None:
    # Abre una ventana de diálogo para seleccionar la ruta de guardado del video
    file_path = tk.filedialog.asksaveasfilename(defaultextension='.mp4')
    
    # Si el usuario ha seleccionado una ruta de guardado
    if file_path:
        # Genera el video y lo guarda en la ruta seleccionada
        print(file_path) 
        #generate_video(file_path)

# Crea un botón que llamará a la función "save_video" cuando se haga clic en él
button = tk.Button(root, text='Guardar video', command=save_video)
button.pack()

# Inicia la aplicación
root.mainloop()
