#!/usr/bin/python

import xmltodict
import requests
import omdb
import json


xml_url = 'http://www.cinemark.com.br/programacao.xml'
r = requests.get(xml_url)
xml = xmltodict.parse(r.text)

def get_in_theaters_movies_list():
	movies = []
	for cinemark_movie in xml['cinemark']['programacao']['filmes']['filme']:
		movie_entry = {}

		movie_entry['title'] = cinemark_movie['titulo_original']
		movie_entry['title_br'] = cinemark_movie['titulo_portugues']
		imdb_search = omdb.search_movie(movie_entry['title'])
		if imdb_search:
			imdb_movie = omdb.get(title = imdb_search[0].title, tomatoes = True)
			if imdb_movie:
				movie_entry['poster'] = imdb_movie.poster
				movie_entry['genre'] = imdb_movie.genre
				movie_entry['awards'] = imdb_movie.awards
				movie_entry['runtime'] = imdb_movie.runtime
				movie_entry['metascore'] = imdb_movie.metascore
				movie_entry['imdb_rating'] = imdb_movie.imdb_rating
				movie_entry['tomato_rating'] = imdb_movie.tomato_rating

		movies.append(movie_entry)

	return movies

def get_in_theaters_movies_json():
	return json.dumps(get_in_theaters_movies_list())

if __name__ == "__main__":
	print get_in_theaters_movies_json()