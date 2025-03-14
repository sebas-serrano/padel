import requests

# Configuración

DYNATRACE_URL = "https://avl52975.live.dynatrace.com/api/v2/metrics/ingest"
API_TOKEN = "dt0c01.6ERICNNGIYMSPUJII6VODYUS.C5JOCAXDEPM6UTBUTGWXYYPMXEQXGOFAWHM7W4I6HCDN4NN3FLKFXRMLOP2DWHK6"

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
