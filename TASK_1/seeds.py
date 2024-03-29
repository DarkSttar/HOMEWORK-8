from models import Author, Quote
from datetime import datetime
import connect
import json

with open("author.json", "r") as file:
    author_data = json.load(file)

with open("quotes.json", "r") as file:
    quotes_data = json.load(file)


def save_authors(data):
    for dt in data:
        author = Author(
            fullname=dt["fullname"],
            born_date=datetime.strptime(dt["born_date"], "%B %d, %Y"),
            born_location=dt["born_location"],
            description=dt["description"],
        )
        author.save()
    return "Authors Saved!"


def find_author_id(name):
    authors = Author.objects()
    for author in authors:
        if author.fullname == name:
            return author.id


def save_quotes(quotes_data):
    for dt in quotes_data:
        quote = Quote(
            tags=dt["tags"], author=find_author_id(dt["author"]), quote=dt["quote"]
        )
        quote.save()
    return "Quotes Saved!"


if __name__ == "__main__":
    save_authors(author_data)
    save_quotes(quotes_data)
