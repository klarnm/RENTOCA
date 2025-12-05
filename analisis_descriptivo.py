import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ═══════════════════════════════════════════════════════════════════════════
# 📊 SCRIPT DE GENERACIÓN DE GRÁFICOS ESTÁTICOS
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ HACE:
# - Lee el dataset limpio (rentoca_limpio.csv)
# - Genera 5 gráficos descriptivos + 1 modelo ML
# - Guarda todos los gráficos como PNG en la carpeta static/
# - CADA BLOQUE es independiente: si falla uno, los otros siguen funcionando
#
# USO:
# python analisis_descriptivo.py
# Genera todos los PNG necesarios para que la web muestre los gráficos
#
# NOTA: Este script se ejecuta UNA SOLA VEZ para pre-generar las imágenes
#       La web luego solo muestra estas imágenes (no genera en tiempo real)

# 📂 CARGAR DATASET LIMPIO
csv_path = 'data/rentoca_limpio.csv'
df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip', encoding='latin1', low_memory=False)


# ═══════════════════════════════════════════════════════════════════════════
# 📊 GRÁFICO 1: HEATMAP DE VALORES NULOS
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ MUESTRA:
# - Porcentaje de datos faltantes por cada columna principal
# - Ayuda a identificar qué columnas tienen más "huecos"
# - Ej: Si edad tiene 5% de nulos, hay 5% de registros sin edad
#
# INTERPRETACIÓN:
# - Barras altas = muchos datos faltantes (problema de calidad)
# - Barras bajas = pocos datos faltantes (columna confiable)

# Seleccionar solo columnas principales para análisis de nulos
cols_nulos = ['sexo', 'edad', 'departamento', 'provincia', 'nivel_educat', 'p1_ing', 'p1_horas', 'p1_sector', 'p1_perfil', 'p1_sunat']

# Calcular porcentaje de nulos: sum(nulos) / total * 100
porc_nulos = (df[cols_nulos].isnull().mean() * 100).round(1)

# Crear figura y gráfico de barras
plt.figure(figsize=(10,5))
bars = plt.bar(porc_nulos.index, porc_nulos.values, color=sns.color_palette('pastel'))
plt.ylabel('% de valores nulos', fontsize=12)
plt.xlabel('Columna', fontsize=12)
plt.title('Porcentaje de valores nulos por columna principal', fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=11)
plt.ylim(0, 100)

# Etiquetas sobre cada barra mostrando el porcentaje exacto
for bar in bars:
	height = bar.get_height()
	plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

# Guardar y cerrar
plt.tight_layout()
plt.savefig('static/analisis_heatmap_nulos.png')
plt.close()

# ═══════════════════════════════════════════════════════════════════════════
# 📊 GRÁFICO 2: BOXENPLOT - INGRESOS vs EDUCACIÓN
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ MUESTRA:
# - Distribución de INGRESOS para CADA NIVEL EDUCATIVO
# - Cada "columna" = un nivel educativo (Primaria, Secundaria, etc.)
# - Las "cajas" muestran cuartiles (25%, 50%, 75% de los datos)
# - Los puntos = valores atípicos (outliers)
#
# INTERPRETACIÓN:
# - Columna más alta = ingresos más altos en ese nivel educativo
# - Columna más ancha = mucha variabilidad (algunos ganan mucho, otros poco)
# - Puntos arriba = personas con ingresos excepcionales

# Filtrar datos: solo ingresos < 100k para mejor visualización
# (los ingresos muy altos distorsionan la escala)
df_boxen = df[(df['p1_ing'] < 100000) & (~df['p1_ing'].isnull()) & (~df['nivel_educat'].isnull())]

# Ordenar por cantidad de registros (de más a menos)
orden_educ = df_boxen['nivel_educat'].value_counts().index.tolist()

# Crear boxenplot (versión mejorada del boxplot)
plt.figure(figsize=(12,6))
sns.boxenplot(x='nivel_educat', y='p1_ing', data=df_boxen, order=orden_educ)
plt.xticks(rotation=30, ha='right', fontsize=9)
plt.ylabel('Ingresos (p1_ing)')
plt.title('Ingresos (p1_ing) por nivel educativo (Boxenplot, <100k)')
plt.tight_layout()
plt.savefig('static/analisis_boxen_ing_educacion.png')
plt.close()

# ═══════════════════════════════════════════════════════════════════════════
# 📊 GRÁFICO 3: HEXBIN - EDAD vs INGRESOS (MAPA DE DENSIDAD)
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ MUESTRA:
# - Relación entre EDAD (eje X) e INGRESOS (eje Y)
# - Los hexágonos oscuros = muchas personas en esa combinación edad-ingreso
# - Los hexágonos claros = pocas personas
# - Colores plasma: oscuro=baja densidad, brillante=alta densidad
#
# INTERPRETACIÓN:
# - Si hay línea diagonal: a más edad, más ingresos
# - Si hay línea horizontal: la edad no influye en ingresos
# - Agrupaciones: tendencias comunes (ej: mayoría gana entre 1000-3000)

# Cargar datos de edad e ingresos (eliminar filas con nulos)
df_hex = df[['edad', 'p1_ing']].dropna()

# Filtrar ingresos extremos para mejor visualización (outliers distorsionan)
df_hex = df_hex[df_hex['p1_ing'] < 100000]

# Crear hexbin con 40x40 hexágonos
# gridsize=40: número de hexágonos por lado
# cmap='plasma': color scheme (oscuro=baja densidad, brillante=alta)
# mincnt=1: mostrar hexágonos incluso con 1 valor
plt.figure(figsize=(9,7))
hb = plt.hexbin(df_hex['edad'], df_hex['p1_ing'], gridsize=40, cmap='plasma', mincnt=1)

# Agregar barra de colores con etiqueta
cb = plt.colorbar(hb)
cb.set_label('Cantidad de registros')

# Etiquetas y límites de ejes
plt.xlabel('Edad', fontsize=12)
plt.ylabel('Ingresos mensuales (p1_ing)', fontsize=12)
plt.title('Relación entre edad e ingresos mensuales (Hexbin)', fontsize=14)
plt.xlim(15, 100)  # Edad entre 15 y 100 años
plt.ylim(0, 100000)  # Ingresos entre 0 y 100k
plt.tight_layout()
plt.savefig('static/analisis_pairplot.png')
plt.close()

# ═══════════════════════════════════════════════════════════════════════════
# 📊 GRÁFICO 4: VIOLINPLOT - HORAS TRABAJADAS POR SECTOR
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ MUESTRA:
# - Distribución de HORAS TRABAJADAS para CADA SECTOR
# - Los "violines" son como boxplots pero con forma de distribución
# - Sector más ancho = mayor variabilidad de horas
# - El box interior = cuartiles (25%, 50%, 75%)
# - La línea en el medio = mediana (valor central)
#
# INTERPRETACIÓN:
# - Violín ancho = hay trabajadores que trabajan muchas horas distintas
# - Violín estrecho = la mayoría trabaja horas similares (más consistente)
# - Posición del box = mayoría trabaja esas horas

# Filtrar datos: solo filas con ambas columnas (p1_horas y p1_sector)
df_violin = df[(~df['p1_horas'].isnull()) & (~df['p1_sector'].isnull())]

# Ordenar sectores por cantidad de registros (de más a menos)
orden_sector = df_violin['p1_sector'].value_counts().index.tolist()

# Crear violinplot
plt.figure(figsize=(12,6))
sns.violinplot(
    x='p1_sector',  # Eje X: cada sector
    y='p1_horas',   # Eje Y: horas trabajadas
    data=df_violin,
    order=orden_sector,  # Ordenar por cantidad
    inner='box',         # Mostrar box interior
    cut=0                # No extender violín más allá de los datos
)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Horas trabajadas')
plt.xlabel('Sector')
plt.title('Distribución de horas trabajadas por sector (Violinplot)')
plt.tight_layout()
plt.savefig('static/analisis_violin_horas_sector.png')
plt.close()

# ═══════════════════════════════════════════════════════════════════════════
# 🤖 GRÁFICO 5: MODELO MACHINE LEARNING - DECISION TREE (FORMALIDAD)
# ═══════════════════════════════════════════════════════════════════════════
# QUÉ HACE:
# - Entrena un DecisionTreeClassifier para predecir FORMALIDAD
# - Target: p1_sunat (¿está registrado en SUNAT? = formal o informal)
# - Features: características del trabajador (edad, educación, sector, etc.)
# - Objetivo: clasificar automáticamente si es "Formal" o "Informal"
#
# ALGORITMO: Decision Tree (Árbol de Decisión)
# - Funciona por preguntas binarias: "¿edad > 30?", "¿sector = cultura?"
# - Construye un árbol de decisiones que particiona los datos
# - Ventaja: interpretable, rápido, no requiere normalización
# - Desventaja: puede overfitting (memorizar datos en lugar de aprender patrones)
#
# NOTA: Este es un modelo DEMO/EDUCATIVO, no es producción

print('🤖 Generando modelo ML - Decision Tree para predicciones de formalidad...')
try:
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PASO 0: DEFINIR TARGET (QUÉ PREDECIR) Y FEATURES (CON QUÉ PREDECIR)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # TARGET: La columna que queremos predecir
    # p1_sunat = ¿está registrado en SUNAT? (binaria: Sí/No = Formal/Informal)
    target = 'p1_sunat'
    
    # FEATURES: Las columnas que usamos como pistas para predecir
    # Se seleccionan características que probablemente estén relacionadas con formalidad
    features = [
        'tipo_registro',      # Tipo de registro en RENTOCA
        'direccion_principal', # Tiene dirección = más formalidad
        'nivel_educat',       # Nivel educativo (educación > formalidad)
        'p1_sector',          # Sector de trabajo
        'p1_perfil',          # Perfil de trabajador
        'p1_ocupacion_f1',    # Ocupación específica
        'frec_ingreso',       # Frecuencia de ingresos (regular = formal)
        'p1_horas',           # Horas trabajadas (regular = formal)
        'p1_cat_lab',         # Categoría laboral
        'p1_ing'              # Ingreso mensual
    ]
    
    # Filtrar solo las features que existen en el dataset
    features = [col for col in features if col in df.columns]

    # Validar que tengamos target y al menos algunas features
    if target in df.columns and features:
        print(f'   ✓ Target: {target}')
        print(f'   ✓ Features ({len(features)}): {", ".join(features)}')
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PASO 1: PREPARAR DATOS (LIMPIEZA Y CODIFICACIÓN)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        # Filtrar filas donde NO existe el target (p1_sunat)
        # Solo entrenamos con datos que sabemos si son formales o no
        data = df[features + [target]].dropna(subset=[target])
        
        # Rellenar valores nulos en features con 'Desconocido'
        # No eliminamos filas: asumimos que "nulo" es información válida
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

