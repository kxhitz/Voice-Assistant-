from ipaddress import ip_address
import requests
import wikipedia
import pywhatkit as kit

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def get_news():
    news_headline = []
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=0c7f14b40523459d9017c2806cda36c4"
        )
        result = response.json()
        articles = result.get("articles", [])
        for article in articles:
            news_headline.append(article.get("title", "No Title"))
        return news_headline[:6]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return ["Sorry, I'm unable to fetch the news right now."]

def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=ff949e19518b92bf17ba48d8d0ea2eff&units=metric"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"