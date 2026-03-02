# Getting Started

First of all we have to admit due to our app having multiple entrypoints, our
app is a [modular monolith app](https://www.geeksforgeeks.org/system-design/what-is-a-modular-monolith/).
When we are developing modular monolith app, we have huge bunch of reusable
code. This reusable code makes next entrypoint implementation much easier. For
example you have your first web application and you have already implemented
authorization. You may share all authorization logic and create another web app
with absolutely different role but authorization would be reused, and here you
save a lot of time. Aggressive code sharing makes modular monolith very efficient
in terms of cost of feature metric

Also `systemPY` doesn't limit you how to write your code and how to implement
your units. You may set instancies of created objects as your unit attributes or
not, you may use `contextvars` or not -- all depends to you

## How to handle modular monolith?

Here we are agree we are developing modular monolith and we want to share code
between our apps. We may create `lib` directory and put here all reusable logic.
Then we have to  create `unit` folder somewhere. It may be created inside your
project's `lib` directory or in the root of your project

Then you have to to create a unit for each component. How? Please check examples.
for example, look at [SQLAlchemy](examples/unit/sqlalchemy.md). Also please
check for [ASGI Web Server](examples/self-hosted/asgi-web-app.md)

## Working examples?

Yes, we have. Some of them even executes in tests. Please check
[examples](https://github.com/kai3341/systemPY/tree/main/examples) directory
