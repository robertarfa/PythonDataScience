# #Create a app
# #https://developer.x.com/en/apps
import tweepy
from dotenv import load_dotenv
import os
import time

load_dotenv()

bearer =  os.getenv("TwitterBearerToken")

client = tweepy.Client(bearer_token=bearer)  # Inicialização do seu cliente

def make_api_call(query):
    try:
        response = client.search_recent_tweets(query=query, tweet_fields=['created_at'], max_results=10) #Exemplo de chamada à API
        # ... processa os tweets ...
        return response
    except tweepy.TweepyException as e:
        if e.response.status_code == 429:
            print("Limite de taxa atingido. Esperando...")
            retry_after = int(e.response.headers.get('x-rate-limit-reset', 0)) - time.time()
            time.sleep(max(retry_after, 60))  # Espera pelo menos 60 segundos
            print("Tentando novamente...")
            return make_api_call(query) # Chamada recursiva para tentar de novo
        else:
            print(f"Erro na API: {e}")
            return None


# Exemplo de uso:
query = "healthcare"
results = make_api_call(query)
if results:
    # ... processa os dados ...
    for tweet in results.data:
        print(tweet.text)

        