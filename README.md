Smash Box
========

## Introduction

Smash Box is a Python command line script for load testing web applications. It uses threads to run multiple requests concurrently in the same process space.

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

### License

Licensed under [MIT license](http://www.opensource.org/licenses/mit-license.php). Do what you like but please don't remove credits.