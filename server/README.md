# PYTHON VERSION 3.12.8

# Clean refactor

A brief overview of what I'm doing so I don't get lost.


# Tooling

I'm using mypy for static type checking and pytest for tests.


# Project structure

I'll be adding docstrings to modules, check them out.


## Core

The business logic. See its docstrings.


## Ports

Defines the interfaces used by the `Core` to access the outside world.


## Adapters

Containts implementations for the `Ports`.


## Entrypoints

This contains the modules that initialize the `Adapters` and drive the `Core`.


# Concerns

 - Not sure if I should be using ABC instead of Protocol.
