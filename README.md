
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

## Naive Approach
The naive approach is, to simply perform the computation in the `save` method, either of the form creating/updating
a new configuration or the model storing the computation. While this is by far the easiest solution, it has too many
drawbacks to be implemented in production:

* Too many computations in parallel block the web server, even for responding to requests not triggering computations.
* The user experience is poor, since submitting a form takes as long as the computation needs to finish.
  Hence, the user might think the server is down, while it is still computing.
* Really long computations (like one minute) will cause the server to timeout -
  while results are being generated and the user receives a timeout error
* The computation is re-triggered on a submit of the form, even if nothing has changed (however this could be solved
  easily).

## Start using celery
To overcome all but the last drawback, let's start by using
[celery](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html) as a queueing system
with [redis](https://redis.io/) as message broker. You need to perform the bold steps from the *Run* section below.

Now, if the user submits the form, a task is dispatched on the message broker, which will be picked up by one of the
workers. The user is immediately redirected to the page displaying the fractal.
However, since it is still being computed, a *default*-fractal is displayed.
Users can dispatch an arbitrary amount of computations without causing any blocks for serving the http requests.

If the computation is completed and the user refreshes the page, the new fractal is displayed.
Of course this solution is not ideal.
Users should be notified that new results are available.
And if outdated or default results are displayed, this should become clear to the user immediately.
These issues will be tackled next.

## Display ongoing computations and notify user
To the user, it should be obvious that a computation is ongoing.
And the user should be notified, if the computation is complete.

In order to be able to do that, we need to have a mechanism to know which computations are going on.
Again, let's start with the naive approach: Marking whether a computation is going on in the `Configuration` model.

If the configuration is marked to be computing, a url is injected into the `context_data` while accessing the 
`ConfigurationUpdate`-view. 
The frontend uses this url to poll the backend continuously to check whether the computation is complete. 
If the polling yields a complete computation, the page refereshes to display the new results.
While the frontend is polling, the displayed result has a spinning overlay, to inform the user about the ongoing computation.

Now imagine what happens if the user changes the configuration twice in a short period of time. 
The first time, the configuration-model is marked to be computing.
When the first task finishes, the computation is marked to be finished, even though the second computation is still going on.
Hence, the page refreshes and displays the results of the first computation as the final results.
The user is not notified, when the second results are ready.

## Save results explicitly
To avoid the necessity for the task to edit the `Configuration` model, it makes sense to create an explicit `Result` model.
If the form is saved a new `Result` is created, set to be computing and a task to actually compute the result is dispatched.
After success, the `Result` instance is set to be complete and the created fractal is saved for the instance.
If the user tries to access a configuration, always the last created result is accessed.
That way, the issue described in the previous paragraph is solved.


## Monitoring
Currently it is very hard to get insight into what is going on inside *celery* and *redis*.
A great monitoring tool is [flower](http://flower.readthedocs.io/en/latest/).
To setup and access it, follow the bold steps from the *Run* section below (again).


## Revoking tasks (current)
Using flower, we can now see what happens if the form is submitted many times in a short amount of time.
For each submit a new task is submitted.
No matter if the configuration has changed or is already outdated.
This causes the queue to be cluttered with computations that are not relevant (anymore).
To save time and server costs, let's try to revoke tasks when a new configuration is submitted.
Flower will help to investigate whether revoking the tasks actually works.


# Run
Because the issues mostly arise, when the application is run in a production environment, one shouldn't use Django's
`manage.py runserver` to evaluate how the server is blocked by the long running computation.
I recommend using `gunicorn`, for a demonstration as well as for actual production usage.
However, for demonstration I limit it to two worker because I want to be able to still use my machine.

* Create a Python 3.6 virtual environment. I recommend using [pipenv](https://github.com/pypa/pipenv)
* Activate the environment: `pipenv shell`
* **Install the dependencies: `pipenv install`**
* Run the migrations `python manage.py migrate`
* `gunicorn long_running_computations.wsgi -w 2` for 2 workers (being able to run two computations simultaneously).
*  Restart gunicorn since it doesn't support hot reloading
* Install [redis](https://redis.io/) (for Windows, there is a [fork](https://github.com/MicrosoftArchive/redis)
  available). And start a redis server, simply by typing `redis-server` to the console.
* Restart celery workers: `celery -A long_running_computations worker -l info`
  (on windows you have to append `--pool=solo`)
* **Run flower from within a virtual environment (`pipenv shell`): `flower -A long_running_computations.celery --port=5555`**
* **Navigate to `http://127.0.0.1:5555`**


# Demo
There is a demo on Heroku: https://long-running-computations.herokuapp.com/

To set it up yourself, you need to define a couple of environment variables:

* `DEBUG` (set to `False` !!!)
* `PRODUCTION` (set to `True`)
* `SECRET_KEY` (generate one [here](https://www.miniwebtool.com/django-secret-key-generator/))
* Because you can't serve media files from a local folder in Heroku (it is deleted upon dyno-restart),
  this application is configured to store media files on AWS S3. You need to set the environment variables
  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`
  * `AWS_STORAGE_BUCKET_NAME`
* Provision a redis server on Heroku: `heroku addons:create heroku-redis:hobby-dev`
* Start the worker dynos: `heroku ps:restart worker`

# Limitations
* User is not notified for finished computations when on list view
