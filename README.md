# Msg Tracker

*Work in progress.*

## Overview

Msg Tracker is a service that queries various messaging services to summarize end-user active
hours.

Currently supported services:

* Slack

Other messaging platforms coming *Soon^TM*.

## Usage

Start by setting up your python virtual environment with `./setup.sh`. After all the dependencies
are installed, run the collector as a service and the reporter periodically, as desired.

### Collector

The collector is responsible for querying messaging endpoint for activity data and placing it into
our backing store, redis. To run the collector, use `./tools/collect.sh`.

### Reporter

The reporter prints formatted activity data in the form of time summaries on a per user basis
(i.e. it tells you how long a user was logged in during a given time period). To run the reporter
use `./tools/report.sh`.

## Unit Tests

To run unit tests use `./tools/test.sh`.
