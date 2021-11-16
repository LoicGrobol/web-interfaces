from typing import List
import sqlite3

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


def get_db():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    try:
        yield cur
        con.commit()
    finally:
        cur.close()
        con.close()


# Database setup
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
cur.execute(
    "create table if not exists trees (tree_id VARCHAR NOT NULL PRIMARY KEY, text TEXT)"
)
con.close()


class Tree(BaseModel):
    tree_id: str
    text: str


# Methods for interacting with the database
def get_tree(cur: sqlite3.Cursor, tree_id: str):
    cur.execute("select * from trees where tree_id=:tree_id", {"tree_id": tree_id})
    db_tree_id, db_text = cur.fetchone()
    return {"tree_id": db_tree_id, "text": db_text}


def get_trees(cur: sqlite3.Cursor):
    cur.execute("select * from trees")
    return [
        {"tree_id": db_tree_id, "text": db_text}
        for db_tree_id, db_text in cur.fetchall()
    ]


def create_tree(cur: sqlite3.Cursor, tree: Tree):
    cur.execute(
        "insert into trees values (:tree_id, :text)",
        {"tree_id": tree.tree_id, "text": tree.text},
    )
    return tree


@app.post("/trees/", response_model=Tree)
def create_trees_view(tree: Tree, db: sqlite3.Cursor = Depends(get_db)):
    db_tree = create_tree(db, tree)
    return db_tree


@app.get("/trees/", response_model=List[Tree])
def get_trees_view(db: sqlite3.Cursor = Depends(get_db)):
    return get_trees(db)


@app.get("/tree/{tree_id}")
def get_tree_view(tree_id: str, db: sqlite3.Cursor = Depends(get_db)):
    return get_tree(db, tree_id)


@app.post("/trees/")
async def create_tree_view(tree: Tree):
    return tree


@app.get("/")
async def root():
    return {"message": "Hello World!"}
