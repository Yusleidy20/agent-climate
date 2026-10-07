# 🤖 Local AI Weather Agent (Hermes 3 + Ollama + Python)

Agente de inteligencia artificial ejecutado de forma 100% local capaz de interpretar consultas en lenguaje natural, tomar decisiones autónomas e invocar herramientas externas mediante **Function Calling** para obtener datos meteorológicos en tiempo real.

## 🚀 Características

- **Modelo Local:** Utiliza `Hermes 3` orquestado a través de **Ollama**.
- **Function Calling / Tool Use:** El modelo analiza la pregunta y decide cuándo llamar a las funciones de Python.
- **APIs REST en vivo:** Consulta las APIs públicas de `Open-Meteo` (Geocoding y Weather API) sin necesidad de credenciales o claves API.
- **Mapeo WMO:** Decodifica códigos meteorológicos internacionales a descripciones legibles en español.
- **CLI Interactivo:** Interfaz de línea de comandos continua para realizar múltiples consultas.

## 🛠️ Tecnologías utilizadas

- **Lenguaje:** Python 3.10+
- **LLM:** Hermes 3 (por Nous Research)
- **Runtime de IA:** Ollama
- **Librerías:** `ollama`, `urllib`, `json`
- **API Meteorológica:** Open-Meteo API

## 📋 Requisitos previos

1. Tener instalado [Ollama](https://ollama.com/).
2. Descargar el modelo `hermes3`:
   ```bash
   ollama run hermes3