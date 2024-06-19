---

# BookSpace - API de Cadastro de Livros

Este é o README do projeto de API web **BookSpace**, desenvolvido para a disciplina de Programação WEB. A API BookSpace oferece funcionalidades essenciais para o cadastro, edição e gerenciamento de livros, assim como para o gerenciamento de usuários.

## Funcionalidades

- **Cadastro de Livros**: Permite o cadastro de novos livros na base de dados.
- **Deletar Livros**: Permite a exclusão de livros cadastrados.
- **Editar Livros**: Permite a atualização das informações dos livros.
- **Cadastro de Usuários**: Implementa a funcionalidade de cadastro de novos usuários.
- **Login de Usuários**: Permite que usuários registrados façam login no sistema.

## Requisitos

- **Python e SQLAlchemy**: O projeto é inteiramente implementado utilizando Python e SQLAlchemy para a manipulação do banco de dados.
- **Banco de Dados**: Utiliza SQLite como banco de dados relacional.
- **Interface Web**: Utiliza HTML (Jinja2 templates), CSS e TailwindCSS para a interface visual.

## Uso da API

### Endpoints Principais

- **/cadastro** (POST)
  - Cadastro de novos livros.
  - **Parâmetros**: `titulo`, `autor`, `editora`, `idioma`, `sinopse`, `imagem`, `tipo_imagem`.
  - **Exemplo**: 
    ```json
    {
      "titulo": "O Livro da Alegria",
      "autor": "Dalai Lama",
      "editora": "Editora XYZ",
      "idioma": "Português",
      "sinopse": "Uma conversa inspiradora entre o Dalai Lama e Desmond Tutu.",
      "imagem": "/caminho/para/imagem.jpg",
      "tipo_imagem": "image/jpeg"
    }
    ```

- **/deletar/{id}** (DELETE)
  - Deleta um livro com base no ID fornecido.
  - **Exemplo**: `/deletar/1`

- **/editar/{id}** (PUT)
  - Atualiza as informações de um livro com base no ID fornecido.
  - **Parâmetros**: Mesmos parâmetros do cadastro, todos opcionais.
  - **Exemplo**:
    ```json
    {
      "titulo": "O Livro da Alegria - Edição Revisada",
      "autor": "Dalai Lama",
      "editora": "Editora ABC",
      "idioma": "Português",
      "sinopse": "Uma conversa ainda mais inspiradora entre o Dalai Lama e Desmond Tutu.",
      "imagem": "/caminho/para/imagem_nova.jpg",
      "tipo_imagem": "image/jpeg"
    }
    ```

- **/usuarios/cadastro** (POST)
  - Cadastro de novos usuários.
  - **Parâmetros**: `nome`, `email`, `password`.
  - **Exemplo**:
    ```json
    {
      "nome": "Ana",
      "email": "ana@email.com",
      "password": "senha_segura"
    }
    ```

- **/usuarios/login** (POST)
  - Login de usuários.
  - **Parâmetros**: `email`, `password`.
  - **Exemplo**:
    ```json
    {
      "email": "ana@email.com",
      "password": "senha_segura"
    }
    ```

## Instalação

### Requisitos Pré-Requisitos

- **Python 3**: Assegure-se de ter o Python 3 instalado em seu sistema.

### Passo a Passo de Instalação

1. **Clone o projeto**

   ```bash
   git clone https://github.com/oBrunoz/ProjetoFinal_ProgWeb.git
   ```

2. **Crie um ambiente virtual**

   ```bash
   pip install virtualenv
   virtualenv venv
   ```

3. **Ative o ambiente virtual e instale as dependências**

   ```bash
   source venv/Scripts/activate  # No Windows
   source venv/bin/activate  # No Linux/MacOS
   pip install -r requirements.txt
   ```

5. **Inicie o servidor**

   ```bash
   fastapi dev main.py
   ```

