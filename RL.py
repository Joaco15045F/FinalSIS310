import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression

class RegresionLinealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regresión Lineal App")
        self.root.configure(bg='#D6D6D6')

        # Estilo del botón
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        # Fuente Arial 12
        font_style = ('Arial', 12)

        self.label_datos = ttk.Label(root, text="Datos (X, Y)", font=font_style)
        self.label_datos.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="W")

        # Configuración de las celdas de entrada para X
        self.entry_x = ttk.Entry(root, font=font_style, width=15)
        self.entry_x.grid(row=1, column=1, padx=10, pady=5, sticky="W")
        self.label_x = ttk.Label(root, text="X:", font=font_style)
        self.label_x.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        # Configuración de las celdas de entrada para Y
        self.entry_y = ttk.Entry(root, font=font_style, width=15)
        self.entry_y.grid(row=2, column=1, padx=10, pady=5, sticky="W")
        self.label_y = ttk.Label(root, text="Y:", font=font_style)
        self.label_y.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        self.btn_calcular = ttk.Button(root, text="Calcular Regresión Lineal", command=self.calcular_regresion)
        self.btn_calcular.grid(row=3, column=0, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="W")

        # Sección para mostrar resultados de la regresión
        self.label_resultados = ttk.Label(root, text="Resultados de la Regresión", font=font_style)
        self.label_resultados.grid(row=0, column=3, padx=10, pady=5, sticky="W")

        self.resultados_text = scrolledtext.ScrolledText(root, width=30, height=8, wrap=tk.WORD, font=font_style)
        self.resultados_text.grid(row=1, column=3, rowspan=3, padx=10, pady=5, sticky="W")

    def calcular_regresion(self):
        try:
            # Obtener datos de las entradas
            x = np.array([float(value) for value in self.entry_x.get().split(",")])
            y = np.array([float(value) for value in self.entry_y.get().split(",")])

            # Realizar regresión lineal
            model = LinearRegression()
            x = x.reshape(-1, 1)  # Asegurar que x sea una matriz 2D
            model.fit(x, y)

            # Obtener los coeficientes de la regresión
            slope = model.coef_[0]
            intercept = model.intercept_

            # Calcular pronósticos para cada mes
            pronosticos = model.predict(x.reshape(-1, 1))

            # Visualizar resultados en el gráfico
            self.ax.clear()

            # Graficar las demandas en azul
            self.ax.plot(x, y, label='Demandas (Y)', linestyle='-', marker='o', color='blue')
            
            # Trazar la regresión lineal
            x_line = np.linspace(np.min(x), np.max(x), 100).reshape(-1, 1)
            self.ax.plot(x_line, model.predict(x_line), label=f'Regresión Lineal', linestyle='dashed', color='red')

            # Graficar los pronósticos en verde
            self.ax.plot(x, pronosticos, label='Pronósticos', linestyle='-', marker='o', color='green')

            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.legend()

            # Mostrar resultados en el widget de texto
            self.resultados_text.delete(1.0, tk.END)  # Limpiar el contenido anterior
            self.resultados_text.insert(tk.END, f"Pendiente (a): {intercept:.4f}\n")
            self.resultados_text.insert(tk.END, f"Intercepto (b): {slope:.4f}\n")
            self.resultados_text.insert(tk.END, "Pronósticos por Mes:\n")
            
            for i, pronostico in enumerate(pronosticos):
                self.resultados_text.insert(tk.END, f"Mes {i+1}: {pronostico:.4f}\n")

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la regresión lineal: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegresionLinealApp(root)
    root.mainloop()
