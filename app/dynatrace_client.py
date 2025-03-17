import requests
import os

# Configuración
DYNATRACE_URL = os.getenv("DYNATRACE_URL")
API_TOKEN = os.getenv("API_TOKEN")


# Cabeceras con autenticación
headers = {
    "Authorization": f"Api-Token {API_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8"
}


def enviar_metrica(nombre, valor, unidad="count"):
    """Envía una métrica personalizada a Dynatrace"""

    payload = f"{nombre},unit={unidad} {valor}"
    
    response = requests.post(DYNATRACE_URL, headers=headers, data=payload)

    print(response.text)
    
    if response.status_code == 202:
        print(f"Métrica '{nombre}' enviada con éxito: {valor} {unidad}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
