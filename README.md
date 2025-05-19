# 🧠 Projeto API de Usuários - Flask + MongoDB

Este projeto é uma API desenvolvida em Python com Flask que realiza operações CRUD (Create, Read, Update, Delete) em um banco de dados MongoDB, gerenciando usuários do tipo "jogadores", contendo informações de login, personagem e progresso no jogo.

---

## 🚀 Tecnologias utilizadas

- Python 3.13.2
- Flask
- MongoDB (MongoDB Atlas)
- Pymongo

---

## 📁 Estrutura do Usuário

Cada usuário (jogador) possui os seguintes dados:

```json
{
  "username": "joaodasilva",
  "password": "senhaSegura123",
  "character": {
    "nome": "Jogador",
    "idade": 25,
    "genero": "Masculino",
    "nivel": "Estagiário",
    "profissao": "Advogado"
  },
  "progresso": {
    "confianca": 80,
    "casos_perdidos": 2,
    "casos_resolvidos": 5,
    "fase": 3
  }
}
