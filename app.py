from flask import Flask, render_template, request, jsonify
import openai
import os

# Configuração da API Key do OpenAI (usando variável de ambiente)
openai.api_key = os.getenv('OPENAI_API_KEY')  # Certifique-se de definir a variável de ambiente 'OPENAI_API_KEY'

# Criação do aplicativo Flask
app = Flask(__name__, template_folder="templates")

# Dicionário de sabores de pizza e seus valores
pizzas = {
    "marguerita": 25.00,
    "pepperoni": 30.00,
    "quatro queijos": 35.00,
    "calabresa": 28.00,
    "vegetariana": 27.00
}

# Dicionário de respostas para comprimentos e saudações
greetings = {
    "oi": "Olá! Como posso ajudar você hoje?",
    "olá": "Olá! O que você precisa?",
    "tudo bem": "Estou bem, obrigado! E você?",
    "como vai": "Vai bem, obrigado por perguntar! Como posso ajudar?",
    "boa tarde": "Boa tarde! Em que posso ajudar?",
    "bom dia": "Bom dia! O que você precisa hoje?",
    "boa noite": "Boa noite! Como posso ajudar?"
}

# Função que retorna respostas do chatbot com base na entrada do usuário
def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Verifica saudações e comprimentos
    if user_input in greetings:
        return greetings[user_input]
    
    # Verifica se a entrada do usuário contém uma pergunta sobre pizzas
    if "pizza" in user_input:
        for flavor, price in pizzas.items():
            if flavor in user_input:
                return f"A pizza de {flavor} custa R${price:.2f}."
        
        # Se não encontrar o sabor específico, retorna todos os sabores e preços
        return "Aqui estão os preços das pizzas disponíveis:\n" + "\n".join([f"A pizza de {flavor} custa R${price:.2f}." for flavor, price in pizzas.items()])
    
    # Caso não seja uma saudação ou sobre pizza, usa a API do OpenAI
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Você pode escolher um modelo diferente se preferir
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")  # Registra o erro
        return "Desculpe, houve um erro ao processar sua solicitação."

# Rota principal que renderiza a página inicial
@app.route("/")
def home():
    return render_template("index.html")

# Rota para processar as mensagens enviadas pelo usuário
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form.get("msg", "")  # Usa o get para evitar KeyError
    response = chatbot_response(user_input)
    return jsonify({"response": response})

# Executa o aplicativo Flask
if __name__ == "__main__":
    app.run(debug=True)
