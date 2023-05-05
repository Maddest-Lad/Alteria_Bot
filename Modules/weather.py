import aiohttp

WWO_CODE = {
    "113": "Sunny",
    "116": "PartlyCloudy",
    "119": "Cloudy",
    "122": "VeryCloudy",
    "143": "Fog",
    "176": "LightShowers",
    "179": "LightSleetShowers",
    "182": "LightSleet",
    "185": "LightSleet",
    "200": "ThunderyShowers",
    "227": "LightSnow",
    "230": "HeavySnow",
    "248": "Fog",
    "260": "Fog",
    "263": "LightShowers",
    "266": "LightRain",
    "281": "LightSleet",
    "284": "LightSleet",
    "293": "LightRain",
    "296": "LightRain",
    "299": "HeavyShowers",
    "302": "HeavyRain",
    "305": "HeavyShowers",
    "308": "HeavyRain",
    "311": "LightSleet",
    "314": "LightSleet",
    "317": "LightSleet",
    "320": "LightSnow",
    "323": "LightSnowShowers",
    "326": "LightSnowShowers",
    "329": "HeavySnow",
    "332": "HeavySnow",
    "335": "HeavySnowShowers",
    "338": "HeavySnow",
    "350": "LightSleet",
    "353": "LightShowers",
    "356": "HeavyShowers",
    "359": "HeavyRain",
    "362": "LightSleetShowers",
    "365": "LightSleetShowers",
    "368": "LightSnowShowers",
    "371": "HeavySnowShowers",
    "374": "LightSleetShowers",
    "377": "LightSleet",
    "386": "ThunderyShowers",
    "389": "ThunderyHeavyRain",
    "392": "ThunderySnowShowers",
    "395": "HeavySnowShowers",
}

WEATHER_SYMBOL = {
    "Unknown":             "✨",
    "Cloudy":              "☁️",
    "Fog":                 "🌫",
    "HeavyRain":           "🌧",
    "HeavyShowers":        "🌧",
    "HeavySnow":           "❄️",
    "HeavySnowShowers":    "❄️",
    "LightRain":           "🌦",
    "LightShowers":        "🌦",
    "LightSleet":          "🌧",
    "LightSleetShowers":   "🌧",
    "LightSnow":           "🌨",
    "LightSnowShowers":    "🌨",
    "PartlyCloudy":        "⛅️",
    "Sunny":               "☀️",
    "ThunderyHeavyRain":   "🌩",
    "ThunderyShowers":     "⛈",
    "ThunderySnowShowers": "⛈",
    "VeryCloudy": "☁️",
}

HOST = 'wttr.in'

 
# Json Format J1 gives all data while J2 gives just current 
async def get_weather_forecast(location, json_format='j1'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'https://{HOST}/{location}?format={json_format}') as promise:  # Get Data Formatted as JSON
            return await promise.json()          

async def get_current_report(location):
    current = (await get_weather_forecast(location, json_format='j2'))['current_condition'][0]   
      
    return f"""Current Weather Report
> Feels Like: {current['FeelsLikeF']}f
> Weather: {WEATHER_SYMBOL[WWO_CODE[current['weatherCode']]]} {current['weatherDesc'][0]['value']}
> Cloud Cover: {current['cloudcover']}%
> Humidity: {current['humidity']}%
    """ # this formatting kills me

# async def get_forecast(location):
#     forecast = await get_weather_forecast(location)
#     for key in forecast['weather'][0]['hourly']:
#         print(key['chanceofrain'])
        
#     return 


if __name__ == '__main__':
    import asyncio
    location = 'Maple+Valley'
    
    data = asyncio.run(get_weather_forecast(location))
    report = asyncio.run(get_current_report(location))
    #forecast = asyncio.run(get_forecast(location))
    
    print(report)