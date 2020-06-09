import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    print(csv.Sniffer().has_header(f.read(5000)))
    f.seek(1)
    reader = csv.reader(f)

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO tb_books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added ISBN {isbn}, title {title}, author {author} and year {year}")
    db.commit()

if __name__ == "__main__":
    main()
