from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    genre = Genre(id=1, name="test_genre")
    director = Director(id=1, name="test_director")

    movie_1 = Movie(id=1, title="test movie 1", description="test movie 1", trailer="test movie 1", year=2021,
                    rating=10, genre=genre, director=director)
    movie_2 = Movie(id=2, title="test movie 2", description="test movie 2", trailer="test movie 2", year=2022, rating=9,
                    genre=genre, director=director)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_data = {
            "title": "test movie 3",
            "description": "test movie 3",
            "trailer": "test movie 3",
            "year": 2020,
            "rating": 8,
        }
        movie = self.movie_service.create(movie_data)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_data = {
            "id": 2,
            "title": "test movie 3",
            "description": "test movie 3",
            "trailer": "test movie 3",
            "year": 2020,
            "rating": 8,
        }
        self.movie_service.update(movie_data)
