import strawberry
from strawberry.asgi import GraphQL
import uvicorn

@strawberry.type
class Book:
    title: str
    author: str

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return [
            Book(
                title="Distributed Systems",
                author="Andrew S. Tanenbaum",
            ),
            Book(
                title="The Pragmatic Programmer",
                author="David Thomas",
            ),
        ]

schema = strawberry.Schema(query=Query)
app = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)