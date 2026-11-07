from fastapi import FastAPI, HTTPException
from pydantic import BaseModel , Field

app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "Марсианин",
        "director": "Ридли Скотт",
        "year": 2015
    },
    {
        "id": 2,
        "title": "Интерстеллар",
        "director": "Кристофер Нолан",
        "year": 2014
    },
]

class Movie(BaseModel):
    id: int
    title:str
    year: int
    director: str

class MovieCreate(BaseModel):
    title:str = Field(min_length = 2 )
    year: int = Field(ge = 1900 , le = 2030)
    director: str = Field(min_length=2)

@app.get("/movies", response_model=list[Movie])
def get_movies():
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(status_code=404,detail="Фильм не найден", )

@app.post("/movies", response_model=Movie, status_code=201)
def create_movie(movie: MovieCreate):
    for saved_movie in movies:
        if saved_movie["name"].lower() == movie.name.lower():
            raise HTTPException(status_code=400,detail="Фильм с таким названием уже существует",)
    new_movie = movie.model_dump()
    new_movie["id"] = len(movies) + 1
    movies.append(new_movie)
    return new_movie
