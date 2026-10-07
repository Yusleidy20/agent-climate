import urllib.request
import urllib.parse
import json
import ollama

def obtener_clima(ciudad: str, pais: str = "") -> str:
    try:
        termino_busqueda = f"{ciudad}, {pais}".strip(", ") if pais else ciudad
        ciudad_encoded = urllib.parse.quote(termino_busqueda)
        
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad_encoded}&count=1&language=es&format=json"
        req = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            geo_data = json.loads(response.read().decode('utf-8'))
            
        if not geo_data.get('results'):
            return f"No se encontraron datos geográficos para '{termino_busqueda}'."

        lugar = geo_data['results'][0]
        lat, lon = lugar['latitude'], lugar['longitude']
        nombre_real = lugar.get('name', ciudad)
        pais_real = lugar.get('country', '')

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        req_w = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req_w) as response:
            weather_data = json.loads(response.read().decode('utf-8'))

        clima = weather_data['current_weather']
        temp = clima['temperature']
        viento = clima['windspeed']
        codigo_clima = clima.get('weathercode')
        condiciones = {
            0: "despejado",
            1: "mayormente despejado",
            2: "parcialmente nublado",
            3: "nublado",
            45: "con niebla",
            48: "con niebla y escarcha",
            51: "con llovizna ligera",
            53: "con llovizna moderada",
            55: "con llovizna intensa",
            56: "con llovizna helada ligera",
            57: "con llovizna helada intensa",
            61: "con lluvia ligera",
            63: "con lluvia moderada",
            65: "con lluvia intensa",
            66: "con lluvia helada ligera",
            67: "con lluvia helada intensa",
            71: "con nieve ligera",
            73: "con nieve moderada",
            75: "con nieve intensa",
            77: "con granos de nieve",
            80: "con chubascos ligeros",
            81: "con chubascos moderados",
            82: "con chubascos intensos",
            85: "con chubascos de nieve ligeros",
            86: "con chubascos de nieve intensos",
            95: "con tormenta",
            96: "con tormenta y granizo ligero",
            99: "con tormenta y granizo intenso",
        }.get(codigo_clima, "con condiciones no disponibles")

        ubicacion_completa = f"{nombre_real}, {pais_real}" if pais_real else nombre_real

        return (
            f"En {ubicacion_completa}, ahora hay {temp}°C, {condiciones} "
            f"y viento de {viento} km/h."
        )

    except Exception as e:
        return f"Error al consultar la API de clima: {str(e)}"

herramienta_clima = {
    'type': 'function',
    'function': {
        'name': 'obtener_clima',
        'description': 'Obtiene la temperatura, estado del día y viento actual de cualquier ciudad o país.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ciudad': {
                    'type': 'string',
                    'description': 'Nombre de la ciudad (ejemplo: Cúcuta, Bogotá, Madrid, Tokio)',
                },
                'pais': {
                    'type': 'string',
                    'description': 'Nombre del país (opcional, para ser más precisos. Ejemplo: Colombia, España, Japón)',
                },
            },
            'required': ['ciudad'],
        },
    },
}

print("==================================================")
print("🤖 AGENTE METEOROLÓGICO CON HERMES 3 🤖")
print("Escribe una pregunta sobre el clima o 'salir' para terminar.")
print("==================================================\n")

while True:
    pregunta = input("\nTú: ").strip()
    
    if pregunta.lower() in ['salir', 'exit', 'quit']:
        print("\n¡Hasta luego! Agente finalizado.")
        break
        
    if not pregunta:
        continue

    print("\n[Pensando y procesando...]")

    respuesta_inicial = ollama.chat(
        model='hermes3',
        messages=[
            {
                'role': 'system',
                'content': 'Eres un asistente meteorológico. Cuando consultes el clima, responde únicamente con el clima actual proporcionado por la herramienta, de forma breve y directa. No añadas promedios, estaciones, contexto geográfico ni recomendaciones.'
            },
            {'role': 'user', 'content': pregunta}
        ],
        tools=[herramienta_clima]
    )

    mensaje_agente = respuesta_inicial['message']

    if mensaje_agente.get('tool_calls'):
        for tool in mensaje_agente['tool_calls']:
            if tool['function']['name'] == 'obtener_clima':
                args = tool['function']['arguments']
                ciudad_peticion = args.get('ciudad', '')
                pais_peticion = args.get('pais', '')

                print(f"⚙️  [Usando herramienta: consultar clima para '{ciudad_peticion}' {pais_peticion}]")
                
                # Ejecutamos la API
                resultado_api = obtener_clima(ciudad=ciudad_peticion, pais=pais_peticion)

                print(f"\nAgente: {resultado_api}")
    else:
        print(f"\nAgente: {mensaje_agente['content']}")