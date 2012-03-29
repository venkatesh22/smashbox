#!/usr/bin/env python

"""Smash Box. A simple but configurable load testing script that will
request an URL on a number of threads [-t] for a time in minutes [-m]. The -u
 (--url) argument is required. By default Smash Box will run on 1 thread for
  1 minute. See help for more details."""

import logging
import urllib2
import time
import socket
import threading
from argparse import ArgumentParser

__author__ = "Steven Holmes"
__copyright__ = "Copyright 2012, Steven Holmes"
__license__ = "MIT"
__version__ = "1.0"

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s [%(levelname)s]: %(message)s')
logger = logging.getLogger("Smash Box")

# Time to pause between kicking off new threads
THREAD_START_DELAY = 30 #seconds

#Define a timeout event
timeout_event = threading.Event()

class Counter(object):
    """Counter object with a Lock to guard against simultaneous access. Used to
    increment the number of times ThreadedRequest is called """
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            self.value += 1
        finally:
            self.lock.release()

class ThreadedRequest(threading.Thread):
    """ Custom Thread class for making threaded requests to an URL """
    def __init__(self, counter, url=''):
        """ Override ThreadedRequest's __init__ method to accept counter object
        and url"""
        self.counter = counter
        self.url = url
        super(ThreadedRequest, self).__init__()

    def make_request(self):
        """ Use urllib2 to make a request to an URL, logging the status code."""
        if not self.url.startswith("http://"):
            self.url = "http://%s" % self.url
        response = urllib2.urlopen(self.url)
        status_code = response.getcode()
        if status_code != 200:
            logger.warning("Bad response.")
        else:
            logger.info("Status: %s, URL: %s " % (status_code, self.url))

    def run(self):
        """ Call make_request() until a timeout event is triggered,
        counting the number of times make_request() is called and updating a
        class variable that tracks the total number of times the
        ThreadedRequest class is instantiated."""
        times_run = 0
        thread_name = threading.current_thread().getName()
        logger.info("%s triggered..." % thread_name)
        while not timeout_event.is_set():
            try:
                logger.info("Request %s on: %s" % (times_run + 1, thread_name))
                self.make_request()
                times_run += 1
                self.counter.increment()
            except socket.timeout:
                pass
        logger.info("%s finished." % thread_name)

class LoadTest(object):
    """ Start one or more ThreadedRequest threads for load testing a given
    URL, controlling when threads are initialised and providing global stats
     on completion."""

    def trigger(self, url, number_of_threads, minutes_at_peak_qps):
        """ Trigger a load test for a given URL, number of threads and time
        at peak QPS."""
        runtime = (THREAD_START_DELAY * number_of_threads + minutes_at_peak_qps * 60)
        logger.info("Total load test time will be: %d seconds" % runtime)
        start_time = end_time = time.time()
        counter = Counter()
        threads = []
        try:
            for i in xrange(number_of_threads):
                thread = ThreadedRequest(counter, url=url)
                thread.start()
                time.sleep(THREAD_START_DELAY)
            logger.info("All threads active")
            time.sleep(minutes_at_peak_qps * 60)
            end_time = time.time()
            logger.info("Completed load test. Stopping threads.")
        except Exception, e:
            logger.error("Stopping threads. Exception raised: %s" % e)

        # Set a stop event to prevent further requests and shut down threads
        timeout_event.set()
        time.sleep(5)
        for t in threads:
            t.join()

        # Log some stats
        total_time = end_time - start_time
        total_requests = counter.value
        logger.info("Total time: %d seconds, total requests: %d" % (total_time, total_requests))
        logger.info("Req/sec: %.2f" % (total_requests / total_time))
        logger.info("All done.")

def main():
    # Handle args
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-u", "--url",
        dest="url",
        help="URL to load test.",
        metavar="URL",
        required=True
    )
    parser.add_argument(
        "-t", "--threads",
        dest="number_of_threads",
        type=int,
        help="number of threads to use during the load test. Default = 1.",
        metavar="T",
        default=1
    )
    parser.add_argument(
        "-m", "--minutes",
        dest="minutes_at_peak_qps",
        type=int,
        help="how many minutes the load test should run with all guns blazing. Default = 1.",
        metavar="M",
        default=1
    )

    args = parser.parse_args()

    # Start the load test
    load_test = LoadTest()
    load_test.trigger(args.url, args.number_of_threads, args.minutes_at_peak_qps)

if __name__ == '__main__':
    main()