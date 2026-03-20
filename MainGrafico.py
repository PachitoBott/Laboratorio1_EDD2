import tkinter as tk
from InterfazArbol import InterfazArbol
import Arbol

print(Arbol.__file__)
print(hasattr(Arbol.Arbol, "insert"))
print(dir(Arbol.Arbol))

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazArbol(ventana)
    ventana.mainloop()