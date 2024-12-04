# Clean refactor

A brief overview of what I'm doing

## Tooling

I'm using mypy for static type checking and pytest for tests.

## Domain layer

This layer is responsible of defining the domain and business rules.

It provides a repository interface that the data layer will implement
to provide access to a data persistency tool such as Postgresql.

It also provides the services that will be used by the application layer.
Each service has unit tests using the fake repositories.
