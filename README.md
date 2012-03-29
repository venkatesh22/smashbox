Smash Box
========

## Introduction

Smash Box is a simple Python command line script for load testing web applications.

Smash Box uses threads to run multiple requests concurrently in the same process space, allowing you to hit an URL several hundred / thousand times in a relatively small space of time. Both threads and load test time are configurable and can be upped to increase the load on your server or application. Threads will take time to ramp up so the -m argument (see help) is the time the load test will run *after* all threads -t are active. The actual runtime will therefore be larger than the -m value specified.

### Basic usage

For example:

    python smashbox.py -u www.test.com

    -u [URL], --url [URL] = URL to load test. This is required.
    -h, --help = Show help.

The above example will fire requests at www.test.com on one thread for one minute (defaults).

### Options

If you want to increase the load on your web application, use the following options:

    -t [T], --threads [T] = Number of threads to use during the load test (integer).
    -m [M], --minutes [M] = How many minutes the test should run with all threads active (integer).

For example:

    python smashbox.py -u www.test.com -t 10 -m 5

The above example will fire requests at www.test.com on 10 threads for 5 minutes.

### What's it for?

There are many scripts, applications, libraries and services for load testing. I wrote this for two reasons: i) to quickly and simply load test App Engine applications and ii) have a tinker with Python's threads and locks.

### License

Licensed under [MIT license](http://www.opensource.org/licenses/mit-license.php). Do what you like but please don't remove credits.