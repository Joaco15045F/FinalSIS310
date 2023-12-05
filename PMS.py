import tkinter as tk
from tkinter import messagebox
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalculadoraPromedioMovil:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Promedio Móvil Simple")

        # Variables para almacenar los errores absolutos, cuadrados y porcentual
        self.errores_absolutos = []
        self.errores_cuadraticos = []
        self.errores_porcentuales = []

        # Configuración de ancho de columnas
        for i in range(9):  # Ajusta el rango según la cantidad de columnas que tengas
            self.root.columnconfigure(i, weight=1)

        self.demandas = [tk.DoubleVar(value=None) for _ in range(12)]
        self.entry_demandas = [tk.Entry(root, textvariable=demanda, font=("Arial", 12), validate="key", validatecommand=(root.register(self.validate_input), '%P')) for demanda in self.demandas]

        self.result_labels = [tk.Label(root, text="", font=("Arial", 12), width=20) for _ in range(12)]
        self.error_labels = [tk.Label(root, text="", font=("Arial", 12), width=20) for _ in range(12)]
        self.errorabs_labels = [tk.Label(root, text="", font=("Arial", 12), width=20) for _ in range(12)]
        self.errorcuadrado_labels = [tk.Label(root, text="", font=("Arial", 12), width=20) for _ in range(12)]
        self.errorporcentual_labels = [tk.Label(root, text="", font=("Arial", 12), width=20) for _ in range(12)]

        # Etiquetas y entradas para los meses y demandas
        for i in range(12):
            mes_label = tk.Label(root, text=calendar.month_abbr[i + 1], font=("Arial", 12))
            mes_label.grid(row=i + 1, column=0, padx=(10, 5), pady=5, sticky="w")

            self.entry_demandas[i].grid(row=i + 1, column=1, padx=(5, 5), pady=5)

            # Posicionar etiquetas para mostrar los pronósticos y errores
            self.result_labels[i].grid(row=i + 1, column=2, padx=(5, 5), pady=5)
            self.error_labels[i].grid(row=i + 1, column=3, padx=(5, 5), pady=5)
            self.errorabs_labels[i].grid(row=i + 1, column=4, padx=(5, 5), pady=5)
            self.errorcuadrado_labels[i].grid(row=i + 1, column=5, padx=(5, 10), pady=5)
            self.errorporcentual_labels[i].grid(row=i + 1, column=6, padx=(10, 10), pady=5)

        # Etiqueta y entrada para el valor de N
        tk.Label(root, text="Valor de N:", font=("Arial", 12)).grid(row=0, column=4, padx=(0, 5), pady=5)
        self.valor_n = tk.Entry(root, font=("Arial", 12))
        self.valor_n.grid(row=0, column=5, padx=(5, 10), pady=5)

        # Botón para calcular pronósticos y errores
        tk.Button(root, text="Calcular Pronósticos y Errores", font=("Arial", 12), command=self.calcular_promedio_y_errores).grid(row=13, column=0, columnspan=9, pady=10)

        # Configuración para la gráfica
        self.fig, self.ax = plt.subplots(figsize=(10, 4))  # Ajusta las dimensiones de la figura aquí
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=14, column=0, columnspan=9, padx=10, pady=10, sticky="nesw")  # Ajusta el rowspan según sea necesario
        self.canvas.draw()


    def validate_input(self, value):
        # Método de validación para permitir solo números
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def plot_grafica(self, demandas, pronosticos, n):
        # Limpiar el eje antes de trazar una nueva gráfica
        self.ax.clear()

        # Trazar la demanda y los pronósticos en el mismo gráfico
        meses = list(range(1, 13))
        self.ax.plot(meses, demandas, label="Demanda", marker='o')
        self.ax.plot(meses[n:], pronosticos, label="Pronósticos", marker='o')

        # Configuraciones adicionales para la gráfica
        self.ax.set_xlabel("Mes")
        self.ax.set_ylabel("Valor")
        self.ax.set_title("Demanda y Pronósticos")
        self.ax.legend()

        # Actualizar la gráfica
        self.canvas.draw()

    def reiniciar_metricas(self):
        # Reiniciar variables para métricas
        self.errores_absolutos = []
        self.errores_cuadraticos = []
        self.errores_porcentuales = []

    def calcular_promedio_y_errores(self):
        try:
            n = int(self.valor_n.get())
            if n > 0:
                if n <= len(self.demandas):
                    # Reiniciar métricas
                    self.reiniciar_metricas()

                    # Borrar pronósticos y errores anteriores
                    for label in self.result_labels:
                        label.config(text="")
                    for label in self.error_labels:
                        label.config(text="")
                    for label in self.errorabs_labels:
                        label.config(text="")
                    for label in self.errorcuadrado_labels:
                        label.config(text="")
                    for label in self.errorporcentual_labels:
                        label.config(text="")

                    # Obtener las demandas actuales
                    demandas_actuales = [float(entry.get()) for entry in self.demandas]

                    # Calcular los promedios móviles y errores y mostrar resultados en etiquetas
                    pronosticos = []
                    for i in range(n, 12):
                        promedio = sum(demandas_actuales[i - n:i]) / n
                        mes = i + 1
                        error = demandas_actuales[i] - promedio
                        errorabs = abs(error)
                        errorcuadrado = error * error
                        errorporcentual = abs(error / demandas_actuales[i]) * 100
                        pronosticos.append(promedio)
                        self.result_labels[i - n].config(text=f"Pronóstico {calendar.month_abbr[i + 1]}: {promedio:.2f}")
                        self.error_labels[i - n].config(text=f"Error {calendar.month_abbr[i + 1]}: {error:.2f}")
                        self.errorabs_labels[i - n].config(text=f"E.Absoluto {calendar.month_abbr[i + 1]}: {errorabs:.2f}")
                        self.errorcuadrado_labels[i - n].config(text=f"E.Cuadrado {calendar.month_abbr[i + 1]}: {errorcuadrado:.2f}")
                        self.errorporcentual_labels[i - n].config(text=f"E.Porcentual {calendar.month_abbr[i + 1]}: {errorporcentual:.2f}%")

                        # Almacenar los errores absolutos, cuadrados y porcentuales
                        self.errores_absolutos.append(errorabs)
                        self.errores_cuadraticos.append(errorcuadrado)
                        self.errores_porcentuales.append(errorporcentual)

                    # Calcular y mostrar el promedio de errores absolutos
                    mad = sum(self.errores_absolutos) / len(self.errores_absolutos)
                    tk.Label(self.root, text=f"MAD: {mad:.2f}", font=("Arial", 12)).grid(row=15, column=1, columnspan=9, pady=10)

                    # Calcular y mostrar el promedio de errores cuadrados
                    mse = sum(self.errores_cuadraticos) / len(self.errores_cuadraticos)
                    tk.Label(self.root, text=f"MSE: {mse:.2f}", font=("Arial", 12)).grid(row=15, column=2, columnspan=9, pady=10)

                    # Calcular y mostrar el promedio de errores porcentuales excluyendo diciembre
                    if n <= 12 and n > 0:
                        made = (sum(self.errores_porcentuales) - self.errores_porcentuales[-1]) / (12-n - 1)
                        tk.Label(self.root, text=f"MADE: {made:.2f}%", font=("Arial", 12)).grid(row=15, column=3, columnspan=9, pady=10)

                    # Trazar la gráfica
                    self.plot_grafica(demandas_actuales, pronosticos, n)

                else:
                    messagebox.showerror("Error", "N no puede ser mayor que el número de meses.")
            else:
                messagebox.showerror("Error", "N debe ser un número positivo.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para N.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")  # Establecer el tamaño de la ventana
    app = CalculadoraPromedioMovil(root)
    root.mainloop()
