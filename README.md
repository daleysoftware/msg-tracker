# Slack Time Tracker

*Work in progress.*

## Overview

A service that queries slack to summarize end-user active hours.

## Usage

Start by setting up your python virtual environment with `./setup.sh`. After
all your deps are installed, run the collector as a service and the reporter
periodically, as desired.

### Collector

The collector is responsible for querying Slack for activity data and placing
it into our backing store, Redis.

The environment variable `SLACK_TOKEN` must be present for the collector to
operate.

To run the collector:

```
./tools/collector.sh
```

### Reporter

The reporter prints formatted activity data in the form of daily summaries
on a per user basis (i.e. it tells you how long a user was logged in on a
given day).

To run the reporter:

```
./tools/reporter:
```

## Notes

This tool operates on local time (not UTC).
