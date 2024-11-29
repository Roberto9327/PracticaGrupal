import plotly.graph_objects as go

def create_sentiment_graph(sentiment):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['TextBlob', 'VADER'],
        y=[sentiment['textblob'], sentiment['vader']],
        marker_color=['blue', 'orange']
    ))
    fig.update_layout(title='Análisis de Sentimiento',
                      xaxis_title='Método',
                      yaxis_title='Puntuación de Sentimiento')
    return fig