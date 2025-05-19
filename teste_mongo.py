from pymongo import MongoClient
from flask import Flask, jsonify, request

uri = "mongodb+srv://gustavopaterno1:E910vzSF1OYgJI8I@jpg2.oaxxecf.mongodb.net/?retryWrites=true&w=majority&appName=JPG2"
client = MongoClient(uri)
db = client["jpg2"]  
colecao = db["Jogadores"]  

app = Flask(__name__)

@app.route('/api/get/aluno', methods=['GET'])
def get_alunos():
    alunos = list(colecao.find({}, {"_id": 0}))  
    return jsonify(alunos)

@app.route('/api/post/aluno', methods=['POST'])
def post_aluno():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados inválidos"}), 400

    username = data.get("username")
    password = data.get("password")
    character = data.get("character")
    progresso = data.get("progresso")

    if not username or not password or not character or not progresso:
        return jsonify({"erro": "Faltando dados obrigatórios"}), 400

    novo_usuario = {
        "username": username,
        "password": password,
        "character": character,
        "progresso": progresso
    }

    colecao.insert_one(novo_usuario)
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

@app.route('/api/update/aluno', methods=['PUT'])
def update_aluno():
    data = request.json
    username = data.get("username")  # critério de busca
    novo_character = data.get("character")
    novo_progresso = data.get("progresso")

    if not username:
        return jsonify({"message": "Username é obrigatório"}), 400

    update_fields = {}
    if novo_character:
        update_fields["character"] = novo_character
    if novo_progresso:
        update_fields["progresso"] = novo_progresso

    if not update_fields:
        return jsonify({"message": "Nada para atualizar"}), 400

    resultado = colecao.update_one(
        {"username": username},
        {"$set": update_fields}
    )

    if resultado.modified_count == 1:
        return jsonify({"mensagem": "Dados do aluno atualizados com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum aluno atualizado. Verifique o username."})

@app.route('/api/delete/aluno', methods=['DELETE'])
def delete_aluno():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"message": "info error"})
    
    resultado = colecao.delete_one(
        {"username": username}
    )

    if resultado.deleted_count == 1:
        return jsonify({"mensagem": "Aluno deletado com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum aluno deletado. Verifique o nome."})


if __name__ == '__main__':
    app.run(debug=True)
