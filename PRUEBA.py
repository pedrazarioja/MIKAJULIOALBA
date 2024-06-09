import streamlit as st
import pandas as pd

def obtener_monto():
    monto = st.number_input("Ingrese el monto para el cual quiere realizar el plan de gastos mensual en bolivianos (Bs): ", min_value=0.0, step=0.01)
    return monto

def obtener_porcentaje_ahorro():
    porcentaje = st.selectbox("¿Cuánto quiere ahorrar?", ["0%", "3%", "6%", "9%"])
    return float(porcentaje.strip('%')) / 100

def pregunta_si_no(mensaje):
    respuesta = st.radio(mensaje, ["sí", "no"])
    return respuesta == "sí"

def obtener_gasto_si_no(mensaje):
    if pregunta_si_no(mensaje):
        gasto = st.number_input(f"¿Cuánto paga mensualmente por {mensaje.lower()}?", min_value=0.0, step=0.01)
        return gasto
    else:
        return 0

def seleccionar_categorias():
    categorias = ["ALIMENTACION", "SERVICIOS BASICOS", "TRANSPORTE", "OCIO", "COMUNICACION", "SALUD"]
    seleccionadas = []
    for categoria in categorias:
        if pregunta_si_no(f"¿Tiene gasto en la categoría {categoria}?"):
            seleccionadas.append(categoria)
    return seleccionadas

def prioridad_categorias(seleccionadas):
    prioridades = {}
    for i, categoria in enumerate(seleccionadas):
        prioridad = st.number_input(f"Asignar prioridad a {categoria} (1 para la más importante, {len(seleccionadas)} para la menos importante): ", min_value=1, max_value=len(seleccionadas), step=1, key=categoria)
        prioridades[categoria] = prioridad
    return prioridades

def calcular_porcentajes(prioridades):
    n = len(prioridades)
    porcentaje_categoria = {
        1: {1: 100},
        2: {1: 60, 2: 40},
        3: {1: 45, 2: 30, 3: 25},
        4: {1: 32, 2: 27, 3: 23, 4: 18},
        5: {1: 30, 2: 25, 3: 20, 4: 15, 5: 10},
        6: {1: 26, 2: 22, 3: 19, 4: 15, 5: 11, 6: 7}
    }
    return {categoria: porcentaje_categoria[n][prioridad] / 100 for categoria, prioridad in prioridades.items()}

def calcular_subcategorias(categoria):
    subcategorias = []
    if categoria == "SERVICIOS BASICOS":
        subcategorias = ["LUZ", "AGUA", "GAS"]
    elif categoria == "COMUNICACION":
        subcategorias = ["CREDITO", "INTERNET"]
    
    prioridades = {}
    for subcategoria in subcategorias:
        prioridad = st.number_input(f"Asignar prioridad a {subcategoria} (1 para la más importante, {len(subcategorias)} para la menos importante): ", min_value=1, max_value=len(subcategorias), step=1, key=subcategoria)
        prioridades[subcategoria] = prioridad
    
    n = len(prioridades)
    porcentaje_subcategoria = {
        1: {1: 100},
        2: {1: 60, 2: 40},
        3: {1: 45, 2: 30, 3: 25}
    }
    return {subcategoria: porcentaje_subcategoria[n][prioridad] / 100 for subcategoria, prioridad in prioridades.items()}

def main():
    st.title("Plan de Gastos Mensual")
    
    monto = obtener_monto()
    porcentaje_ahorro = obtener_porcentaje_ahorro()

    alquiler = obtener_gasto_si_no("¿Paga alquiler?")
    deudas = obtener_gasto_si_no("¿Tiene deudas económicas o educativas? Por ejemplo, deudas bancarias o cuotas del colegio/universidad")
    actividades = obtener_gasto_si_no("¿Realiza actividades extracurriculares como gimnasio, danza, ajedrez, etc?")
    
    total_1 = monto - alquiler - deudas - actividades
    total_2 = total_1 * porcentaje_ahorro
    total_final = total_1 - total_2
    ahorro = total_2

    seleccionadas = seleccionar_categorias()
    prioridades = prioridad_categorias(seleccionadas)
    porcentajes = calcular_porcentajes(prioridades)
    
    resultados = {}
    for categoria, porcentaje in porcentajes.items():
        if categoria in ["SERVICIOS BASICOS", "COMUNICACION"]:
            subcategorias = calcular_subcategorias(categoria)
            resultados[categoria] = {subcategoria: total_final * porcentaje * porcentaje_subcategoria for subcategoria, porcentaje_subcategoria in subcategorias.items()}
        else:
            resultados[categoria] = total_final * porcentaje
    
    resultados["AHORRO"] = ahorro
    resultados["ALQUILER"] = alquiler
    resultados["ACTIVIDADES EXTRACURRICULARES"] = actividades
    resultados["DEUDAS"] = deudas
    
    data = []
    for categoria, valor in resultados.items():
        if isinstance(valor, dict):
            for subcategoria, subvalor in valor.items():
                data.append([categoria, subcategoria, subvalor])
        else:
            data.append([categoria, '', valor])
    
    df = pd.DataFrame(data, columns=["Categoría", "Subcategoría", "Monto"])
    st.write("Plan de Gastos Mensual")
    st.dataframe(df)

if __name__ == "__main__":
    main()
