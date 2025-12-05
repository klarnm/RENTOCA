from fasthtml.common import *
import pandas as pd
from datetime import datetime, timedelta


# Inicialización de la aplicación FastHTML
# - `app, rt = fast_app()` crea la aplicación y el decorador `@rt` para definir rutas
app, rt = fast_app()

# Credenciales de demo (sin BD)
DEMO_CREDENTIALS = {
    'admin': 'admin123',
    'user': 'user123',
    'guest': 'guest'
}

# Almacenar sesiones en memoria (diccionario simple)
active_sessions = {}

# Estilos CSS modernos en modo oscuro
dark_css = Style('''
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
body {
    background: linear-gradient(135deg, #23272f 0%, #6a4cff 100%, #ff6a88 100%);
    color: #f3f3f3;
    font-family: 'Poppins', 'Inter', 'Roboto', 'Arial', sans-serif;
    margin: 0;
    min-height: 100vh;
}
.main-content {
    width: 100%;
    min-height: 100vh;
    margin: 0 auto;
    padding: 0 24px;
    background: none;
    display: flex;
    flex-direction: column;
    gap: 32px;
    align-items: center;
    box-sizing: border-box;
}
.cards-row {
    display: flex;
    flex-direction: row;
    gap: 32px;
    width: 100%;
    max-width: 1400px;
    justify-content: center;
    align-items: stretch;
    margin: 0 auto;
    padding: 0 24px;
    box-sizing: border-box;
}
.card {
    background: rgba(40,44,52,0.96);
    border-radius: 20px;
    box-shadow: 0 4px 24px #0005;
    padding: 48px 36px;
    margin-bottom: 0;
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    position: relative;
    align-items: stretch;
    box-sizing: border-box;
}
.card-large {
    background: rgba(40,44,52,0.96);
    border-radius: 20px;
    box-shadow: 0 4px 24px #0005;
    padding: 48px 36px;
    margin-bottom: 0;
    width: 100%;
    max-width: 1200px;
    min-height: 40vh;
    display: flex;
    flex-direction: column;
    gap: 24px;
    position: relative;
    align-items: stretch;
    overflow-x: auto;
    overflow-y: auto;
    margin-left: auto;
    margin-right: auto;
    box-sizing: border-box;
}
.card-title {
    font-size: 2.6rem;
    font-weight: 700;
    margin-bottom: 18px;
    color: #90caf9;
    letter-spacing: 1px;
}
.card-content {
    font-size: 1.35rem;
    color: #e3e3e3;
}
.card-list {
    margin-bottom: 0;
    font-size: 1.2rem;
}
.card-list li {
    margin-bottom: 10px;
    font-size: 1.1rem;
}
.card-list ul {
    margin-left: 18px;
}
.card-dataset {
    margin-top: 12px;
    width: 100%;
    overflow-x: auto;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    background: rgba(35,39,47,0.95);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px #0002;
    font-size: 1.25rem;
}
.table-header {
    background: #374151;
    color: #90caf9;
    font-weight: bold;
    padding: 18px;
    border-bottom: 2px solid #90caf9;
    font-size: 1.3rem;
}
.table-cell {
    padding: 16px 18px;
    border-bottom: 1px solid #374151;
    vertical-align: top;
    word-break: break-word;
    font-size: 1.15rem;
}
.styled-table tr:nth-child(even) {
    background: #2c313a;
}
.styled-table tr:hover {
    background: #3b4252;
}
.fade-in-title {
    opacity: 0;
    animation: fadeIn 1.2s ease-in forwards;
    animation-delay: 0.3s;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-align: left;
    margin-bottom: 24px;
    color: #90caf9;
    text-shadow: 0 2px 16px #0006;
}
.fade-in-text {
    opacity: 0;
    animation: fadeIn 1.2s ease-in forwards;
    animation-delay: 0.7s;
    font-size: 1.25rem;
    color: #e3e3e3;
    margin-bottom: 18px;
    line-height: 1.6;
}
.main-title {
    font-size: 3.2rem;
    font-weight: 700;
    color: #90caf9;
    letter-spacing: 2px;
    margin-bottom: 38px;
    margin-left: 12px;
    text-shadow: 0 2px 16px #0006;
    text-align: left;
    opacity: 0;
    animation: fadeIn 1.2s ease-in forwards;
    animation-delay: 0.1s;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}
.menu-container {
    width: 100%;
    background: transparent;
    padding: 0;
}
.menu-bar {
    display: flex;
    gap: 32px;
    padding: 24px 32px 0 32px;
    font-size: 1.2rem;
}
.menu-link {
    color: #90caf9;
    text-decoration: none;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 8px;
    transition: background 0.2s, color 0.2s;
}
.menu-link:hover {
    background: #374151;
    color: #fff;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 24px;
    background: rgba(35,39,47,0.95);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px #0002;
}
.table-header {
    background: #374151;
    color: #90caf9;
    font-weight: bold;
    padding: 12px;
    border-bottom: 2px solid #90caf9;
}
.table-cell {
    padding: 10px 12px;
    border-bottom: 1px solid #374151;
    vertical-align: top;
    word-break: break-word;
}
.styled-table tr:nth-child(even) {
    background: #2c313a;
}
.styled-table tr:hover {
    background: #3b4252;
}
.fade-in-title {
    opacity: 0;
    animation: fadeIn 1.2s ease-in forwards;
    animation-delay: 0.3s;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-align: center;
    margin-bottom: 32px;
    color: #90caf9;
    text-shadow: 0 2px 16px #0006;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
}
.login-card {
    background: rgba(40,44,52,0.98);
    border-radius: 20px;
    box-shadow: 0 8px 32px #0008;
    padding: 60px 50px;
    width: 100%;
    max-width: 450px;
    display: flex;
    flex-direction: column;
    gap: 24px;
}
.login-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #90caf9;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 1px;
}
.login-subtitle {
    font-size: 1.1rem;
    color: #a0a0a0;
    text-align: center;
    margin-bottom: 24px;
}
.login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.form-label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e3e3e3;
}
.form-input {
    padding: 14px 16px;
    border: 2px solid #374151;
    border-radius: 10px;
    background: rgba(30,34,42,0.95);
    color: #e3e3e3;
    font-size: 1.1rem;
    font-family: 'Poppins', sans-serif;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.form-input:focus {
    outline: none;
    border-color: #90caf9;
    box-shadow: 0 0 12px #90caf933;
}
.login-btn {
    padding: 14px 20px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(135deg, #90caf9 0%, #6a4cff 100%);
    color: #fff;
    font-size: 1.2rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 12px;
}
.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px #90caf955;
}
.login-btn:active {
    transform: translateY(0);
}
.login-error {
    background: rgba(255, 106, 136, 0.2);
    border-left: 4px solid #ff6a88;
    padding: 12px 16px;
    border-radius: 8px;
    color: #ff9bb5;
    font-size: 1rem;
    margin-bottom: 12px;
    text-align: center;
}
.login-footer {
    text-align: center;
    color: #a0a0a0;
    font-size: 0.95rem;
    margin-top: 12px;
}
''')


# Menú principal de la aplicación
# - `menu(username)` devuelve la barra de navegación.
# - Si `username` está presente muestra un enlace de logout con el nombre.
def menu(username=None):
    # Renderiza los links principales y, opcionalmente, el logout
    return Div(
        Div(
            A('RETOCA original', href='/', cls='menu-link'),
            A('RETOCA limpio', href='/limpio', cls='menu-link'),
            A('Análisis estadístico', href='/analisis', cls='menu-link'),
            A('Predicciones con ML', href='/predicciones', cls='menu-link'),
            username and A(f'Logout ({username})', href='/logout', cls='menu-link', style='margin-left: auto; color: #ff6a88;') or '',
            cls='menu-bar'
        ),
        cls='menu-container'
    )

def check_session(request):
    """Verifica si el usuario tiene una sesión activa"""
    session_id = request.cookies.get('session_id')
    if session_id and session_id in active_sessions:
        session_data = active_sessions[session_id]
        if session_data['expires'] > datetime.now():
            return session_data['username']
    return None

def create_session(username):
    """Crea una nueva sesión"""
    import secrets
    session_id = secrets.token_hex(16)
    active_sessions[session_id] = {
        'username': username,
        'expires': datetime.now() + timedelta(hours=24)
    }
    return session_id


def truncate(val, maxlen=32):
    val = str(val)
    return val if len(val) <= maxlen else val[:maxlen] + '...'


# Ruta de predicciones con ML
# - Carga datos, entrena modelo (demo) y muestra una tabla con predicciones.
# - La lógica está simplificada para mostrar comportamiento; no es producción.
@rt('/predicciones')
def predicciones(request):
    # Verificar sesión
    username = check_session(request)
    if not username:
        return RedirectResponse(url='/login', status_code=303)
    
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    csv_path = 'data/rentoca_limpio.csv'
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip', encoding='latin1', low_memory=False)
    except Exception as e:
        return Div(
            dark_css,
            menu(),
            Div(
                Div('Predicciones con machine learning', cls='main-title'),
                Div(f'Error al leer el CSV: {e}', cls='card'),
                cls='main-content'
            )
        )

    # Explicación teórica
    card_teoria = Div(
        Div('¿Qué tipo de Machine Learning se usa aquí?', cls='card-title', style='text-align:center;'),
        Div(
            P('Se utiliza un modelo de clasificación supervisada binaria, específicamente un Árbol de Decisión (DecisionTreeClassifier) de scikit-learn.'),
            P('La tarea es predecir si un trabajador cultural es FORMAL (registrado en SUNAT) o INFORMAL (no registrado).'),
            P('Clasificación FORMAL: Trabajadores que tienen algún tipo de registro (como persona natural RUC/RUS/RES, o como persona jurídica).'),
            P('Clasificación INFORMAL: Trabajadores que no están registrados (sin RUC ni registro formal).'),
            P('Las variables seleccionadas incluyen: tipo_registro, dirección_principal, nivel_educat, sector, perfil, ocupación, frecuencia de ingreso, horas trabajadas, categoría laboral e ingreso.'),
            P('El modelo aprende patrones en los datos históricos (51.67% informal, 44.29% formal en los datos reales) para estimar la probabilidad de formalidad en nuevos casos.'),
            cls='card-content',
            style='text-align:left;max-width:900px;margin:auto;'
        ),
        cls='card fade-in-title',
        style='margin:auto;'
    )

    try:
        # Variables para el modelo
        # - `target` es la columna objetivo original del dataset.
        # - `features` son las variables que usaremos como predictors (selección manual).
        target = 'p1_sunat'
        features = ['tipo_registro', 'direccion_principal', 'nivel_educat', 'p1_sector', 'p1_perfil', 'p1_ocupacion_f1', 'frec_ingreso', 'p1_horas', 'p1_cat_lab', 'p1_ing']
        # Filtrar features que realmente existen en el CSV (por compatibilidad)
        features = [col for col in features if col in df.columns]
        if target not in df.columns or not features:
            return Div(
                dark_css,
                menu(),
                Div(
                    Div('Predicciones con machine learning', cls='main-title'),
                    card_teoria,
                    Div('No se encuentran las columnas necesarias para el modelo.', cls='card'),
                    cls='main-content'
                )
            )
        
        # 1) Seleccionar registros con target definido y rellenar nulos secundarios
        #    (solo eliminamos filas sin target; los demás nulos se codifican como 'Desconocido')
        data = df[features + [target]].dropna(subset=[target])
        data = data.fillna('Desconocido')

        # 2) Convertir la variable objetivo original a BINARIA
        #    - Queremos predecir FORMAL (1) vs INFORMAL (0)
        #    - Dado que el CSV tiene problemas de encoding, buscamos palabras clave
        def clasificar_formalidad(valor):
            valor_str = str(valor).upper()
            # Si contiene 'NO EST' lo consideramos Informal (no registrado)
            if 'NO EST' in valor_str:
                return 0
            # Si menciona 'PERSONA' o 'JURIDICA' lo consideramos Formal
            elif 'PERSONA' in valor_str or 'JURIDICA' in valor_str:
                return 1
            # Por defecto, marcar como informal (conservador)
            return 0

        data['formalidad_binaria'] = data[target].apply(clasificar_formalidad)

        # 3) Preparar matriz X y vector y
        #    Convertimos todo a string porque hay columnas mixtas; luego codificaremos.
        X = data[features].astype(str)
        y = data['formalidad_binaria'].astype(int)

        # 4) Codificar variables categóricas con LabelEncoder (simple y reproducible)
        #    Guardamos los encoders en `encoders` por si queremos decodificar después.
        encoders = {}
        for col in features:
            enc = LabelEncoder()
            X[col] = enc.fit_transform(X[col])
            encoders[col] = enc

        # 5) Dividir en entrenamiento / test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 6) Entrenar un árbol de decisión sencillo (máx depth=4 para evitar overfitting excesivo)
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        clf.fit(X_train, y_train)

        # 7) Evaluación rápida: accuracy en test (solo referencia básica)
        y_pred = clf.predict(X_test)
        acc = (y_pred == y_test).mean()

        # 8) Hacer predicciones sobre una muestra limitada (evitar render lento en la web)
        muestra = X.head(200)
        pred_formal = clf.predict(muestra)
        
        # Crear tabla con predicciones decodificadas
        tabla_rows = []
        for (idx, row), pred in zip(muestra.iterrows(), pred_formal):
            formal_text = 'Formal (Registrado en SUNAT)' if pred == 1 else 'Informal (No registrado)'
            tabla_rows.append(
                Tr(
                    *[Td(str(row[col]), cls='table-cell') for col in features],
                    Td(formal_text, cls='table-cell', style='color: #4caf50;' if pred == 1 else 'color: #ff6a88;')
                )
            )
        
        muestra_tabla = Table(
            Thead(
                Tr(
                    *[Th(col.replace('_', ' ').capitalize(), cls='table-header') for col in features],
                    Th('Formalidad predicha (SUNAT)', cls='table-header')
                )
            ),
            *tabla_rows,
            cls='styled-table'
        )

        card_pred = Div(
            Div('Predicción de formalidad (SUNAT) usando árbol de decisión', cls='card-title', style='text-align:center;'),
            Div(
                P(f'Precisión del modelo en test: {acc:.2%}'),
                P(f'Se muestran predicciones para los primeros 200 registros del dataset (Total: {len(X)} registros).'),
                cls='card-content',
                style='margin-bottom:18px;text-align:center;'
            ),
            cls='card fade-in-title',
            style='margin:auto;'
        )

        card_tabla = Div(
            muestra_tabla,
            cls='card-large fade-in-title',
            style='margin:auto;'
        )

        grid = Div(
            card_teoria,
            card_pred,
            style='display:grid;grid-template-columns:1fr 1fr;gap:48px;margin-bottom:48px;'
        )

        # RESUMEN CON ESTADÍSTICAS Y GRÁFICOS
        # Calcular distribución de predicciones
        pred_counts = pd.Series(pred_formal).value_counts()
        total_pred = len(pred_formal)
        
        # Usar imagen generada por analisis_descriptivo.py
        chart_img = Img(src='static/ml_distribucion_predicciones.png', 
                       style='width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0 2px 12px #0003;')

        # Calcular estadísticas correctas
        n_formal_real = (y == 1).sum()
        n_informal_real = (y == 0).sum()
        pct_formal_real = (n_formal_real / len(y)) * 100 if len(y) > 0 else 0
        pct_informal_real = (n_informal_real / len(y)) * 100 if len(y) > 0 else 0
        
        n_formal_pred = (pred_formal == 1).sum()
        n_informal_pred = (pred_formal == 0).sum()
        
        # Tarjetas de métricas
        metrics_cards = Div(
            Div(
                Div(f'{pct_formal_real:.1f}%', style='font-size: 2.5rem; color: #4caf50; font-weight: bold;'),
                Div('Formal (Real)', style='color: #e3e3e3; margin-top: 10px;'),
                Div(f'{n_formal_real} registros', style='color: #a0a0a0; font-size: 0.9rem;'),
                cls='card',
                style='text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;'
            ),
            Div(
                Div(f'{pct_informal_real:.1f}%', style='font-size: 2.5rem; color: #ff6a88; font-weight: bold;'),
                Div('Informal (Real)', style='color: #e3e3e3; margin-top: 10px;'),
                Div(f'{n_informal_real} registros', style='color: #a0a0a0; font-size: 0.9rem;'),
                cls='card',
                style='text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;'
            ),
            Div(
                Div(f'{(n_formal_pred/len(pred_formal)*100):.1f}%', style='font-size: 2.5rem; color: #90caf9; font-weight: bold;'),
                Div('Formal (Predicción)', style='color: #e3e3e3; margin-top: 10px;'),
                Div(f'{n_formal_pred} predicciones', style='color: #a0a0a0; font-size: 0.9rem;'),
                cls='card',
                style='text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;'
            ),
            Div(
                Div(f'{acc:.1%}', style='font-size: 2.5rem; color: #ffc107; font-weight: bold;'),
                Div('Precisión del Modelo', style='color: #e3e3e3; margin-top: 10px;'),
                Div(f'en {len(X_test)} muestras', style='color: #a0a0a0; font-size: 0.9rem;'),
                cls='card',
                style='text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;'
            ),
            style='display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 48px; max-width: 800px; margin-left: auto; margin-right: auto; width: 100%; padding: 0 24px; box-sizing: border-box;'
        )

        # Tarjeta de resumen
        card_resumen = Div(
            Div('Resumen del Modelo', cls='card-title', style='text-align:center;'),
            Div(
                chart_img,
                style='display: flex; justify-content: center; align-items: center; margin: 30px 0; width: 100%;'
            ),
            Div(
                Ul(
                    Li(f'Algoritmo: Árbol de Decisión (DecisionTreeClassifier)'),
                    Li(f'Profundidad máxima: 4 niveles'),
                    Li(f'Variables independientes: {len(features)}'),
                    Li(f'Variable objetivo: {target} → Formalidad (Formal vs Informal)'),
                    Li(f'Registros de entrenamiento: {len(X_train)}'),
                    Li(f'Registros de test: {len(X_test)}'),
                    Li(f'Precisión alcanzada: {acc:.2%}'),
                    Li(f'Clases en datos reales: 51.67% Informal, 44.29% Formal, 4.04% Otra'),
                    Li(f'Nota: El desequilibrio de clases puede afectar la distribución de predicciones'),
                    style='font-size: 1.1rem; line-height: 1.8;'
                ),
                style='text-align: left; max-width: 800px; margin: auto;'
            ),
            cls='card-large fade-in-title',
            style='margin: auto; margin-top: 48px;'
        )

        # Tabla abajo, ocupando todo el ancho
        return Div(
            dark_css,
            menu(username),
            Div(
                Div('Predicciones con machine learning', cls='main-title', style='text-align:center;'),
                grid,
                Div(
                    card_tabla,
                    style='width:100%;max-width:100%;display:block;overflow-x:auto;'
                ),
                metrics_cards,
                card_resumen,
                cls='main-content',
                style='align-items:center;justify-content:center;display:flex;flex-direction:column;gap:48px;width:100%;'
            )
        )
    except Exception as e:
        return Div(
            dark_css,
            menu(),
            Div(
                Div('Predicciones con machine learning', cls='main-title'),
                card_teoria,
                Div(f'Error durante el procesamiento del modelo: {str(e)}', cls='card'),
                cls='main-content'
            )
        )

# Ruta /analisis: pestaña vacía para análisis estadístico
@rt('/analisis')
def analisis(request):
    # Verificar sesión
    username = check_session(request)
    if not username:
        return RedirectResponse(url='/login', status_code=303)
    
    return Div(
        dark_css,
        menu(username),
        Div(
            Div('Análisis estadístico', cls='main-title'),
            # 1. Boxenplot
            Div(
                Div(
                    B('Modelo matemático usado', style='font-size:1.5rem;'),
                    P('El boxenplot es una extensión del boxplot que utiliza cuantiles sucesivos para mostrar la distribución de los datos. Cada "caja" representa un rango de cuantiles, permitiendo visualizar la dispersión, la asimetría y la presencia de valores atípicos (outliers). Se basa en el cálculo de la mediana, los cuartiles y el rango intercuartílico (IQR). Los outliers se identifican como valores que están fuera de 1.5 veces el IQR respecto a los cuartiles.'),
                    cls='card',
                    style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                ),
                    Div(
                        B('Variables usadas y justificación', style='font-size:1.5rem;'),
                        P(B('Variables:'), ' Ingresos mensuales (p1_ing), Nivel educativo (nivel_educat)'),
                        P('Se usan estas variables porque queremos analizar cómo el nivel educativo influye en la distribución de los ingresos. El boxenplot permite comparar la dispersión y presencia de outliers entre grupos educativos.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Gráfico', style='font-size:1.5rem;'),
                        Img(src='static/analisis_boxen_ing_educacion.png', style='width:96%;max-width:900px;margin:18px auto;display:block;background:#fff;border-radius:10px;box-shadow:0 2px 12px #0003;'),
                        P('Distribución de ingresos mensuales por nivel educativo (Boxenplot).'),
                        cls='card',
                        style='min-height:320px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    style='display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:48px;grid-template-rows:auto auto;grid-template-areas:"modelo variables" "grafico grafico";'
                ),
                # 2. Barras de nulos
                Div(
                    Div(
                        B('Modelo matemático usado', style='font-size:1.5rem;'),
                        P('El gráfico de barras para nulos calcula el porcentaje de valores faltantes en cada columna. Se basa en la suma de valores nulos y la divide entre el total de registros para cada variable, permitiendo identificar rápidamente variables problemáticas.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Variables usadas y justificación', style='font-size:1.5rem;'),
                        P(B('Variables:'), ' Todas las columnas principales del dataset'),
                        P('Se analizan todas las variables para detectar aquellas con mayor cantidad de datos faltantes. Esto es fundamental para la limpieza y calidad del análisis posterior.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Gráfico', style='font-size:1.5rem;'),
                        Img(src='static/analisis_heatmap_nulos.png', style='width:96%;max-width:900px;margin:18px auto;display:block;background:#fff;border-radius:10px;box-shadow:0 2px 12px #0003;'),
                        P('Porcentaje de valores nulos por columna principal.'),
                        cls='card',
                        style='min-height:320px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    style='display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:48px;grid-template-rows:auto auto;grid-template-areas="modelo variables" "grafico grafico";'
                ),
                # 3. Hexbin edad-ingresos
                Div(
                    Div(
                        B('Modelo matemático usado', style='font-size:1.5rem;'),
                        P('El gráfico hexbin agrupa los datos en celdas hexagonales y cuenta cuántos registros caen en cada celda. Es útil para visualizar la densidad de puntos en relaciones numéricas, especialmente en grandes volúmenes de datos. Cada hexágono representa una frecuencia de ocurrencia para un rango de valores de edad e ingresos.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Variables usadas y justificación', style='font-size:1.5rem;'),
                        P(B('Variables:'), ' Edad (p1_edad), Ingresos mensuales (p1_ing)'),
                        P('Se usan estas variables para explorar la relación entre la edad y los ingresos. El hexbin permite ver la concentración de datos y detectar patrones o outliers que no serían evidentes en un scatterplot tradicional.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Gráfico', style='font-size:1.5rem;'),
                        Img(src='static/analisis_pairplot.png', style='width:96%;max-width:900px;margin:18px auto;display:block;background:#fff;border-radius:10px;box-shadow:0 2px 12px #0003;'),
                        P('Relación entre edad e ingresos mensuales (Hexbin).'),
                        cls='card',
                        style='min-height:320px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    style='display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:48px;grid-template-rows:auto auto;grid-template-areas="modelo variables" "grafico grafico";'
                ),
                # 4. Violinplot horas por sector
                Div(
                    Div(
                        B('Modelo matemático usado', style='font-size:1.5rem;'),
                        P('El violinplot combina un boxplot con una estimación de densidad de kernel (KDE). Muestra la distribución de los datos para cada grupo, permitiendo ver la forma, la dispersión y la presencia de múltiples modas. La "caja" central indica la mediana y los cuartiles, mientras que la forma exterior representa la densidad de los datos.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Variables usadas y justificación', style='font-size:1.5rem;'),
                        P(B('Variables:'), ' Horas trabajadas (p1_horas), Sector cultural (p1_sector)'),
                        P('Estas variables permiten comparar la distribución de horas trabajadas entre diferentes sectores culturales. El violinplot es ideal para visualizar diferencias de dispersión y densidad entre grupos.'),
                        cls='card',
                        style='min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    Div(
                        B('Gráfico', style='font-size:1.5rem;'),
                        Img(src='static/analisis_violin_horas_sector.png', style='width:96%;max-width:900px;margin:18px auto;display:block;background:#fff;border-radius:10px;box-shadow:0 2px 12px #0003;'),
                        P('Distribución de horas trabajadas por sector (Violinplot).'),
                        cls='card',
                        style='min-height:320px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
                    ),
                    style='display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:48px;grid-template-rows:auto auto;grid-template-areas="modelo variables" "grafico grafico";'
                ),
                cls='main-content'
            )
        )

@rt('/logout')
def logout():
    response = RedirectResponse(url='/login', status_code=303)
    response.delete_cookie('session_id')
    return response

# Ruta /limpio: teoría, imágenes y dataset limpio
@rt('/limpio')
def limpio(request):
    # Verificar sesión
    username = check_session(request)
    if not username:
        return RedirectResponse(url='/login', status_code=303)
    
    csv_path = 'data/rentoca_limpio.csv'
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip', encoding='latin1', low_memory=False)
        table = Table(
            Thead(
                Tr(*[Th(col, cls='table-header') for col in df.columns])
            ),
            *[Tr(*[Td(truncate(val), cls='table-cell') for val in row]) for row in df.head(20).values],
            cls='styled-table'
        )
    except Exception as e:
        table = P(f'Error al leer el CSV limpio: {e}')

    # Tarjetas de proceso de limpieza (12 pasos, cada uno con texto y su imagen)
    pasos = [
        {
            'titulo': 'Paso 1 — Revisar estado inicial',
            'texto': 'Evalúa tamaño del dataset, duplicados y columnas con más valores vacíos.',
            'img': 'static/paso1.jpg'
        },
        {
            'titulo': 'Paso 2 — Eliminar duplicados y columnas vacías',
            'texto': 'Quita filas repetidas y columnas con más del 80% de nulos.',
            'img': 'static/paso2.jpg'
        },
        {
            'titulo': 'Paso 3 — Normalizar nombres de columnas',
            'texto': 'Convierte nombres a minúsculas, sin acentos y sin caracteres especiales.',
            'img': 'static/paso3.jpg'
        },
        {
            'titulo': 'Paso 4 — Limpiar valores de texto inconsistentes',
            'texto': 'Transforma “NA”, “No aplica” y similares en NaN; unifica “Sí/No”.',
            'img': 'static/paso4.jpg'
        },
        {
            'titulo': 'Paso 5 — Eliminar filas completamente vacías',
            'texto': 'Descarta registros sin ningún dato útil para análisis.',
            'img': 'static/paso5.jpg'
        },
        {
            'titulo': 'Paso 6 — Convertir tipos de datos',
            'texto': 'Parsea fechas, convierte números y transforma “SI/NO” en booleanos.',
            'img': 'static/paso6.jpg'
        },
        {
            'titulo': 'Paso 7 — Normalización fina de strings',
            'texto': 'Elimina espacios dobles y mejora capitalización para columnas clave.',
            'img': 'static/paso7.jpg'
        },
        {
            'titulo': 'Paso 8 — Estandarizar categorías importantes',
            'texto': 'Unifica valores de sexo, actividades y nombres de departamentos.',
            'img': 'static/paso8.jpg'
        },
        {
            'titulo': 'Paso 9 — Deduplicación semántica',
            'texto': 'Elimina duplicados usando DNI, nombre completo y fecha como claves.',
            'img': 'static/paso9.jpg'
        },
        {
            'titulo': 'Paso 10 — Detección de outliers',
            'texto': 'Identifica valores numéricos atípicos mediante el método IQR.',
            'img': 'static/paso10.jpg'
        },
        {
            'titulo': 'Paso 11 — Chequeos finales de calidad',
            'texto': 'Revisa porcentajes de nulos y columnas con cardinalidad anómala.',
            'img': 'static/paso11.jpg'
        },
        {
            'titulo': 'Paso 12 — Exportación y bitácora',
            'texto': 'Ordena columnas, genera metadatos y exporta dataset limpio en CSV.',
            'img': 'static/paso12.jpg'
        }
    ]

    # Generar tarjetas en grid 2 columnas (texto - imagen)
    tarjetas = []
    for paso in pasos:
        tarjetas.append(
            Div(
                Div(
                    B(paso['titulo']),
                    P(paso['texto']),
                    cls='card-title',
                    style='font-size:1.3rem;text-align:center;margin-bottom:12px;'
                ),
                cls='card',
                style='background:rgba(40,44,52,0.96);color:#fff;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:180px;'
            )
        )
        tarjetas.append(
            Div(
                Img(src=paso['img'], style='width:96%;height:340px;object-fit:contain;border-radius:18px;box-shadow:0 2px 16px #0008;'),
                cls='card',
                style='background:rgba(40,44,52,0.96);color:#fff;display:flex;justify-content:center;align-items:center;min-height:340px;font-size:1.2rem;'
            )
        )

    grid = Div(
        *tarjetas,
        style='display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:48px;'
    )

    # Card: Vista previa del dataset limpio
    card_dataset = Div(
        Div('Vista previa del dataset limpio', cls='card-title'),
        Div(table, cls='card-dataset'),
        cls='card-large fade-in-title'
    )

    return Div(
        dark_css,
        menu(username),
        Div(
            Div('RETOCA limpio: Teoría y resultados', cls='main-title'),
            grid,
            card_dataset,
            cls='main-content'
        )
    )

@rt('/login', methods=['GET', 'POST'])
async def login(request):
    error_msg = None
    
    if request.method == 'POST':
        form_data = await request.form()
        username = form_data.get('username', '').strip()
        password = form_data.get('password', '').strip()
        
        # Validar credenciales
        if username in DEMO_CREDENTIALS and DEMO_CREDENTIALS[username] == password:
            session_id = create_session(username)
            response = RedirectResponse(url='/', status_code=303)
            response.set_cookie('session_id', session_id, max_age=86400, httponly=True)
            return response
        else:
            error_msg = 'Usuario o contraseña incorrectos'
    
    return Div(
        dark_css,
        Div(
            Div(
                Div('RENTOCA', cls='login-title'),
                Div('Sistema de Análisis de Trabajadores Culturales', cls='login-subtitle'),
                Div(
                    Form(
                        Div(
                            error_msg and Div(error_msg, cls='login-error') or '',
                            Div(
                                Label('Usuario', cls='form-label'),
                                Input(type='text', name='username', cls='form-input', placeholder='admin, user o guest', required=True),
                                cls='form-group'
                            ),
                            Div(
                                Label('Contraseña', cls='form-label'),
                                Input(type='password', name='password', cls='form-input', placeholder='ver abajo', required=True),
                                cls='form-group'
                            ),
                            Button('Ingresar', type='submit', cls='login-btn'),
                            cls='login-form'
                        ),
                        method='POST'
                    ),
                    Div(
                        P(
                            B('Credenciales de demo:'),
                            Br(),
                            'admin / admin123',
                            Br(),
                            'user / user123',
                            Br(),
                            'guest / guest',
                            cls='login-footer'
                        ),
                        style='margin-top: 24px; padding-top: 24px; border-top: 1px solid #374151;'
                    )
                ),
                cls='login-card'
            ),
            cls='login-container'
        )
    )

@rt('/')
def index(request):
    # Verificar sesión
    username = check_session(request)
    if not username:
        return RedirectResponse(url='/login', status_code=303)
    
    csv_path = 'data/rentoca_limpio.csv'
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip', encoding='latin1', low_memory=False)
        table = Table(
            Thead(
                Tr(*[Th(col, cls='table-header') for col in df.columns])
            ),
            *[Tr(*[Td(truncate(val), cls='table-cell') for val in row]) for row in df.head(20).values],
            cls='styled-table'
        )
    except Exception as e:
        table = P(f'Error al leer el CSV: {e}')

    card_purpose = Div(
        Div('Propósito del Proyecto', cls='card-title', style='text-align:center;'),
        Div(
            P('El RENTOCA es un registro oficial del sector cultural peruano, pero su estructura original contiene problemas como vacíos, duplicados e inconsistencias, lo que dificulta analizar adecuadamente la realidad de los trabajadores culturales.', style='text-align:center;'),
            P('Nuestro objetivo fue tomar este archivo complejo, limpiarlo y transformarlo en un dataset confiable, listo para realizar análisis, visualizaciones y modelos de machine learning.', style='text-align:center;'),
            cls='card-content fade-in-text',
            style='text-align:center;'
        ),
        cls='card fade-in-title',
        style='margin:auto;'
    )

    card_problems = Div(
        Div('Problemas Iniciales Detectados', cls='card-title', style='text-align:center;'),
        Div(
            B('1. Calidad de Datos'),
            P('Muchas columnas vacías o incompletas.'),
            P('Respuestas inconsistentes entre registros.'),
            P('Duplicados y errores de formato.'),
            B('2. Errores de Codificación'),
            P('Uso irregular de mayúsculas y acentos.'),
            P('Caracteres especiales mal codificados.'),
            P('Comillas tipográficas que rompían el procesamiento.'),
            cls='card-list fade-in-text',
            style='text-align:left;'
        ),
        cls='card fade-in-title',
        style='margin:auto;'
    )

    card_dataset = Div(
        Div('Vista previa del dataset', cls='card-title', style='text-align:center;'),
        Div(table, cls='card-dataset'),
        cls='card-large fade-in-title',
        style='margin:auto;'
    )

    return Div(
        dark_css,
        menu(username),
        Div(
            Div('Análisis estadístico y predictivo del dataset RENTOCA', cls='main-title', style='text-align:center;'),
            Div(
                card_purpose,
                card_problems,
                cls='cards-row',
                style='justify-content:center;align-items:center;gap:48px;'
            ),
            card_dataset,
            cls='main-content',
            style='align-items:center;justify-content:center;display:flex;flex-direction:column;gap:48px;'
        )
    )


# Iniciar servidor después de declarar todas las rutas
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    serve(host='0.0.0.0', port=port)
