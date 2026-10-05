library(tcltk)

# --- CLASE / LÓGICA DE SIMULACIÓN ---
simular_moneda <- function(total_lanzamientos) {
  # 0 -> Águila, 1 -> Sol
  tiradas <- sample(c("Águila", "Sol"), size = total_lanzamientos, replace = TRUE)
  frecuencias <- table(factor(tiradas, levels = c("Águila", "Sol")))
  
  cant_aguila <- as.numeric(frecuencias["Águila"])
  cant_sol <- as.numeric(frecuencias["Sol"])
  
  esperada <- total_lanzamientos / 2.0
  chi_cuadrada <- ((cant_aguila - esperada)^2 / esperada) + ((cant_sol - esperada)^2 / esperada)
  valor_critico <- 3.841
  
  es_equilibrada <- chi_cuadrada <= valor_critico
  
  return(list(
    aguila = cant_aguila,
    sol = cant_sol,
    chi_cuadrada = chi_cuadrada,
    valor_critico = valor_critico,
    esperada = esperada,
    es_equilibrada = es_equilibrada
  ))
}

# --- INTERFAZ GRÁFICA (tcltk) ---
crear_interfaz_moneda <- function() {
  tt <- tktoplevel(bg = "#f4f6f9")
  tkwm.title(tt, "Simulador de Moneda - Análisis Estadístico (R)")
  tkwm.geometry(tt, "820x520")
  
  txt_tiros_var <- tclVar("500")
  
  # Panel Izquierdo (Tarjeta Blanca)
  panel_izq <- tkframe(tt, bg = "#ffffff", padx = 15, pady = 15, relief = "solid", bd = 1)
  tkgrid(panel_izq, row = 0, column = 0, padx = 15, pady = 15, sticky = "nsew")
  
  lbl_titulo <- tklabel(
    panel_izq, text = "Simulación de Moneda", 
    font = tkfont.create(family = "Segoe UI", size = 13, weight = "bold"),
    fg = "#1e293b", bg = "#ffffff"
  )
  tkpack(lbl_titulo, anchor = "w", pady = c(0, 10))
  
  lbl_tiros <- tklabel(
    panel_izq, text = "Número de Lanzamientos:",
    font = tkfont.create(family = "Segoe UI", size = 9, weight = "bold"),
    fg = "#64748b", bg = "#ffffff"
  )
  tkpack(lbl_tiros, anchor = "w")
  
  ent_tiros <- tkentry(
    panel_izq, textvariable = txt_tiros_var,
    bg = "#f8fafc", fg = "#0f172a", font = tkfont.create(family = "Segoe UI", size = 10)
  )
  tkpack(ent_tiros, fill = "x", pady = c(5, 10))
  
  lbl_consola <- tklabel(
    panel_izq, text = "Resultados Chi-cuadrada:",
    font = tkfont.create(family = "Segoe UI", size = 9, weight = "bold"),
    fg = "#64748b", bg = "#ffffff"
  )
  tkpack(lbl_consola, anchor = "w", pady = c(5, 5))
  
  txt_consola <- tktext(
    panel_izq, bg = "#f8fafc", fg = "#1e293b",
    font = tkfont.create(family = "Consolas", size = 9),
    width = 28, height = 12, relief = "solid", bd = 1
  )
  tkpack(txt_consola, fill = "both", expand = TRUE, pady = c(0, 10))
  
  ejecutar_simulacion <- function() {
    total <- as.numeric(tclvalue(txt_tiros_var))
    
    if (is.na(total) || total <= 0) {
      tkmessageBox(title = "Error", message = "Ingrese un número entero positivo válido.", icon = "error")
      return()
    }
    
    res <- simular_moneda(total)
    dictamen <- if (res$es_equilibrada) "MONEDA JUSTA (Uniforme)" else "MONEDA CARGADA (No uniforme)"
    
    reporte <- paste0(
      "--- PRUEBA CHI-CUADRADA ---\n\n",
      "Lanzamientos:   ", total, "\n",
      "Frec. Esperada: ", round(res$esperada, 1), "\n\n",
      "Obtenido Águila: ", res$aguila, "\n",
      "Obtenido Sol:    ", res$sol, "\n\n",
      "Chi² Calculado: ", round(res$chi_cuadrada, 2), "\n",
      "Chi² Crítico:   ", round(res$valor_critico, 3), "\n\n",
      "RESULTADO:\n", dictamen
    )
    
    tkdelete(txt_consola, "1.0", "end")
    tkinsert(txt_consola, "end", reporte)
    
    # Renderizar gráfico de barras en R Studio
    barplot(
      c(res$aguila, res$sol),
      names.arg = c("Águila", "Sol"),
      col = c("#0d9488", "#0284c7"),
      border = NA,
      main = "Comparativa de Lados Obtenidos",
      col.main = "#1e293b",
      col.axis = "#64748b",
      ylab = "Frecuencia",
      ylim = c(0, max(res$aguila, res$sol) * 1.2),
      las = 1
    )
    grid(nx = NA, ny = NULL, col = "#e2e8f0", lty = "dotted")
  }
  
  btn_simular <- tkbutton(
    panel_izq, text = "Ejecutar Prueba",
    bg = "#0d9488", fg = "#ffffff",
    font = tkfont.create(family = "Segoe UI", size = 10, weight = "bold"),
    command = ejecutar_simulacion
  )
  tkpack(btn_simular, fill = "x", ipady = 4)
}

# Ejecutar la aplicación
crear_interfaz_moneda()