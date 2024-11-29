import json
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from analysis.sentiment_analysis import analyze_sentiment
from visualizations.sentiment_visualization import create_sentiment_graph

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Función para cargar credenciales desde un archivo JSON
def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'twitter': {},
            'facebook': {},
            'instagram': {}
        }

# Función para guardar credenciales en un archivo JSON
def save_credentials(twitter_key, twitter_secret, facebook_key, facebook_secret, instagram_key, instagram_secret):
    credentials = {
        'twitter': {
            'api_key': twitter_key,
            'api_secret': twitter_secret
        },
        'facebook': {
            'api_key': facebook_key,
            'api_secret': facebook_secret
        },
        'instagram': {
            'api_key': instagram_key,
            'api_secret': instagram_secret
        }
    }
    with open('credentials.json', 'w') as f:
        json.dump(credentials, f)

# Cargar credenciales al iniciar la aplicación
credentials = load_credentials()

# Función ficticia para simular la recuperación de publicaciones
def fetch_posts(platform):
    # Aquí iría la lógica para conectarse a la API de la red social y recuperar las publicaciones
    # Retornar una lista de publicaciones simuladas
    return [
        {'date': '3/15/2024, 5:00:00 AM', 'content': 'Excited to announce our new product launch!'},
        {'date': '3/16/2024, 6:00:00 AM', 'content': 'Had a great day at the park!'},
        {'date': '3/17/2024, 7:00:00 AM', 'content': 'Feeling sad about the recent news.'},
        {'date': '3/18/2024, 8:00:00 AM', 'content': 'Can’t wait for the weekend!'},
        # Agrega más publicaciones simuladas según sea necesario
    ]

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Dashboard', children=[
            html.Div([
                html.H1("Análisis de Sentimiento - Dashboard"),
                dcc.Input(id='input-text', type='text', placeholder='Ingresa el texto aquí', style={'width': '100%'}),
                html.Button('Analizar', id='analyze-button', n_clicks=0),
                dcc.Graph(id='sentiment-graph')
            ])
        ]),
        dcc.Tab(label='Twitter', children=[
            html.Div([
                html.H1("Análisis de Sentimiento en Twitter"),
                dcc.Input(id='input-twitter', type='text', placeholder='Ingresa un tweet aquí', style={'width': '100%'}),
                html.Button('Analizar Tweet', id='analyze-twitter-button', n_clicks=0),
                dcc.Graph(id='twitter-sentiment-graph'),
                html.Div(id='posts-list'),
                dcc.Input(id='filter-input', type='text', placeholder='Filtrar publicaciones', style={'width': '100%'}),
                html.Button('Cargar Publicaciones', id='fetch-posts-button', n_clicks=0),
            ])
        ]),
        dcc.Tab(label='Facebook', children=[
            html.Div([
                html.H1("Análisis de Sentimiento en Facebook"),
                dcc.Input(id='input-facebook', type='text', placeholder='Ingresa una publicación aquí', style={'width': '100%'}),
                html.Button('Analizar Publicación', id='analyze-facebook-button', n_clicks=0),
                dcc.Graph(id='facebook-sentiment-graph')
            ])
        ]),
        dcc.Tab(label='Instagram', children=[
            html.Div([
                html.H1("Análisis de Sentimiento en Instagram"),
                dcc.Input(id='input-instagram', type='text', placeholder='Ingresa un comentario aquí', style={'width': '100%'}),
                html.Button('Analizar Comentario', id='analyze-instagram-button', n_clicks=0),
                dcc.Graph(id='instagram-sentiment-graph')
            ])
        ]),
        dcc.Tab(label='Credenciales', children=[
            html.Div([
                html.H1("Credenciales de API"),
                html.Div([
                    html.H2("Twitter"),
                    html.Label("API Key:"),
                    dcc.Input(id='twitter-api-key', type='text ', value=credentials['twitter'].get('api_key', ''), style={'width': '100%'}),
                    html.Label("API Secret:"),
                    dcc.Input(id='twitter-api-secret', type='text', value=credentials['twitter'].get('api_secret', ''), style={'width': '100%'}),
                    html.Button('Guardar Credenciales', id='save-credentials-button', n_clicks=0)
                ]),
                html.Div([
                    html.H2("Facebook"),
                    html.Label("API Key:"),
                    dcc.Input(id='facebook-api-key', type='text', value=credentials['facebook'].get('api_key', ''), style={'width': '100%'}),
                    html.Label("API Secret:"),
                    dcc.Input(id='facebook-api-secret', type='text', value=credentials['facebook'].get('api_secret', ''), style={'width': '100%'}),
                ]),
                html.Div([
                    html.H2("Instagram"),
                    html.Label("API Key:"),
                    dcc.Input(id='instagram-api-key', type='text', value=credentials['instagram'].get('api_key', ''), style={'width': '100%'}),
                    html.Label("API Secret:"),
                    dcc.Input(id='instagram-api-secret', type='text', value=credentials['instagram'].get('api_secret', ''), style={'width': '100%'}),
                ])
            ])
        ])
    ])
])

# Callbacks para manejar la lógica de la aplicación
@app.callback(
    Output('sentiment-graph', 'figure'),
    Input('analyze-button', 'n_clicks'),
    Input('input-text', 'value')
)
def update_sentiment_graph(n_clicks, input_text):
    if n_clicks > 0 and input_text:
        sentiment_score = analyze_sentiment(input_text)
        return create_sentiment_graph(sentiment_score)
    return {}

@app.callback(
    Output('posts-list', 'children'),
    Input('fetch-posts-button', 'n_clicks'),
    Input('filter-input', 'value')
)
def update_posts_list(n_clicks, filter_value):
    if n_clicks > 0:
        posts = fetch_posts('twitter')
        if filter_value:
            posts = [post for post in posts if filter_value.lower() in post['content'].lower()]
        return [html.Div(f"{post['date']}: {post['content']}") for post in posts]
    return []

@app.callback(
    Output('twitter-api-key', 'value'),
    Output('twitter-api-secret', 'value'),
    Output('facebook-api-key', 'value'),
    Output('facebook-api-secret', 'value'),
    Output('instagram-api-key', 'value'),
    Output('instagram-api-secret', 'value'),
    Input('save-credentials-button', 'n_clicks'),
    Input('twitter-api-key', 'value'),
    Input('twitter-api-secret', 'value'),
    Input('facebook-api-key', 'value'),
    Input('facebook-api-secret', 'value'),
    Input('instagram-api-key', 'value'),
    Input('instagram-api-secret', 'value'),
)
def save_credentials_callback(n_clicks, twitter_key, twitter_secret, facebook_key, facebook_secret, instagram_key, instagram_secret):
    if n_clicks > 0:
        save_credentials(twitter_key, twitter_secret, facebook_key, facebook_secret, instagram_key, instagram_secret)
    return twitter_key, twitter_secret, facebook_key, facebook_secret, instagram_key, instagram_secret

if __name__ == '__main__':
    app.run_server(debug=True)