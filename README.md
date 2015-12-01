# Msg Tracker

*Work in progress.*

## Overview

Msg Tracker is a service that queries various messaging services to summarize end-user active
hours.

Currently supported services:

* Slack

## Usage

Start by setting up your python virtual environment with `./setup.sh`. After all your deps are
installed, run the collector as a service and the reporter periodically, as desired.

### Collector

The collector is responsible for querying Slack for activity data and placing it into our backing
store, redis.

The environment variable `SLACK_TOKEN` must be present for the collector to operate.

To run the collector:

```
./tools/collect.sh
```

### Reporter

The reporter prints formatted activity data in the form of time summaries on a per user basis
(i.e. it tells you how long a user was logged in during a given time period).

To run the reporter:

```
./tools/report.sh <interval_days> <max_results>
```

Where `interval_days` is the query interval, with units in days, and `max_results` is the maximum
number of results to pull for a given user. For example, if given `interval_days=1` and
`max_results=7`, the active times for the past week would be displayed.

## Design Notes

* This tool operates on local time (not UTC).
* Cleanup of data is currently not supported, but could easily be added later using the redis
  `expiry` feature. Ad-hoc cleanup and be accomplished using the `./tools/cleanup.sh` script.
