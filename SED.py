import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar

class SuavizadoExponencialDobleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suavizado Exponencial Doble App")

        # Cambios en la fuente y tamaño
        self.root.option_add('*Font', 'Arial 12')

        self.label_datos = ttk.Label(root, text="Datos por Mes")
        self.label_datos.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="W")

        self.entry_meses = []
        for i in range(20):  # Ajusta el rango según la cantidad de columnas que tengas
            self.root.columnconfigure(i, weight=1)

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

        self.label_beta = ttk.Label(root, text="Factor de suavizado de la tendencia (0 < beta < 1):")
        self.label_beta.grid(row=15, column=0, padx=10, pady=5, sticky="W")
        self.entry_beta = ttk.Entry(root)
        self.entry_beta.grid(row=15, column=1, padx=10, pady=5, sticky="W")

        tk.Button(root, text="Calcular Suavizado Exponencial Doble",font=("Arial",12) ,command=self.calcular_suavizado_doble).grid(row=16, column=0, columnspan=3, pady=20)

        # Crear etiquetas para mostrar los resultados de A_t, T_t y P_(t+rho) para cada mes
        self.labels_at = []
        self.labels_tt = []
        self.labels_pt = []

        for i, mes in enumerate(calendar.month_name[1:]):
            label_at = ttk.Label(root, text=f"{mes}: At=0.0")
            label_at.grid(row=i + 1, column=2, padx=10, pady=5, sticky="W")
            self.labels_at.append(label_at)

            label_tt = ttk.Label(root, text=f"Tt=0.0")
            label_tt.grid(row=i + 1, column=3, padx=10, pady=5, sticky="W")
            self.labels_tt.append(label_tt)

            label_pt = ttk.Label(root, text=f"Pt=0.0")
            label_pt.grid(row=i + 1, column=4, padx=10, pady=5, sticky="W")
            self.labels_pt.append(label_pt)

        self.fig, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=5, rowspan=17, padx=10, pady=10, sticky="W")

    def calcular_suavizado_doble(self):
        try:
            datos = [float(entry.get()) for entry in self.entry_meses]
            alpha = float(self.entry_alpha.get())
            beta = float(self.entry_beta.get())
            rho = 1  # RHO es siempre 1 en este caso

            # Calcular suavizado exponencial doble
            N = len(datos)
            suavizado_nivel = [datos[0]]
            suavizado_tendencia = [0]
            pronostico = [0]

            # Actualizar etiquetas con resultados para cada mes
            for i in range(1, N):
                At = alpha * datos[i] + (1 - alpha) * (suavizado_nivel[i - 1] + suavizado_tendencia[i - 1])
                Tt = beta * (At - suavizado_nivel[i - 1]) + (1 - beta) * suavizado_tendencia[i - 1]
                
                # Corregir el cálculo del pronóstico para febrero
                Pt = suavizado_nivel[i - 1] + rho * suavizado_tendencia[i - 1] if i > 0 else datos[i]

                suavizado_nivel.append(At)
                suavizado_tendencia.append(Tt)
                pronostico.append(Pt)

                # Actualizar etiquetas con los resultados
                self.labels_at[i - 1]['text'] = f"{calendar.month_name[i + 1]}: A_t={At:.2f}"
                self.labels_tt[i - 1]['text'] = f"T_t={Tt:.2f}"
                self.labels_pt[i - 1]['text'] = f"P_t={Pt:.2f}"

            # Visualizar resultados en la gráfica
            self.ax.clear()
            self.ax.plot(calendar.month_name[1:N], datos[:-1], label='Demanda', marker='o')
            self.ax.plot(calendar.month_name[2:N+1], pronostico[1:], label=f'Pronóstico (alpha={alpha}, beta={beta}, rho={rho})', linestyle='dashed', marker='o')
            self.ax.set_xlabel('Meses')
            self.ax.set_ylabel('Valor')
            self.ax.legend()

            self.canvas.draw()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al calcular el suavizado exponencial doble: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SuavizadoExponencialDobleApp(root)
    root.mainloop()
