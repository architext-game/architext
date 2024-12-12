# Clean refactor

A brief overview of what I'm doing so I don't get lost.
ATM is more like a desired state that a description of the current
system.


## Tooling

I'm using mypy for static type checking and pytest for tests.


# Project structure

architext/
  core/  # only depends on ports
    domain/
      entities/
      events/
    services/
    handlers/
    messagebus/
  ports/  # we may have to separate "in" and "out" ports in the future
    unit_of_work/
    room_repository/
    user_repository/
    notificator/
  adapters/
    socketio_notificator/
    aqlalchemy_uow/
    sqlalchemy_user_repository/
    sqlalchemy_room_repository/
  entrypoints/
    socketio_server/




# Core

This is the part of the app that does not depend on the outside world.
The only other part of the app that Core can depend on is the code in
the Ports folder.

## Domain layer

This layer is responsible of defining the entities present in the domain
and the rules that they obey (business rules). At the time of writting,
those are
 - User, an aggregate root
 - Room, an aggregate root
 - Exit, part of the Room aggregate

 It also defines events and when they happen (ussually when something
 is done to some entity).


## Service layer

This layer defines the Services: actions that the users can do to the 
domain entities. Also defines handlers: very similar to services, but
they are triggered when a certain domain event happens. Both concepts
will be merged at the right time. 

It provides a repository interface that the services and handlers will
use to access and persist data.

It provides a 

The Unit of Work is the vehicle used by the services to access the repositories.
It also abstracts the concept of transactions


## Adapters layer

Here lives all the code depending on external libraries and tools that will be
actively used by the service layer, like sending email or accessing a database.


## Entrypoints layer

This contains the python scripts that will put the rest of the system to use.
For example, an entrypoint may start an API REST that gives access to the
services.

## Concerns

Not sure if I should be using ABC instead of Protocol.
