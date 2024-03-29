import connect
from models import Author, Quote
import re
import sys


def getAuthorIDS(name):
    result = Author.objects(fullname__icontains=name)
    return result


def searchByAuthorName(name):
    authors = getAuthorIDS(name)
    result = []
    answer = Quote.objects(author__in=authors)
    for ans in answer:
        result.append("-" * 100)
        result.append(
            f"Author: {ans.author.fullname}\nTags: {ans.tags}\nQuote{ans.quote}"
        )
    return result


def searchbyTag(tag):
    result = []
    pattern = re.compile(f".*{tag}*.", re.IGNORECASE)
    answer = Quote.objects(tags__in=[pattern])
    for ans in answer:
        result.append("-" * 100)
        result.append(
            f"Author: {ans.author.fullname}\nTags: {ans.tags}\nQuote{ans.quote}"
        )
    return result


def searchByTags(tags: list):

    result = []
    answer = Quote.objects(tags__all=tags)
    for ans in answer:
        result.append("-" * 100)
        result.append(
            f"Author: {ans.author.fullname}\nTags: {ans.tags}\nQuote{ans.quote}"
        )
    return result


commands = {
    "name": searchByAuthorName,
    "tag": searchbyTag,
    "tags": searchByTags,
    "testname": getAuthorIDS,
}
if __name__ == "__main__":
    while True:
        command = input("tap command:")
        if command == "exit":
            sys.exit(0)
        try:
            cmd, args = command.split(":")
            if "," in args:
                args = args.split(",")
            result = commands[cmd](args)
            for r in result:
                print(r)
        except ValueError:
            print("Invalid input, please try again!")
        except KeyError:
            print("Invalid input, please try again!")
