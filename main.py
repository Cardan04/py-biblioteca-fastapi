from fastapi import FastAPI, HTTPException
import random
import json
import os
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book(BaseModel):
    nome: str
    price: float
    genero: Literal['Ficção', 'Nao Ficção']
    book_id: Optional[str] = None


BOOKS_FILES = 'books.json'


# Carregar ou iniciar arquivo JSON
if os.path.exists(BOOKS_FILES):
    with open(BOOKS_FILES, "r") as f:
        BOOK_DATABASE = json.load(f)
else:
    BOOK_DATABASE = []


# ------------------ GET -------------------------

@app.get('/')
async def home():
    return 'Seja bem vindo à nossa livraria!' 


@app.get('/list-books')
async def list_books():
    return {'Books': BOOK_DATABASE}


@app.get('/list-book-by-index/{index}')
async def list_book_by_index(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(404, 'Index fora do range')
    return {'Book': BOOK_DATABASE[index]}


@app.get('/random-book')
async def random_book():
    if not BOOK_DATABASE:
        raise HTTPException(404, "Nenhum livro cadastrado")
    return random.choice(BOOK_DATABASE)



# ------------------ POST -------------------------

@app.post('/add-book')
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)

    with open(BOOKS_FILES, 'w') as f:
        json.dump(BOOK_DATABASE, f, indent=4)

    return {'mensagem': f'Livro "{book.nome}" foi adicionado com sucesso!', 'book_id': book.book_id}


'''
Para executar é necessario executar esse cmando: uvicorn main:app --reload
'''