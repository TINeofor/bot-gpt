from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openai

# Configurar a API da OpenAI
openai.api_key = "SUA_API_KEY"

def gerar_resposta(mensagem):
    # Envia a mensagem para o ChatGPT e retorna a resposta
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": mensagem}]
    )
    return response['choices'][0]['message']['content']

def iniciar_bot():
    # Configurar o navegador
    driver = webdriver.Chrome()
    driver.get("https://chat.neofor.com.br/chat/U9M1HU?chatConnectionId=IMD1JW")

    # Esperar o chat carregar (ajuste conforme necessário)
    time.sleep(10)

    # Loop para monitorar novas mensagens
    while True:
        try:
            # Localizar a última mensagem recebida no chat
            mensagens = driver.find_elements(By.CLASS_NAME, "nome-classe-mensagem")
            ultima_mensagem = mensagens[-1].text

            # Gerar uma resposta com ChatGPT
            resposta = gerar_resposta(ultima_mensagem)

            # Enviar a resposta no chat
            campo_input = driver.find_element(By.CLASS_NAME, "nome-classe-input")
            campo_input.send_keys(resposta + Keys.RETURN)

            # Aguardar antes de verificar novas mensagens
            time.sleep(5)

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_bot()
