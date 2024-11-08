import plotly.graph_objects as go

# Datos de ejemplo
categories = ['Categoria 1', 'Categoria 2', 'Categoria 3', 'Categoria 4', 'Categoria 5']
values = [4, 3, 2, 5, 4]

# Crear gráfico de radar
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Valores'
))

# Ajustar el diseño
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=False
)

# Mostrar gráfico
fig.show()
