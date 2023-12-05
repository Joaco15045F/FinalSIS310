import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar

class SuavizadoExponencialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suavizado Exponencial App")

        self.label_datos = ttk.Label(root, text="Datos por Mes")
        self.label_datos.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="W")

        self.entry_meses = []
        for i, mes in enumerate(calendar.month_name[1:]):  # Ignorar el mes 0
            label_mes = ttk.Label(root, text=f"{mes}:")
            label_mes.grid(row=i + 1, column=0, padx=10, pady=5, sticky="W")
            entry_mes = ttk.Entry(root)
            entry_mes.grid(row=i + 1, column=1, padx=10, pady=5, sticky="W")
            self.entry_meses.append(entry_mes)

        self.label_alpha = ttk.Label(root, text="Factor de suavizado (0 < alpha < 1):")
        self.label_alpha.grid(row=14, column=0, padx=10, pady=5, sticky="W")
        self.entry_alpha = ttk.Entry(root)
        self.entry_alpha.grid(row=14, column=1, padx=10, pady=5, sticky="W")

        self.btn_calcular = ttk.Button(root, text="Calcular Suavizado Exponencial", command=self.calcular_suavizado)
        self.btn_calcular.grid(row=15, column=0, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=16, padx=10, pady=10, sticky="W")

        # Sección para mostrar pronósticos
        self.label_pronosticos = ttk.Label(root, text="Pronósticos")
        self.label_pronosticos.grid(row=0, column=3, padx=10, pady=5, sticky="W")

        self.pronosticos_text = scrolledtext.ScrolledText(root, width=30, height=10, wrap=tk.WORD)
        self.pronosticos_text.grid(row=1, column=3, rowspan=15, padx=10, pady=5, sticky="W")

    def calcular_suavizado(self):
        try:
            datos = [float(entry.get()) for entry in self.entry_meses]
            alpha = float(self.entry_alpha.get())

            # Calcular suavizado exponencial
            suavizado = [datos[0]]
            pronosticos = [suavizado[0]]
            
            for i in range(1, len(datos)):
                suavizado.append(alpha * datos[i-1] + (1 - alpha) * suavizado[-1])
                pronosticos.append(alpha * datos[i-1] + (1 - alpha) * suavizado[-1])

            # Visualizar resultados en el gráfico
            self.ax.clear()
            self.ax.plot(calendar.month_name[1:], datos, label='Datos', marker='o')
            self.ax.plot(calendar.month_name[1:], suavizado, label=f'Suavizado (alpha={alpha})', linestyle='dashed', marker='o')
            self.ax.set_xlabel('Meses')
            self.ax.set_ylabel('Valor')
            self.ax.legend()

            # Mostrar pronósticos en el widget de texto
            self.pronosticos_text.delete(1.0, tk.END)  # Limpiar el contenido anterior
            for mes, pronostico in zip(calendar.month_name[1:], pronosticos):
                self.pronosticos_text.insert(tk.END, f"{mes}: {pronostico:.2f}\n")

            self.canvas.draw()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al calcular el suavizado exponencial: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SuavizadoExponencialApp(root)
    root.mainloop()
