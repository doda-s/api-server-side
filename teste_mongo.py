from pymongo import MongoClient
from flask import Flask, jsonify, request

# Conectando a aplicação ao MongoDB
uri = "mongodb+srv://gustavopaterno1:E910vzSF1OYgJI8I@jpg2.oaxxecf.mongodb.net/?retryWrites=true&w=majority&appName=JPG2"

client = MongoClient(uri)
db = client["jpg2"]  
jogadores = db["Jogadores"]  
fases = db["Fases"]
npc = db["NPCs"]

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

    new_usuario = {
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
    new_character = data.get("character")
    new_progresso = data.get("progresso")

    if not username:
        return jsonify({"message": "Username é obrigatório"}), 400

    # Cria um Dict com os dados novos a serem atualizados
    update_fields = {}
    if new_character:
        update_fields["character"] = new_character
    if new_progresso:
        update_fields["progresso"] = new_progresso

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

@app.route('/api/get/fases', methods=['GET'])
def get_fases():
    alunos = list(fases.find({}, {"_id": 0}))  
    return jsonify(alunos)

@app.route('/api/post/fases', methods=['POST'])
def post_fases():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados inválidos"}), 400

    name = data.get("name")
    level = data.get("level")
    description = data.get("description")

    if not name or not description or not level:
        return jsonify({"erro": "Faltando dados obrigatórios"}), 400

    new_fase = {
        "name": name,
        "description": description,
        "level": level
    }

    fases.insert_one(new_fase)
    return jsonify({"mensagem": "fase criada com sucesso!"}), 201

@app.route('/api/update/fases', methods=['PUT'])
def update_fases():
    data = request.json
    level = data.get("level")  # critério de busca
    new_name = data.get("new_name")
    new_description = data.get("new_description")
    new_level = data.get("new_level")

    if not level or not new_name or not new_description or not new_level:
        return jsonify({"message": "Username é obrigatório"}), 400

    update_fields = {}
    if new_name:
        update_fields["name"] = new_name
    if new_description:
        update_fields["description"] = new_description
    if new_level:
        update_fields["level"] = new_level

    if not update_fields:
        return jsonify({"message": "Nada para atualizar"}), 400

    resultado = fases.update_one(
        {"level": level},
        {"$set": update_fields}
    )

    if resultado.modified_count == 1:
        return jsonify({"mensagem": "Dados da fase atualizadas com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhuma fase atualizada. Verifique o username."})

@app.route('/api/delete/fases', methods=['DELETE'])
def delete_fases():
    data = request.json
    level = data.get("level")
    username = data.get("username")

    if not level:
        return jsonify({"message": "info error"})
    
    resultado = fases.delete_one(
        {"level": level}
    )

    if resultado.deleted_count == 1:
        return jsonify({"mensagem": "fase deletada com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhuma fase deletada. Verifique os campos."})
    

#NPCs
@app.route('/api/get/npc', methods=['GET'])
def get_npc():
    alunos = list(npc.find({}, {"_id": 0}))  
    return jsonify(alunos)

@app.route('/api/post/npc', methods=['POST'])
def post_npc():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    position = data.get("position")
    profession = data.get("profession")

    if not name or not age or not gender or not position or not profession:
        return jsonify({"erro": "Faltando dados obrigatórios"}), 400

    new_npc = {
        "name": name,
        "age": age,
        "gender": gender,
        "position": position,
        "profession": profession
    }

    npc.insert_one(new_npc)
    return jsonify({"mensagem": "npc criada com sucesso!"}), 201

@app.route('/api/update/npc', methods=['PUT'])
def update_npc():
    data = request.json
    name = data.get("name")
    new_name = data.get("new_name")
    new_age = data.get("new_age")
    new_gender = data.get("new_gender")
    new_position = data.get("new_position")
    new_profession = data.get("new_profession")

    if not name or not new_name or not new_age or not new_gender or not new_position or not new_profession:
        return jsonify({"erro": "Faltando dados obrigatórios"}), 400
    
    update_fields = {}
    if new_name:
        update_fields["name"] = new_name
    if new_age:
        update_fields["age"] = new_age
    if new_gender:
        update_fields["gender"] = new_gender
    if new_position:
        update_fields["position"] = new_position
    if new_profession:
        update_fields["profession"] = new_profession

    if not update_fields:
        return jsonify({"message": "Nada para atualizar"}), 400

    resultado = npc.update_one(
        {"name": name},
        {"$set": update_fields}
    )

    if resultado.modified_count == 1:
        return jsonify({"mensagem": "Dados do npc atualizados com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum npc atualizado. Verifique o username."})

@app.route('/api/delete/npc', methods=['DELETE'])
def delete_npc():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"message": "info error"})
    
    resultado = npc.delete_one(
        {"name": name}
    )

    if resultado.deleted_count == 1:
        return jsonify({"mensagem": "npc deletado com sucesso!"})
    else:
        return jsonify({"mensagem": "Nenhum npc deletado. Verifique os campos."})

if __name__ == '__main__':
    app.run(debug=True)
