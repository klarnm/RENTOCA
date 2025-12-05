# RENTOCA — Análisis Estadístico y Predictivo

Versión profesional del README para el proyecto RENTOCA: limpieza, análisis y modelado del Registro Nacional de Trabajadores Culturales (Perú).

## Resumen

RENTOCA es un proyecto que procesa y analiza el registro nacional de trabajadores culturales. El objetivo principal es transformar datos ruidosos en un dataset utilizable para visualizaciones, análisis estadístico y un modelo de clasificación de prueba que estima la formalidad (registro en SUNAT) de los trabajadores.

Este repositorio contiene una pequeña aplicación web (basada en FastHTML) para explorar resultados y una colección de scripts para generar gráficos estáticos.

## Contenido del repositorio

- `main.py` — Aplicación web (rutas: `/`, `/limpio`, `/analisis`, `/predicciones`).
- `analisis_descriptivo.py` — Script que genera las imágenes PNG usadas por la app (en `static/`).
- `data/` — Contiene `rentoca_limpio.csv` (dataset limpio) y el original.
- `static/` — Imágenes generadas y recursos estáticos.
- `explicacion_graficos.txt` — Anotaciones y justificaciones de las visualizaciones.
- `requirements.txt` — Dependencias del proyecto.

## Estado y alcance

- Esta es una versión demostrativa y educativa. La autenticación es en memoria (credenciales demo) y el pipeline de ML está pensado para ejemplificar el flujo: limpieza mínima → codificación → DecisionTreeClassifier.
- No es producción: no hay persistencia segura de sesiones ni despliegue optimizado.

## Requisitos

- Python 3.11+ (recomendado)
- pip

Se asume un entorno de desarrollo local en Windows usando `bash.exe` (Git Bash / WSL compatible).

## Instalación rápida

1. Abre una terminal en la carpeta del proyecto:

```bash
cd C:/Users/aarvg/Desktop/RENTOCA
```

2. Crear y activar un entorno virtual (recomendado):

```bash
# Crear entorno
python -m venv .venv

# Activar en bash.exe (Git Bash / WSL)
source .venv/Scripts/activate
```

Si usas PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
# Si FastHTML no está en PyPI, instalar desde el repo (si es necesario):
pip install git+https://github.com/AnswerDotAI/fasthtml.git
```

Nota: Si no existe `requirements.txt`, instala manualmente:

```bash
pip install pandas scikit-learn matplotlib seaborn numpy uvicorn
```

## Ejecución

- Ejecutar la aplicación web (desarrollo):

```bash
python main.py
```

Abre: http://localhost:5000

- Regenerar todos los gráficos estáticos (se guardan en `static/`):

```bash
python analisis_descriptivo.py
```

## Credenciales demo

- `admin` / `admin123`
- `user` / `user123`
- `guest` / `guest`

Estas credenciales se usan únicamente para la demo; las sesiones se almacenan en memoria.

## Descripción técnica (resumen)

- Entrada: `data/rentoca_limpio.csv` (CSV con separador `;`, encoding `latin1`).
- Preprocesamiento: se limpian nulos mínimos, se convierte la columna `p1_sunat` a binaria (heurística por texto) y se rellenan nulos con `'Desconocido'`.
- Features: selección manual de columnas relevantes (ej.: `nivel_educat`, `p1_ing`, `p1_horas`, `p1_sector`, etc.).
- Codificación: `LabelEncoder` aplicado a cada columna categórica.
- Modelo de ejemplo: `DecisionTreeClassifier(max_depth=4)` con `train_test_split(test_size=0.2, random_state=42)`.

## Notas importantes y recomendaciones

- El target `p1_sunat` en el CSV original tiene problemas de codificación y múltiples categorías; la conversión a binaria se hace por búsqueda de palabras clave y puede no ser perfecta.
- Métricas más robustas: añadir matriz de confusión, precision/recall/F1; considerar `class_weight='balanced'` o re-muestreo (SMOTE) si se mejora el modelo.
- Para producción: usar base de datos para sesiones, implementar autenticación real, añadir paginación y limitar el tamaño de tablas enviadas al cliente.

## Cómo contribuir

- Abrir un issue con la mejora deseada o enviar PR con cambios pequeños (formato de código consistente).

## Licencia

- MIT — ver archivo LICENSE si aplica.

---

Si quieres, puedo añadir:
- Un `requirements.txt` verificado con las versiones exactas usadas.
- Un `Makefile` / scripts para entornos Windows.
- Tests básicos que verifiquen que `analisis_descriptivo.py` genera imágenes.

Indícame cuál de estos extras quieres que añada y lo preparo.
# 📊 RENTOCA: Análisis Estadístico y Predictivo del Dataset

Proyecto web interactivo para analizar, visualizar y hacer predicciones sobre el **RENTOCA** (Registro Nacional de Trabajadores Culturales) del sector cultural peruano.

## 🎯 Propósito

El RENTOCA es un registro oficial, pero su estructura original contiene problemas:
- Vacíos de datos inconsistentes
- Duplicados semánticos
- Errores de codificación
- Inconsistencias de formato

Este proyecto **limpia, analiza y modela** los datos para generar insights sobre formalidad, ingresos y características del sector cultural.

---

## 📁 Estructura del Proyecto

```
RENTOCA/
├── main.py                      # Servidor web FastHTML (4 rutas principales)
├── analisis_descriptivo.py      # Script para generar gráficos estadísticos
├── explicacion_graficos.txt     # Documentación de visualizaciones
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
├── data/
│   ├── rentoca_limpio.csv       # Dataset procesado (limpio)
│   └── rentoca_original.csv     # Dataset sin procesar (original)
└── static/                      # Imágenes generadas
    ├── analisis_*.png           # 4 gráficos de análisis
    └── paso*.jpg                # 12 pasos del proceso de limpieza
```

---

## 🚀 Instalación y Setup

### 1️⃣ Requisitos Previos
- Python 3.11+
- pip (gestor de paquetes)

### 2️⃣ Clonar o Descargar el Repositorio
```bash
cd RENTOCA
```

### 3️⃣ Instalar Dependencias
```bash
# Instalar paquetes base
pip install -r requirements.txt

# Instalar FastHTML (desde GitHub)
pip install git+https://github.com/AnswerDotAI/fasthtml.git
```

---

## 🎬 Uso

### Opción A: Ejecutar la Aplicación Web
```bash
python main.py
```
Luego abre tu navegador en: **http://localhost:5000**

### Opción B: Generar Gráficos Estadísticos
```bash
python analisis_descriptivo.py
```
Los gráficos se guardarán en `static/`

---

## 📱 Rutas Disponibles en la Aplicación Web

| Ruta | Descripción |
|------|------------|
| **`/`** | 🏠 Portada + Introducción del proyecto + Vista previa de datos |
| **`/limpio`** | 🧹 Explica los 12 pasos de limpieza con imágenes |
| **`/analisis`** | 📊 4 gráficos estadísticos interactivos |
| **`/predicciones`** | 🤖 Predicción de formalidad usando ML (DecisionTree) |

---

## 📊 Análisis Incluidos

### 1. **Boxenplot** - Distribución de Ingresos por Nivel Educativo
- Visualiza cómo el nivel educativo influye en los ingresos
- Detecta outliers y asimetría en la distribución

### 2. **Heatmap de Nulos** - Porcentaje de Valores Faltantes
- Identifica qué columnas tienen más datos incompletos
- Fundamental para entender la calidad del dataset

### 3. **Hexbin** - Relación Edad vs. Ingresos
- Muestra la densidad de puntos en esta relación
- Detecta patrones concentrados y outliers

### 4. **Violinplot** - Distribución de Horas Trabajadas por Sector
- Compara dedicación laboral entre sectores culturales
- Visualiza múltiples distribuciones simultáneamente

---

## 🤖 Pipeline de Machine Learning

### Modelo: Decision Tree Classifier
- **Objetivo**: Predecir formalidad (registro en SUNAT)
- **Características usadas**: tipo_registro, nivel_educat, sector, perfil, ocupación, horas, ingreso
- **Precisión**: Se calcula en test set (20% de datos)
- **Salida**: Tabla de predicciones para todos los registros

---

## 🛠️ Tecnologías Usadas

| Librería | Función |
|----------|---------|
| **FastHTML** | Framework web ligero para UI |
| **Pandas** | Manipulación y análisis de datos |
| **Matplotlib & Seaborn** | Visualización estatística |
| **Scikit-Learn** | Machine Learning (DecisionTree, LabelEncoder) |
| **NumPy** | Operaciones numéricas |

---

## 📝 Archivos Clave

### `main.py` (683 líneas)
- Servidor web con 4 rutas principales
- Interfaz oscura moderna con CSS personalizado
- Lectura y procesamiento de CSV
- Pipeline de ML integrado

### `analisis_descriptivo.py` (69 líneas)
- Genera 4 gráficos PNG
- Limpieza de datos extremos (filtra ingresos > 100k)
- Usa índices de columnas dinámicos

### `explicacion_graficos.txt`
- Documentación clara de cada visualización
- Explica qué representa y por qué es importante

---

## ⚠️ Problemas Conocidos y Soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| Tabla de predicciones lenta | Muchas filas procesadas | Limitar a 200 filas en futuras versiones |
| FastHTML no instala de PyPI | Repositorio privado | Usar `git+https://github.com...` |
| Errores de indentación | Tabs vs. espacios | Convertir a 4 espacios |

---

## 🔧 Mejoras Futuras

- [ ] Paginar tabla de predicciones
- [ ] Agregar tests automatizados
- [ ] Implementar API REST
- [ ] Dashboard interactivo con Plotly
- [ ] Exportar reportes a PDF
- [ ] Autenticación de usuarios

---

## 📚 Documentación Adicional

Para detalles sobre el proceso de limpieza, ver: **`explicacion_graficos.txt`**

---

## 👤 Autor
Proyecto RENTOCA - Análisis de Sector Cultural Peruano

## 📄 Licencia
MIT

---

## 💬 Soporte

Si encuentras problemas:
1. Verifica que Python 3.11+ esté instalado: `python --version`
2. Comprueba las dependencias: `pip list`
3. Revisa los logs de la aplicación en la terminal

¡Que disfrutes explorando el dataset RENTOCA! 🎨🎭🎪

