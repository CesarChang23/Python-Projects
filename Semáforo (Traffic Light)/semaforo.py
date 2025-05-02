import tkinter as tk
from tkinter import ttk
import time
import threading

class SemaforoPeatonal:
    def __init__(self, root):
        self.root = root
        self.root.title("Semáforo Peatonal Interactivo")
        
        # Variables de control
        self.estado = "rojo"  # Iniciamos en rojo para que peatones puedan cruzar primero
        self.boton_presionado = False
        self.simulacion_activa = True
        self.tiempo_restante = 0
        self.tiempo_inicio = time.time()
        
        # Tiempos en segundos
        self.tiempo_verde = 30
        self.tiempo_amarillo = 5
        self.tiempo_rojo = 35
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Iniciar control del semáforo
        self.actualizar_semaforo()
        self.actualizar_temporizadores()
        
        # Iniciar hilo de control del semáforo
        self.hilo_semaforo = threading.Thread(target=self.control_semaforo, daemon=True)
        self.hilo_semaforo.start()
    
    def crear_interfaz(self):
        # Configuración de estilo
        style = ttk.Style()
        style.configure('Titulo.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Temporizador.TLabel', font=('Digital-7', 24, 'bold'))
        style.configure('Boton.TButton', font=('Arial', 10, 'bold'), foreground='black')
        style.configure('Estado.TLabel', font=('Arial', 10, 'bold'))
        
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0)
        
        # Semáforo vehicular
        ttk.Label(main_frame, text="SEMÁFORO VEHICULAR", style='Titulo.TLabel').grid(row=0, column=0, pady=5)
        
        self.canvas_semaforo = tk.Canvas(main_frame, width=100, height=300, bg='black', highlightthickness=0)
        self.canvas_semaforo.grid(row=1, column=0, padx=20, pady=5)
        
        # Luces del semáforo vehicular
        self.luz_roja = self.canvas_semaforo.create_oval(25, 50, 75, 100, fill='red', outline='white')
        self.luz_amarilla = self.canvas_semaforo.create_oval(25, 125, 75, 175, fill='gray', outline='white')
        self.luz_verde = self.canvas_semaforo.create_oval(25, 200, 75, 250, fill='gray', outline='white')
        
        # Temporizador vehicular
        self.temporizador_vehicular = ttk.Label(main_frame, text="35", style='Temporizador.TLabel')
        self.temporizador_vehicular.grid(row=2, column=0)
        
        # Semáforo peatonal
        ttk.Label(main_frame, text="SEMÁFORO PEATONAL", style='Titulo.TLabel').grid(row=0, column=1, pady=5)
        
        self.canvas_peatonal = tk.Canvas(main_frame, width=100, height=150, bg='black', highlightthickness=0)
        self.canvas_peatonal.grid(row=1, column=1, padx=20, pady=5)
        
        # Luces peatonales
        self.luz_roja_peaton = self.canvas_peatonal.create_oval(25, 25, 75, 75, fill='gray', outline='white')
        self.luz_verde_peaton = self.canvas_peatonal.create_oval(25, 75, 75, 125, fill='green', outline='white')
        
        # Temporizador peatonal
        self.temporizador_peatonal = ttk.Label(main_frame, text="35", style='Temporizador.TLabel')
        self.temporizador_peatonal.grid(row=2, column=1)
        
        # Botón peatonal
        self.boton = ttk.Button(main_frame, text="PRESIONAR PARA CRUZAR", 
                              command=self.presionar_boton, style='Boton.TButton')
        self.boton.grid(row=3, column=0, columnspan=2, pady=15, ipadx=10, ipady=5)
        
        # Etiqueta de estado
        self.etiqueta_estado = ttk.Label(main_frame, 
                                        text="ESTADO: ROJO - Vehículos detenidos | Peatones CRUZAN", 
                                        style='Estado.TLabel')
        self.etiqueta_estado.grid(row=4, column=0, columnspan=2)
        
        # Botón para salir
        ttk.Button(main_frame, text="SALIR", command=self.cerrar_aplicacion).grid(row=5, column=0, columnspan=2, pady=10)
    
    def actualizar_semaforo(self):
        # Apagar todas las luces vehiculares
        self.canvas_semaforo.itemconfig(self.luz_roja, fill='gray')
        self.canvas_semaforo.itemconfig(self.luz_amarilla, fill='gray')
        self.canvas_semaforo.itemconfig(self.luz_verde, fill='gray')
        
        # Apagar luces peatonales
        self.canvas_peatonal.itemconfig(self.luz_roja_peaton, fill='gray')
        self.canvas_peatonal.itemconfig(self.luz_verde_peaton, fill='gray')
        
        # Actualizar según estado actual
        if self.estado == "rojo":
            # Vehículos detenidos - Peatones pueden cruzar
            self.canvas_semaforo.itemconfig(self.luz_roja, fill='red')
            self.canvas_peatonal.itemconfig(self.luz_verde_peaton, fill='green')
            self.etiqueta_estado.config(text="ESTADO: ROJO - Vehículos detenidos | Peatones CRUZAN")
        elif self.estado == "amarillo":
            # Precaución - Peatones no deben cruzar
            self.canvas_semaforo.itemconfig(self.luz_amarilla, fill='yellow')
            self.canvas_peatonal.itemconfig(self.luz_roja_peaton, fill='red')
            self.etiqueta_estado.config(text="ESTADO: AMARILLO - Precaución | Peatones ESPEREN")
        else:  # verde
            # Vehículos circulan - Peatones esperan
            self.canvas_semaforo.itemconfig(self.luz_verde, fill='green')
            self.canvas_peatonal.itemconfig(self.luz_roja_peaton, fill='red')
            self.etiqueta_estado.config(text="ESTADO: VERDE - Vehículos circulan | Peatones ESPEREN")
    
    def actualizar_temporizadores(self):
        if self.estado == "verde":
            tiempo_total = self.tiempo_verde
        elif self.estado == "amarillo":
            tiempo_total = self.tiempo_amarillo
        else:  # rojo
            tiempo_total = self.tiempo_rojo
        
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.tiempo_restante = max(0, int(tiempo_total - tiempo_transcurrido))
        
        # Actualizar displays
        tiempo_texto = f"{self.tiempo_restante:02d}"
        self.temporizador_vehicular.config(text=tiempo_texto)
        self.temporizador_peatonal.config(text=tiempo_texto)
        
        # Programar próxima actualización
        if self.simulacion_activa:
            self.root.after(200, self.actualizar_temporizadores)
    
    def presionar_boton(self):
        if self.estado == "verde" or self.estado == "amarillo":
            self.boton_presionado = True
            self.boton.config(text="SOLICITUD RECIBIDA!", state='disabled')
            self.root.after(2000, lambda: self.boton.config(text="PRESIONAR PARA CRUZAR", state='normal'))
    
    def control_semaforo(self):
        while self.simulacion_activa:
            # Estado verde
            if self.estado == "verde":
                self.tiempo_inicio = time.time()
                self.actualizar_semaforo()
                
                while time.time() - self.tiempo_inicio < self.tiempo_verde and not self.boton_presionado:
                    time.sleep(0.1)
                
                if self.boton_presionado or time.time() - self.tiempo_inicio >= self.tiempo_verde:
                    self.estado = "amarillo"
                    self.boton_presionado = False
                    self.actualizar_semaforo()
            
            # Estado amarillo
            elif self.estado == "amarillo":
                self.tiempo_inicio = time.time()
                
                while time.time() - self.tiempo_inicio < self.tiempo_amarillo:
                    time.sleep(0.1)
                
                self.estado = "rojo"
                self.actualizar_semaforo()
            
            # Estado rojo
            elif self.estado == "rojo":
                self.tiempo_inicio = time.time()
                
                while time.time() - self.tiempo_inicio < self.tiempo_rojo:
                    time.sleep(0.1)
                    if self.boton_presionado:
                        break  # Salir anticipadamente si se presionó el botón
                
                self.estado = "verde"
                self.boton_presionado = False
                self.actualizar_semaforo()
    
    def cerrar_aplicacion(self):
        self.simulacion_activa = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SemaforoPeatonal(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()