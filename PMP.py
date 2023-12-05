import tkinter as tk
from tkinter import messagebox, ttk
import calendar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PromedioMovilPonderadoApp:
    def __init__(self, root):
        # Inicialización de la aplicación
        self.root = root
        self.root.title("Calculadora Promedio Móvil Ponderado")

        # Variables para almacenar los errores absolutos, cuadrados y porcentual
        self.errores_absolutos = []
        self.errores_cuadraticos = []
        self.errores_porcentuales = []

        # Configuración de ancho de columnas
        for i in range(20):  # Ajusta el rango según la cantidad de columnas que tengas
            self.root.columnconfigure(i, weight=1)

        self.demandas = [tk.DoubleVar(value=None) for _ in range(12)]
        self.entry_meses = [ttk.Entry(root) for _ in range(12)]
        self.entry_pesos = [ttk.Entry(root, state=tk.DISABLED) for _ in range(11)]

        # Interfaz para ingresar datos mensuales
        for i, mes in enumerate(calendar.month_name[1:]):  # Ignorar el mes 0
            label_mes = ttk.Label(root, text=f"{mes}:", font=("Arial", 12))
            label_mes.grid(row=i + 1, column=0, padx=10, pady=5, sticky="W")
            self.entry_meses[i].grid(row=i + 1, column=1, padx=5, pady=5, sticky="W")

        # Interfaz para ingresar el valor de n
        self.label_valor_n = ttk.Label(root, text="Valor de n (1-11):", font=("Arial", 12))
        self.label_valor_n.grid(row=32, column=0, padx=10, pady=5, sticky="W")
        self.entry_valor_n = ttk.Entry(root)
        self.entry_valor_n.grid(row=32, column=1, padx=5, pady=5, sticky="W")
        self.entry_valor_n.bind('<FocusOut>', self.actualizar_interfaz)

        # Inicializar celdas de pesos (se desactivan inicialmente)
        self.label_pesos = ttk.Label(root, text="Pesos:", font=("Arial", 12))
        self.label_pesos.grid(row=33, column=0, padx=10, pady=5, sticky="W")
        for i, entry_peso in enumerate(self.entry_pesos):
            entry_peso.grid(row=34 + i, column=1, padx=5, pady=5, sticky="W")

        # Botón para calcular el promedio móvil ponderado
        tk.Button(root, text="Calcular Promedio Móvil Ponderado", font=("Arial", 12), command=self.calcular_promedio_ponderado).grid(row=16, column=0, columnspan=3, pady=20)

        # Configuración para la gráfica
        self.fig, self.ax = plt.subplots(figsize=(12, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=15, column=7, columnspan=8, rowspan=50, padx=10, pady=10, sticky="S")

    def actualizar_interfaz(self, event):
        # Esta función se llama cuando el valor de n cambia para habilitar/deshabilitar las celdas de pesos
        try:
            n = int(self.entry_valor_n.get())
            if n < 1 or n > 11:
                tk.messagebox.showerror("Error", "El valor de n debe estar entre 1 y 11.")
                for entry_peso in self.entry_pesos:
                    entry_peso.configure(state=tk.DISABLED)
            else:
                for i, entry_peso in enumerate(self.entry_pesos):
                    if i < n:
                        entry_peso.configure(state=tk.NORMAL)
                    else:
                        entry_peso.configure(state=tk.DISABLED)
        except ValueError:
            pass

    def calcular_promedio_ponderado(self):
        try:
            # Obtener datos ingresados por el usuario
            datos = [float(entry.get()) for entry in self.entry_meses]
            n = int(self.entry_valor_n.get())

            # Crear una lista de pesos dinámicamente basada en el valor de n
            pesos = [float(entry_peso.get()) for entry_peso in self.entry_pesos[:n]]

            # Calcular pronósticos y errores a partir del mes n+1
            pronosticos = []
            errores = []
            errores_cuadraticos = []
            errores_porcentuales = []
            for i in range(n, 12):
                pronostico_i = sum(p * datos[i-j] for j, p in enumerate(pesos, start=1))
                pronosticos.append(pronostico_i)

                # Calcular errores
                error_i = datos[i] - pronostico_i
                error_cuadratico_i = error_i ** 2
                error_porcentual_i = abs(error_i / datos[i]) * 100

                # Almacenar errores
                errores.append(error_i)
                errores_cuadraticos.append(error_cuadratico_i)
                errores_porcentuales.append(error_porcentual_i)
           

                # Mostrar resultados en la interfaz
                tk.Label(self.root, text=f"Pronóstico {calendar.month_abbr[i + 1]}: {pronostico_i:.2f}", font=("Arial", 12)).grid(row=i + 1, column=2, padx=(5, 5), pady=5)
                tk.Label(self.root, text=f"Error {calendar.month_abbr[i + 1]}: {error_i:.2f}", font=("Arial", 12)).grid(row=i + 1, column=7, padx=(5, 5), pady=5)
                tk.Label(self.root, text=f"E.Cuadrado {calendar.month_abbr[i + 1]}: {error_cuadratico_i:.2f}", font=("Arial", 12)).grid(row=i + 1, column=8, padx=(5, 5), pady=5)
                tk.Label(self.root, text=f"E.Porcentual {calendar.month_abbr[i + 1]}: {error_porcentual_i:.2f}%", font=("Arial", 12)).grid(row=i + 1, column=9, padx=(5, 5), pady=5)

            # Visualizar resultados en la gráfica
            self.ax.clear()
            self.ax.plot(calendar.month_name[1:], datos, label='Demanda', marker='o')
            self.ax.plot(calendar.month_name[n+1:], pronosticos, label=f'Pronósticos', linestyle='dashed', marker='o')
            self.ax.set_xlabel('Meses')
            self.ax.set_ylabel('Valor')
            self.ax.legend()
            self.ax.set_xticklabels(calendar.month_name[1:], rotation=45, ha='right')  # Alinea los nombres de los meses

            self.canvas.draw()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al calcular el promedio móvil ponderado: {str(e)}")

# Inicializar la aplicación si se ejecuta como script principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PromedioMovilPonderadoApp(root)
    root.mainloop()
