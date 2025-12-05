from fasthtml.common import *
import pandas as pd

app, rt = fast_app()

# Estilos CSS básicos
dark_css = Style('''
body {
    background: #1a1a1a;
    color: #f3f3f3;
    font-family: Arial, sans-serif;
    margin: 0;
    min-height: 100vh;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
.card {
    background: #2a2a2a;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
.title {
    font-size: 2rem;
    color: #90caf9;
    margin-bottom: 20px;
}
''')

def menu():
    return Nav(
        A('Inicio', href='/', style='margin-right: 20px;'),
        A('Limpio', href='/limpio', style='margin-right: 20px;'),
        A('Análisis', href='/analisis', style='margin-right: 20px;'),
        A('Predicciones', href='/predicciones', style='margin-right: 20px;'),
        style='background: #333; padding: 10px; margin-bottom: 20px;'
    )

@rt('/')
def index():
    return Div(
        dark_css,
        menu(),
        Div(
            H1('RENTOCA: Análisis del Sector Cultural', cls='title'),
            Div(
                P('Proyecto de análisis y predicción del registro RENTOCA.'),
                P('Selecciona una opción del menú arriba.'),
                cls='card'
            ),
            cls='container'
        )
    )

@rt('/limpio')
def limpio():
    return Div(
        dark_css,
        menu(),
        Div(
            H1('Dataset Limpio', cls='title'),
            Div(
                P('Aquí irían los datos del dataset limpio.'),
                cls='card'
            ),
            cls='container'
        )
    )

@rt('/analisis')
def analisis():
    return Div(
        dark_css,
        menu(),
        Div(
            H1('Análisis Estadístico', cls='title'),
            Div(
                P('Aquí irían los gráficos de análisis.'),
                cls='card'
            ),
            cls='container'
        )
    )

@rt('/predicciones')
def predicciones():
    return Div(
        dark_css,
        menu(),
        Div(
            H1('Predicciones con ML', cls='title'),
            Div(
                P('Aquí irían las predicciones del modelo.'),
                cls='card'
            ),
            cls='container'
        )
    )

if __name__ == '__main__':
    serve()
