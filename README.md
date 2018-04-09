
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