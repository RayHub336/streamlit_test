import pandas as pd
import scipy.stats
import streamlit as st
import time

# Título de la app
st.header('Lanzar una moneda')

# ---------------------------------------------------------
# 1. GESTIÓN DEL ESTADO (Session State)
# ---------------------------------------------------------
# Streamlit se recarga entero con cada clic. Para que no olvide 
# los datos anteriores, usamos "session_state".
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# ---------------------------------------------------------
# 2. DEFINICIÓN DE FUNCIONES
# ---------------------------------------------------------
def toss_coin(n):
    """
    Simula el lanzamiento de una moneda n veces.
    Retorna la media final de caras (1s).
    """
    # Usamos bernoulli para simular 0s y 1s (cruz y cara)
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    # Iteramos sobre cada lanzamiento para actualizar el gráfico en tiempo real
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        
        # Actualizamos el gráfico con el nuevo dato
        chart.add_rows([mean])
        
        # Pausa para efecto visual (en producción real esto se evita, pero aquí es educativo)
        time.sleep(0.05)

    return mean

# ---------------------------------------------------------
# 3. INTERFAZ DE USUARIO (WIDGETS)
# ---------------------------------------------------------
# Gráfico inicial vacío (inicia en 0.5 que es la probabilidad teórica)
chart = st.line_chart([0.5])

# Slider para elegir número de intentos
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

# Botón de ejecución
start_button = st.button('Ejecutar')

# ---------------------------------------------------------
# 4. LÓGICA DE EJECUCIÓN
# ---------------------------------------------------------
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    
    # Incrementamos el contador de experimentos
    st.session_state['experiment_no'] += 1
    
    # Ejecutamos la función
    mean = toss_coin(number_of_trials)
    
    # Guardamos el resultado en el histórico (session_state)
    new_row = pd.DataFrame(
        data=[[st.session_state['experiment_no'], number_of_trials, mean]],
        columns=['no', 'iteraciones', 'media']
    )
    
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_row],
        axis=0
    )
    
    # Reseteamos el índice para que se vea bonito
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# Mostramos la tabla histórica al final
st.write(st.session_state['df_experiment_results'])