# Website availabilty & perfomance monitoring

## Problem
### Overview
-   ✓ Create a console program to monitor performance and availability of websites
-   ✓ Websites and check intervals are user defined
-   ✓ Users can keep the console app running and monitor the websites


### Stats
-   ✓ Check the different websites with their corresponding check intervals
-   ✓ Compute a few interesting metrics: availability, max/avg response times, response codes count and more...
-   ✓ Over different timeframes: 2 minutes and 10 minutes
-   ✓ Every 10s, display the stats for the past 10 minutes for each website
-   ✓ Every minute, displays the stats for the past hour for each website


### Alerting
-   ✓ When a website availability is below 80% for the past 2 minutes, add a message saying that "Website {website} is down. availability={availability}, time={time}"
-   ✓ When availability resumes for the past 2 minutes, add another message detailing when the alert recovered
-   ✓ Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons


### Tests & question
-   ✓ Write a test for the alerting logic
-   ✓ Explain how you'd improve on this application design

## Running
To run the program: `python3 monitoring.py websites.txt`. Websites.txt file syntax is described below.
If dependencies are missing, you can install them with `pip3 install -r requirements.txt` (Librairies used: pandas, tabulate, requests).

## Architecture
Each website is mapped to a Website object storing its url, its check interval time and all the data collected about the website (using [Pandas DataFrame](http://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.html)).

The user can set its own list of websites and interval (in seconds) by writing them into a text file, following the `website_url interval` syntax.

Example:

```
https://www.google.com/ 5
https://www.zhong.fr/ 30
https://datadoghq.com/ 15
```

We use an event scheduler ([sched](https://docs.python.org/3/library/sched.html)) to plan all events (stats printing and requests).

We use the [Tabulate library](https://pypi.org/project/tabulate/) for pretty printing and the [Requests library](http://docs.python-requests.org/en/master/#) for HTTP calls.

## Statistics
This program monitors the availability and response times of the websites provided. A website is defined available if it returns an HTTP code 200. It prints the average and maximum response times for the given timeframe. We also keep track and count of the status codes returned.

## Alerts
We check if we have to raise an alert for a specific website after each request to this website. We compute the new availability for the past 2 minutes and compare the value to the threshold (80%). We can then raise an error if the availability is below that threshold. We also keep a flag to know if the website is currently up or down, so that we can print a message when the alert recovers and the availability resumes.

## Testing
To test the Alerts system, we can run a [HTTP server](https://docs.python.org/3/library/http.server.html) on localhost then shut it down during two minutes.
We should have the alert message showing up in the terminal. We can then start it again and the recovery message should show up.
This test is implemented in `test_alert.py`.
To run: run `python3 test_alert.py` and then `python3 monitoring.py websites.txt` in another window. Both processes must be running at the same time.

## Improvements
Some improvements can be made to the current program:

-   Viewing values on a graph is better than having just the average and the maximum values in a table, it would allow us to see the evolution of availability and response time over time
-   Switch from a Pandas DataFrame to a Time Series database (such as [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/)). This would allow us to store data between runs.
-   Display an "history" for the websites with last peaks in response times (timestamp and response time)
-   Avoid printing each table after the other. Having one table and updating it is prettier
-   Separate the alert system into its own class and add the ability to create any type of alerts (availability, response_time, duration)
-   Automatize alert testing
-   Add tests

### Minor improvements
-   Instead of counts of status codes, print percentage of each status_code encountered
-   Set warning if number of measures is small compared to the time interval (the data may be irrelevant)
-   Personalize printing interval by passing them as parameters to the program
-   Print warnings in different colors
