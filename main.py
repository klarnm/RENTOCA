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
# - Si `username` está presente muestra un enlace de logout com
