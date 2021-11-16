from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String, Text

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Tree(BaseModel):
    tree_id: str
    text: str

    class Config:
        orm_mode = True


class DBTree(Base):
    __tablename__ = "trees"

    tree_id = Column(String, primary_key=True, index=True)
    text = Column(Text)


Base.metadata.create_all(bind=engine)


# Methods for interacting with the database
def get_tree(db: Session, tree_id: str):
    return db.query(DBTree).where(DBTree.tree_id == tree_id).first()


def get_trees(db: Session):
    return db.query(DBTree).all()


def create_tree(db: Session, tree: Tree):
    db_tree = DBTree(**tree.dict())
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)

    return db_tree


@app.post("/trees/", response_model=Tree)
def create_trees_view(tree: Tree, db: Session = Depends(get_db)):
    db_tree = create_tree(db, tree)
    return db_tree


@app.get("/trees/", response_model=List[Tree])
def get_trees_view(db: Session = Depends(get_db)):
    return get_trees(db)


@app.get("/tree/{tree_id}")
def get_tree_view(tree_id: str, db: Session = Depends(get_db)):
    return get_tree(db, tree_id)


@app.post("/trees/")
async def create_tree_view(tree: Tree):
    return tree
