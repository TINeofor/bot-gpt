from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openai import OpenAI

# Configurar a API do OpenAI
client = OpenAI(api_key="SUA_CHAVE_API")

def gerar_resposta(mensagem):
    """
    Gera uma resposta para a mensagem usando o modelo GPT-4.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            store=True,
            messages=[
                {"role": "user", "content": mensagem}
            ]
        )
        return completion['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."

def iniciar_bot(usuario, senha):
    """
    Inicializa o bot, realiza login e interage com o chat.
    """
    try:
        # Configurar o navegador
        driver = webdriver.Chrome()
        driver.get("https://chat.neofor.com.br/chat/U9M1HU?chatConnectionId=IMD1JW")

        print("Realizando login...")
        time.sleep(3)

        # Localize os campos de login e insira os dados
        campo_usuario = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))  # Substitua pelo seletor correto se necessário
        )
        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))  # Substitua pelo seletor correto se necessário
        )

        campo_usuario.send_keys(usuario)
        campo_senha.send_keys(senha)

        # Aguarde o botão de login ser habilitado e clique
        botao_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'Entrar')]]"))
        )
        botao_login.click()

        print("Login realizado com sucesso. Bot iniciado. Monitorando mensagens...")

        # Aguarde a navegação para o chat após o login
        time.sleep(10)

        # Loop principal para monitorar o chat
        while True:
            try:
                # Substitua "nome-classe-mensagem" pelo nome correto da classe das mensagens
                mensagens = driver.find_elements(By.CLASS_NAME, "nome-classe-mensagem")  
                ultima_mensagem = mensagens[-1].text if mensagens else ""

                if ultima_mensagem:
                    print(f"Mensagem recebida: {ultima_mensagem}")

                    resposta = gerar_resposta(ultima_mensagem)
                    print(f"Resposta gerada: {resposta}")

                    # Substitua "nome-classe-input" pelo seletor correto do campo de entrada de texto
                    campo_input = driver.find_element(By.CLASS_NAME, "nome-classe-input")  
                    campo_input.send_keys(resposta + Keys.RETURN)

                time.sleep(5)

            except Exception as e:
                print(f"Erro no loop principal: {e}")
                time.sleep(5)

    except Exception as e:
        print(f"Erro ao iniciar o bot: {e}")

if __name__ == "__main__":
    usuario = input("Digite seu usuário: ")
    senha = input("Digite sua senha: ")

    iniciar_bot(usuario, senha)
