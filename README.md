
# Motivation

With the rise of "data science", more and more web application developers want to enable their users to configure
computation tasks via an user interface and perform them on the server.
Once the computation is finished, they want to notify the user.
This requirement creates a couple of non-trivial issues to solve:

* How do I handle the computation tasks in way, my webserver still keeps handling usual requests performantly?
* What are ways to avoid displaying outdated data, but still don't retrigger the calculation at every configuration
  change?
* How can the user be notified, once a task is finished?
* What about monitoring and testing?


# Application
This repository contains a Django application to demonstrate several concepts around handling long running computations.

## Data Structure
It has one major model `Configuration`.
This can be considered to be a proxy for a more complex configuration setup.
For example, think about the configuration for training of a neural network.
It's likely you have models defining the individual layers of the model as well as their connections.
Other models describe the parameters used for training of the model.
And least, you need to connect it to a dataset which might be defined in the database, too.

## Computation Proxy
In order not to bloat this demo application too much, no "real computation" is performed.
But because I didn't want to use a `time.sleep()` call as a simulation for the computation, I'm generating fractals
of the [Julia set](https://en.wikipedia.org/wiki/Julia_set)
(please don't ask me anything about the underlying mathematics, I have no idea what it actually means).
The code to generate the fractals is copied and pasted from
[Danilo Bellini](https://github.com/danilobellini/fractal).


# Versions

## Naive Approach (current)
The naive approach is, to simply perform the computation in the `save` method, either of the form creating/updating
a new configuration or the model storing the computation. While this is by far the easiest solution, it has too many
drawbacks to be implemented in production:

* Too many computations in parallel block the web server, even for responding to requests not triggering computations.
* The user experience is poor, since submitting a form takes as long as the computation needs to finish.
  Hence, the user might think the server is down, while it is still computing.
* The computation is re-triggered on a submit of the form, even if nothing has changed (however this could be solved
  easily).
* Really long computations (like one minute) will cause the server to timeout -
  no results are being generated and the user simply receives an error


# Run
Because the issues mostly arise, when the application is run in a production environment, one shouldn't use Django's
`manage.py runserver` to evaluate how the server is blocked by the long running computation.
I recommend using `gunicorn`, for a demonstration as well as for actual production usage.
However, for demonstration I limit it to two worker because I want to be able to still use my machine.

* Create a Python 3.6 virtual environment. I recommend using [pipenv](https://github.com/pypa/pipenv)
* Activate the environment: `pipenv shell`
* Install the dependencies: `pipenv install
* Run the migrations `python manage.py migrate`
* `gunicorn long_running_computations.wsgi -w 2` for 2 workers (being able to run two computations simultaneously)

# Demo
There is a demo on Heroku: https://long-running-computations.herokuapp.com/

To set it up yourself, you need to define a couple of environment variables:

* `DEBUG` (set to `False` !!!)
* `PRODUCTION` (set to `True`)
* `SECRET_KEY` (generate one [here](https://www.miniwebtool.com/django-secret-key-generator/))
* Because you can't serve media files from a local folder in Heroku (it is deleted upon dyno-restart),
  this application is configured to store media files on AWS S3. You need to set the environment variables
  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY
  * `AWS_STORAGE_BUCKET_NAME`