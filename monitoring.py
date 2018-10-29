# A performance monitoring tool for websites

import argparse
import time, sched
from tabulate import tabulate
from website import Website
from datetime import datetime

def parse_arguments():
    """
    Parses terminal arguments
    """
    parser = argparse.ArgumentParser(description='A performance monitoring tool for websites',
                                         epilog='Written by Benoit Zhong')

    parser.add_argument('websites', help='Websites to monitor and their corresponding check intervals in seconds')
    args = parser.parse_args()
    return args

def read_file(filename):
    """
    Reads a file and returns a list of Website objects
    """
    lines = []
    with open(filename) as file:
        for line in file:
            url, interval = line.split(' ')
            interval = int(interval)
            website = Website(url,interval)
            lines.append(website)
    return lines

def send_request_and_reschedule(website, scheduler):
    """
    Sends request to a Website and schedule the next request
    """
    website.send_request()
    scheduler.enter(website.interval, 1, send_request_and_reschedule, argument=(website,scheduler))
    return

def print_stats(websites, duration, interval, scheduler):
    """
    Print statistics and schedule the next printing
    """

    data = []

    status = {}
    codes = set() # data structure to keep track of all status codes

    t = datetime.now()
    for website in websites:
        data.append((website.url + ' (' + str(website.get_number_measures(duration, t)) + ')', website.get_availability(duration, t)*100, website.get_avg_response_time(duration, t), website.get_max_response_time(duration, t)))

        status[website.url] = website.get_response_codes(duration, t)
        status[website.url]['Total'] = 0
        for code in status[website.url]:
            if code != 'Total':
                status[website.url]['Total'] += status[website.url][code]
                codes.add(code)

    # Print statistics
    print("Statistics for last " + str(duration) + " seconds.")
    print(tabulate(data, headers=['Website (number of measures)', 'Availabilty (%)', "Avg response time (sec)", "Max response time (sec)"], tablefmt='orgtbl'))
    print()

    # Print status codes
    print(tabulate([[website.url, *[status[website.url][key] if key in status[website.url] else 0 for key in [*codes,"Total"]]] for website in websites], headers=['Website',*list(codes), "Total"],tablefmt='orgtbl'))
    print()

    scheduler.enter(interval, 1, print_stats,argument=(websites, duration, interval, scheduler))
    return

PRINT_10_MINUTES_INTERVAL = 10
PRINT_1_HOUR_INTERVAL = 60
def main():
    args = parse_arguments()
    websites_list = read_file(args.websites)
    scheduler = sched.scheduler(time.time, time.sleep)

    print("Starting monitoring...")

    for website in websites_list:
        scheduler.enter(website.interval, 1, send_request_and_reschedule, argument=(website,scheduler))

    scheduler.enter(PRINT_10_MINUTES_INTERVAL, 1, print_stats,argument=(websites_list, 10*60, PRINT_10_MINUTES_INTERVAL, scheduler))
    scheduler.enter(PRINT_1_HOUR_INTERVAL, 1, print_stats,argument=(websites_list, 60*60, PRINT_1_HOUR_INTERVAL, scheduler))

    scheduler.run()

main()
