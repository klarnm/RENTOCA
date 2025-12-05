import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Script de generación de gráficos estáticos usados por la app
# - Lee el CSV ya limpio y genera imágenes en `static/`.
# - Cada bloque produce un gráfico independiente (guarda y cierra la figura).
# Cargar el dataset limpio
csv_path = 'data/rentoca_limpio.csv'
df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip', encoding='latin1', low_memory=False)


# 1. Heatmap de nulos (solo columnas principales y primeras 500 filas)

# Gráfico de barras: porcentaje de nulos por columna principal
cols_nulos = ['sexo', 'edad', 'departamento', 'provincia', 'nivel_educat', 'p1_ing', 'p1_horas', 'p1_sector', 'p1_perfil', 'p1_sunat']
porc_nulos = (df[cols_nulos].isnull().mean() * 100).round(1)
plt.figure(figsize=(10,5))
bars = plt.bar(porc_nulos.index, porc_nulos.values, color=sns.color_palette('pastel'))
plt.ylabel('% de valores nulos', fontsize=12)
plt.xlabel('Columna', fontsize=12)
plt.title('Porcentaje de valores nulos por columna principal', fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=11)
plt.ylim(0, 100)
# Etiquetas sobre cada barra
for bar in bars:
	height = bar.get_height()
	plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('static/analisis_heatmap_nulos.png')
plt.close()

# 2. Boxenplot: ingresos por nivel educativo (filtrando extremos)
df_boxen = df[(df['p1_ing'] < 100000) & (~df['p1_ing'].isnull()) & (~df['nivel_educat'].isnull())]
orden_educ = df_boxen['nivel_educat'].value_counts().index.tolist()
plt.figure(figsize=(12,6))
sns.boxenplot(x='nivel_educat', y='p1_ing', data=df_boxen, order=orden_educ)
plt.xticks(rotation=30, ha='right', fontsize=9)
plt.ylabel('Ingresos (p1_ing)')
plt.title('Ingresos (p1_ing) por nivel educativo (Boxenplot, <100k)')
plt.tight_layout()
plt.savefig('static/analisis_boxen_ing_educacion.png')
plt.close()

# 3. Hexbin: relación entre edad e ingresos
df_hex = df[['edad', 'p1_ing']].dropna()
# Limitar ingresos a 0-100,000 para mejor visualización
df_hex = df_hex[df_hex['p1_ing'] < 100000]
plt.figure(figsize=(9,7))
hb = plt.hexbin(df_hex['edad'], df_hex['p1_ing'], gridsize=40, cmap='plasma', mincnt=1)
cb = plt.colorbar(hb)
cb.set_label('Cantidad de registros')
plt.xlabel('Edad', fontsize=12)
plt.ylabel('Ingresos mensuales (p1_ing)', fontsize=12)
plt.title('Relación entre edad e ingresos mensuales (Hexbin)', fontsize=14)
plt.xlim(15, 100)
plt.ylim(0, 100000)
plt.tight_layout()
plt.savefig('static/analisis_pairplot.png')
plt.close()

# 4. Violinplot: horas trabajadas por sector
df_violin = df[(~df['p1_horas'].isnull()) & (~df['p1_sector'].isnull())]
orden_sector = df_violin['p1_sector'].value_counts().index.tolist()
plt.figure(figsize=(12,6))
sns.violinplot(x='p1_sector', y='p1_horas', data=df_violin, order=orden_sector, inner='box', cut=0)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Horas trabajadas')
plt.xlabel('Sector')
plt.title('Distribución de horas trabajadas por sector (Violinplot)')
plt.tight_layout()
plt.savefig('static/analisis_violin_horas_sector.png')
plt.close()

# 5. NUEVO: Gráfico de distribución de predicciones del modelo ML - BINARIA (Formal vs Informal)
print('Generando gráfico de distribución de predicciones...')
try:
    # --- Paso 0: Definir objetivo y features ---
    # `target` es la columna original que indica registro en SUNAT.
    # `features` es una lista manual de columnas a usar; se filtra por existencia.
    target = 'p1_sunat'
    features = ['tipo_registro', 'direccion_principal', 'nivel_educat', 'p1_sector', 'p1_perfil', 
                'p1_ocupacion_f1', 'frec_ingreso', 'p1_horas', 'p1_cat_lab', 'p1_ing']
    features = [col for col in features if col in df.columns]

    # Solo procedemos si tenemos la columna objetivo y al menos una feature
    if target in df.columns and features:
        # 1) Filtrar filas sin target y rellenar nulos secundarios
        #    - No eliminamos filas con nulos en features: los convertimos a 'Desconocido'
        data = df[features + [target]].dropna(subset=[target])
        data = data.fillna('Desconocido')

        # 2) Preparar X e y crudos
        #    - X: todas las features como strings (maneja columnas mixtas)
        #    - y: la columna original como string (la convertiremos a binaria luego)
        X = data[features].astype(str)
        y = data[target].astype(str)

        # 3) Binarizar la variable objetivo (Formal=1, Informal=0)
        #    - Debido a problemas de encoding en el CSV usamos detección basada en palabras clave
        #    - Si contiene 'NO EST' -> Informal (no registrado)
        #    - Si contiene 'PERSONA' o 'JURIDICA' -> Formal (registrado)
        def clasificar_formalidad(valor):
            valor_str = str(valor).upper()
            if 'NO EST' in valor_str:
                return 0
            elif 'PERSONA' in valor_str or 'JURIDICA' in valor_str:
                return 1
            # Conservador: todo lo no identificado se marca como informal
            return 0

        y_binaria = y.apply(clasificar_formalidad)

        # 4) Codificar variables categóricas con LabelEncoder
        #    - Método simple y determinista para pasar cadenas a enteros
        #    - Guardamos los encoders en caso de querer revertir la codificación
        encoders = {}
        for col in features:
            enc = LabelEncoder()
            X[col] = enc.fit_transform(X[col])
            encoders[col] = enc

        # 5) Dividir en entrenamiento y test
        #    - Usamos test_size=0.2 y random_state fijo para reproducibilidad
        X_train, X_test, y_train, y_test = train_test_split(X, y_binaria, test_size=0.2, random_state=42)

        # 6) Entrenar un clasificador sencillo (DecisionTree)
        #    - max_depth=4 para mantener el modelo interpretable y evitar overfitting excesivo
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        clf.fit(X_train, y_train)

        # 7) Evaluación rápida en test (accuracy como referencia básica)
        y_pred = clf.predict(X_test)
        acc = (y_pred == y_test).mean()

        # 8) Contar la distribución de predicciones (informal vs formal)
        n_informal_pred = int((y_pred == 0).sum())
        n_formal_pred = int((y_pred == 1).sum())

        # Preparar etiquetas y colores para la tarta
        counts_vals = [n_informal_pred, n_formal_pred]
        labels = [f'Informal\n({n_informal_pred} predicciones)', 
                  f'Formal\n({n_formal_pred} predicciones)']
        colors = ['#ff6a88', '#4caf50']

        # 9) Crear gráfico tipo 'pie' con estilo coherente con la app
        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax.pie(counts_vals, 
                                           labels=labels,
                                           colors=colors,
                                           autopct='%1.1f%%',
                                           startangle=90,
                                           textprops={'fontsize': 12, 'color': '#f3f3f3'},
                                           explode=(0.05, 0.05))

        # Ajustes de estilo para legibilidad
        for autotext in autotexts:
            autotext.set_color('#2a2a2a')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(14)

        ax.set_title(f'Distribución de Predicciones del Modelo ML\nPrecisión: {acc:.2%}', 
                    fontsize=14, fontweight='bold', color='#90caf9', pad=20)

        # Aplicar fondo oscuro al gráfico (coherente con el theme de la app)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#2a2a2a')

        plt.tight_layout()
        plt.savefig('static/ml_distribucion_predicciones.png', facecolor='#1a1a1a', edgecolor='none', dpi=100)
        plt.close()
        print('[OK] Grafico de distribucion de predicciones generado correctamente')
except Exception as e:
    print(f'[WARN] Error al generar grafico de predicciones: {e}')

