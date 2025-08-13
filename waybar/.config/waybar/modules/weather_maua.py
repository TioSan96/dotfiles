#!/usr/bin/env python3
import requests
import json
import sys
import math

API_KEY = "36ce662c103dd416392fcf2f044b640d"
CITY = "Maua,BR"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br"

def calcular_ponto_orvalho(temp, humidity):
    # Fórmula de Magnus para ponto de orvalho
    a = 17.27
    b = 237.7
    alpha = ((a * temp) / (b + temp)) + math.log(humidity/100.0)
    dew_point = (b * alpha) / (a - alpha)
    return dew_point

try:
    response = requests.get(URL, timeout=5)
    data = response.json()
    temp = data['main']['temp']
    desc = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    feels_like = data['main']['feels_like']
    wind_speed = data['wind']['speed']
    # Calcula o ponto de orvalho
    dew_point = calcular_ponto_orvalho(temp, humidity)
    # Tooltip simples, sem HTML
    tooltip = (
        f"Clima em Mauá-SP\n"
        f"Temperatura: {temp:.1f}°C\n"
        f"Sensação: {feels_like:.1f}°C\n"
        f"Umidade: {humidity}%\n"
        f"Vento: {wind_speed} m/s\n"
        f"Ponto de orvalho: {dew_point:.1f}°C\n"
        f"Descrição: {desc}"
    )
    text = f"{temp:.1f}°C - Mauá - SP"
    print(json.dumps({"text": text, "tooltip": tooltip}))
except Exception as e:
    print(json.dumps({"text": "Erro clima", "tooltip": "Erro ao obter clima"})) 