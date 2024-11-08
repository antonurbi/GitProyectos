import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_data(inversion_cada_30_dias, dias):
    file_path = 'data.csv'
    data = pd.read_csv(file_path)
    data['datetime'] = pd.to_datetime(data['datetime'], format='%d.%m.%Y %H:%M:%S.%f')
    data = data.sort_values(by='datetime').reset_index(drop=True)
    precios = data['close'].values
    dias_inversion = np.arange(0, len(precios), dias)
    return data, precios, inversion_cada_30_dias, dias_inversion

def simulacion(precios, inversion_cada_30_dias, dias_inversion):
    cantidad_comprada = []
    total_invertido = []
    acumulado_invertido = 0
    unidades_totales = 0

    for dia in dias_inversion:
        precio_actual = precios[dia]
        if precio_actual > 0:  # Asegura que el precio sea válido antes de calcular
            unidades = inversion_cada_30_dias / precio_actual
            unidades_totales += unidades
            acumulado_invertido += inversion_cada_30_dias
            valor_actual = unidades_totales * precio_actual
            cantidad_comprada.append(valor_actual)
            total_invertido.append(acumulado_invertido)
        else:
            cantidad_comprada.append(np.nan)
            total_invertido.append(acumulado_invertido)

    ganancia_perdida = np.array(cantidad_comprada) - np.array(total_invertido)
    return cantidad_comprada, total_invertido, ganancia_perdida

def graficar(data, precios, dias_inversion, cantidad_comprada, total_invertido, ganancia_perdida,simbolo,cantidad,dias):
    
    fig = go.Figure()

    # Trazo para el precio del activo
    fig.add_trace(go.Scatter(
        x=data['datetime'],
        y=precios,
        mode='lines+markers',
        name="Precio del activo ($)",
        line=dict(color='blue'),
        hovertemplate='%{y:.6f}'
    ))

    # Trazo para los días de inversión en el precio del activo
    dias_texto = [f"Día {dia}" for dia in dias_inversion]

    fig.add_trace(go.Scatter(
        x=data['datetime'][dias_inversion],
        y=[precios[dia] for dia in dias_inversion],
        mode='markers',
        name="Días",
        marker=dict(color='red', size=8),
        hovertemplate='%{text}',  # Usamos %{text} para poner el día en el hover
        text=dias_texto  # Pasamos los textos de los días para el hover
    ))

    # Trazo para el valor de la inversión
    fig.add_trace(go.Scatter(
        x=data['datetime'][dias_inversion],
        y=cantidad_comprada,
        mode='lines+markers',
        name="Valor Total",
        line=dict(color='green'),
        yaxis="y2",
        hovertemplate='%{y:.2f}'
    ))

    # Trazo para el total invertido
    fig.add_trace(go.Scatter(
        x=data['datetime'][dias_inversion],
        y=total_invertido,
        mode='lines',
        name="Invertido",
        line=dict(color='orange', dash='dash'),
        yaxis="y2",
        hovertemplate='%{y:.2f}'
    ))

    # Trazo para la ganancia/pérdida neta
    fig.add_trace(go.Scatter(
        x=data['datetime'][dias_inversion],
        y=ganancia_perdida,
        mode='lines+markers',
        name="PnL",
        line=dict(color='purple'),
        yaxis="y2"
    ))
    text_inv = f"Simulación de {simbolo} con {cantidad}€ cada {dias} días, en un intervalo de {len(precios)} días"
    # Diseño de la gráfica con escala ajustada
    fig.update_layout(
        title=dict(
            text=text_inv,
            font=dict(size=20, color="white"),
            x=0.5  # Centra el título
        ),
        xaxis=dict(
            title="Fecha",
            titlefont=dict(size=14, color="lightgray"),
            tickfont=dict(size=12, color="lightgray"),
            gridcolor="gray",  # Color de las líneas de la cuadrícula del eje x
            showgrid=False 
        ),
        yaxis=dict(
            title="Precio del activo ($)",
            titlefont=dict(size=14, color="cyan"),
            tickfont=dict(size=12, color="cyan"),
            tickformat=".6f",  # Muestra más decimales para precios pequeños
            gridcolor="gray",  # Color de las líneas de la cuadrícula del eje y
            zerolinecolor="lightgray",
            range=[min(precios) * 0.9, max(precios) * 1.1],  # Ajusta el rango del eje y a los valores de precios
            showgrid=False, 
            zeroline=False 
        ),
        yaxis2=dict(
            title="Valor de la inversión y total invertido ($)",
            titlefont=dict(size=14, color="lightgreen"),
            tickfont=dict(size=12, color="lightgreen"),
            # anchor="x",
            overlaying="y",
            side="right",
            tickformat=".2f",  # Ajusta los decimales para valores de inversión
            # gridcolor="gray"
            showgrid=False
        ),
        plot_bgcolor="black",   # Fondo negro de la gráfica
        paper_bgcolor="black",  # Fondo negro del área de papel (externo)
        legend=dict(
            font=dict(size=12, color="lightgray"),
            bgcolor="rgba(0, 0, 0, 0)"  # Fondo transparente para la leyenda
        ),
        hovermode="x unified",
        font=dict(
            family="Arial, sans-serif",
            color="white"  # Color de fuente general en blanco
        )
    )
    fig.update_xaxes(fixedrange=False)  # Permite zoom en el eje x
    fig.update_yaxes(fixedrange=False)  # Permite zoom en el eje y


    # Añadir anotaciones en puntos clave (opcional)
    for i, dia in enumerate(dias_inversion):
        fig.add_annotation(
            x=data['datetime'][dia],
            y=ganancia_perdida[i],
            text=f"{ganancia_perdida[i]:.2f}",
            showarrow=True,
            arrowhead=1,
            yshift=10,
            font=dict(color="purple")
        )

    fig.show()

def rendimiento(inversion_cada_30_dias,simbolo,cantidad,dias):
    data, precios, inversion_cada_30_dias, dias_inversion = get_data(inversion_cada_30_dias, dias)
    cantidad_comprada, total_invertido, ganancia_perdida = simulacion(precios, inversion_cada_30_dias, dias_inversion)
    graficar(data, precios, dias_inversion, cantidad_comprada, total_invertido, ganancia_perdida,simbolo,cantidad,dias)
