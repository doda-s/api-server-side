from pymongo import MongoClient
from flask import Flask, jsonify, request

# Conectando a aplicação ao MongoDB
uri = "mongodb+srv://gustavopaterno1:E910vzSF1OYgJI8I@jpg2.oaxxecf.mongodb.net/?retryWrites=true&w=majority&appName=JPG2"
client = MongoClient(uri)
db = client["jpg2"]  
colecao = db["Jogadores"]  

# Iniciando o app
app = Flask(__name__)

# Rota para receber informações dos alunos
@app.route('/api/get/aluno', methods=['GET'])
def get_alunos():
    # list(colecao.find({}, {"_id": 0}))  ->  Significa que está buscando sem nenhum filtro aplicado no MDB
    alunos = list(colecao.find({}, {"_id": 0}))  
    return jsonify(alunos)

# Faz envio dos dados dos jogadores 
@app.route('/api/post/aluno', methods=['POST'])
def post_aluno():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados inválidos"}), 400

    # Recebe as informações
    username = data.get("username")
    password = data.get("password")
    character = data.get("character")
    progresso = data.get("progresso")

    # Faz a verificação se tudo foi preenchido
    if not username or not password or not character or not progresso:
        return jsonify({"erro": "Faltando dados obrigatórios"}), 400

    novo_usuario = {
        "username": username,
        "password": password,
        "character": character,
        "progresso": progresso
    }

    # Cria um jogadore novo dentro da coleção no MDB
    colecao.insert_one(novo_usuario)
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

# Faz a atualização dos jogadores
@app.route('/api/update/aluno', methods=['PUT'])
def update_aluno():
    data = request.json
    username = data.get("username")  # critério de busca
    novo_character = data.get("character")
    novo_progresso = data.get("progresso")

    if not username:
        return jsonify({"message": "Username é obrigatório"}), 400

    # Cria um Dict com os dados novos a serem atualizados
    update_fields = {}
    if novo_character:
        update_fields["character"] = novo_character
    if novo_progresso:
        update_fields["progresso"] = novo_progresso

    if not update_fields:
        return jsonify({"message": "Nada para atualizar"}), 400

    # Atualiza no MDB
    resultado = colecao.update_one(
        {"username": username},
        {"$set": update_fields} # o $set é um operador do MDB que faz a atualiação sem substituir os dados.
    )

    # Faz a verificação se foi modificado ou não
    if resultado.modified_count == 1:
        return jsonify({"mensagem": "Dados do aluno atualizados com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum aluno atualizado. Verifique o username."})

# Exclui um usuário
@app.route('/api/delete/aluno', methods=['DELETE'])
def delete_aluno():
    data = request.json
    username = data.get("username")

    # Verifica se existe ou não
    if not username:
        return jsonify({"message": "info error"})
    
    # Deleta no MDB
    resultado = colecao.delete_one(
        {"username": username}
    )

    # Outra verificação para saber se tudo ocorreu bem
    if resultado.deleted_count == 1:
        return jsonify({"mensagem": "Aluno deletado com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum aluno deletado. Verifique o nome."})

# Faz debug da aplicação
if __name__ == '__main__':
    app.run(debug=True)
