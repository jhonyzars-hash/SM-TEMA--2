import random
import tkinter as tk
from tkinter import ttk, messagebox


class Dado:

    def __init__(self, total_tiros: int):
        self.total_tiros = total_tiros
        self.frecuencias = [0] * 6
        self.chi_cuadrada = 0.0
        self.valor_critico = 11.07

    def simular(self):
        for _ in range(self.total_tiros):
            resultado = random.randint(0, 5)
            self.frecuencias[resultado] += 1
        self._calcular_chi_cuadrada()

    def _calcular_chi_cuadrada(self):
        esperada = self.total_tiros / 6.0
        self.chi_cuadrada = sum(
            ((obs - esperada) ** 2) / esperada for obs in self.frecuencias
        )

    def es_dado_justo(self) -> bool:
        return self.chi_cuadrada <= self.valor_critico


class AppDado(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Simulador de Dado - Análisis Estadístico")
        self.geometry("820x500")
        self.configure(bg="#f4f6f9")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel Izquierdo (Tarjeta Blanca)
        self.panel_izq = tk.Frame(
            self,
            bg="#ffffff",
            padx=20,
            pady=20,
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        self.panel_izq.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        lbl_titulo = tk.Label(
            self.panel_izq,
            text="Simulación de Dado",
            font=("Segoe UI", 14, "bold"),
            fg="#1e293b",
            bg="#ffffff",
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        lbl_tiros = tk.Label(
            self.panel_izq,
            text="Número de Lanzamientos:",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#ffffff",
        )
        lbl_tiros.pack(anchor="w")

        self.txt_tiros = tk.Entry(
            self.panel_izq,
            bg="#f8fafc",
            fg="#0f172a",
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        self.txt_tiros.insert(0, "600")
        self.txt_tiros.pack(fill="x", pady=(5, 15), ipady=4)

        btn_simular = tk.Button(
            self.panel_izq,
            text="Ejecutar Prueba",
            bg="#2563eb",
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.on_simular_click,
        )
        btn_simular.pack(fill="x", pady=(0, 15), ipady=5)

        lbl_consola = tk.Label(
            self.panel_izq,
            text="Resultados Chi-cuadrada:",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#ffffff",
        )
        lbl_consola.pack(anchor="w", pady=(5, 5))

        self.txt_consola = tk.Text(
            self.panel_izq,
            bg="#f8fafc",
            fg="#1e293b",
            font=("Consolas", 9),
            width=28,
            height=13,
            relief="solid",
            bd=1,
        )
        self.txt_consola.pack(fill="both", expand=True)

        # Panel Derecho (Gráfica Tarjeta Blanca)
        self.panel_der = tk.Frame(
            self,
            bg="#ffffff",
            padx=20,
            pady=20,
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        self.panel_der.grid(
            row=0, column=1, padx=(0, 20), pady=20, sticky="nsew"
        )

        lbl_grafica = tk.Label(
            self.panel_der,
            text="Distribución de Frecuencias Observadas",
            font=("Segoe UI", 12, "bold"),
            fg="#1e293b",
            bg="#ffffff",
        )
        lbl_grafica.pack(pady=(0, 15))

        self.canvas = tk.Canvas(self.panel_der, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_grafica([0] * 6)

    def dibujar_grafica(self, frecuencias):
        self.canvas.delete("all")

        ancho = self.canvas.winfo_width() or 450
        alto = self.canvas.winfo_height() or 350

        max_frecuencia = max(frecuencias) if max(frecuencias) > 0 else 100
        padding_x = 40
        padding_y = 40

        ancho_util = ancho - (2 * padding_x)
        alto_util = alto - (2 * padding_y)

        num_barras = 6
        ancho_barra = ancho_util / (num_barras * 1.5)
        espacio = ancho_barra * 0.5

        # Línea de Eje X
        self.canvas.create_line(
            padding_x,
            alto - padding_y,
            ancho - padding_x,
            alto - padding_y,
            fill="#cbd5e1",
            width=2,
        )

        for i in range(num_barras):
            val = frecuencias[i]
            altura_barra = (val / max_frecuencia) * alto_util

            x0 = padding_x + (i * (ancho_barra + espacio)) + (espacio / 2)
            y0 = (alto - padding_y) - altura_barra
            x1 = x0 + ancho_barra
            y1 = alto - padding_y

            # Dibujar barra azul claro corporativo
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#3b82f6", outline=""
            )

            # Texto sobre la barra
            self.canvas.create_text(
                (x0 + x1) / 2,
                y0 - 12,
                text=str(val),
                fill="#1e293b",
                font=("Segoe UI", 9, "bold"),
            )

            # Etiqueta en eje X
            self.canvas.create_text(
                (x0 + x1) / 2,
                alto - padding_y + 18,
                text=f"Cara {i+1}",
                fill="#64748b",
                font=("Segoe UI", 9),
            )

    def on_simular_click(self):
        try:
            total = int(self.txt_tiros.get())
            if total <= 0:
                raise ValueError

            dado = Dado(total)
            dado.simular()

            esperada = total / 6.0
            dictamen = (
                "DADO JUSTO (Uniforme)"
                if dado.es_dado_justo()
                else "DADO CARGADO (No uniforme)"
            )

            reporte = (
                f"--- PRUEBA CHI-CUADRADA ---\n\n"
                f"Tiros totales: {total}\n"
                f"Frec. Esperada: {esperada:.1f}\n\n"
                f"Chi² Calculado: {dado.chi_cuadrada:.2f}\n"
                f"Chi² Crítico:   {dado.valor_critico:.2f}\n\n"
                f"RESULTADO:\n{dictamen}"
            )

            self.txt_consola.delete("1.0", tk.END)
            self.txt_consola.insert(tk.END, reporte)

            self.dibujar_grafica(dado.frecuencias)

        except ValueError:
            messagebox.showerror(
                "Error", "Ingrese un número entero positivo válido."
            )


if __name__ == "__main__":
    app = AppDado()
    app.mainloop()