# Getting Started

First of all we have to admit due our app has multiple entrypoints, our app is
a [modular monolith app](https://www.geeksforgeeks.org/system-design/what-is-a-modular-monolith/).
When we are developing modular monolith app, we have huge bunch of reusable
code. This reusable code makes next entrypoint implementation much easier. For
example you have your first web application and you have already implemented
authorization. You may share all authorization logic and create another web app
with absolutelly different role but authorization would be reused, and here you
save a lot of time. Agressive code sharing makes modular monolith very effitient
by cost of feature metric.

## How to handle modular monolith?

Here we are agree we are developing modular monolith and we want to share code
between our apps. We may create `lib` directory and put here all reusable logic.
Then we have to  create `unit` folder somewhere. It may be created insile your
project's `lib` directory or in the root of your project

Then you have to to create a unit for each component. How? Please check examples.
for example, look at [SQLAlchemy](examples/unit/sqlalchemy.md). Also please
check for [ASGI Web Server](examples/self-hosted/asgi-web-app.md)
