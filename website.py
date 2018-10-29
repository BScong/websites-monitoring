from datetime import datetime, timedelta
import requests
import pandas as pd

ALERT_INTERVAL = 2*60

class Website:
    """
    Website object to store data for each website
    """
    def __init__(self, url, interval):
        self.url = url
        self.interval = interval
        self.data = pd.DataFrame(columns=['code','elapsed'])
        self.up = True # if the website is down, set to False

    def get_number_measures(self, duration, t = None):
        """
        Returns number of measures during [t-duration:t] timeframe
        """
        if not t:
            t = datetime.now()
        # get data in the timeframe t-duration to t
        current = self.data.loc[t-timedelta(seconds=duration):t]
        return len(current.index)

    def get_availability(self, duration, t = None):
        """
        Returns website availabilty during [t-duration:t] timeframe
        A website is considered available if it returns an HTTP code 200
        """
        if not t:
            t = datetime.now()
        current = self.data.loc[t-timedelta(seconds=duration):t]
        if len(current.index)==0:
            return 0
        return len(current[current.code == 200])/len(current.index)

    def get_max_response_time(self, duration, t = None):
        """
        Returns maximum response time during [t-duration:t] timeframe
        """
        if not t:
            t = datetime.now()
        current = self.data.loc[t-timedelta(seconds=duration):t]
        if len(current[current.code != -1]) == 0:
            return -1
        return current[current.code != -1]['elapsed'].max().total_seconds()

    def get_avg_response_time(self, duration, t = None):
        """
        Returns average response time during [t-duration:t] timeframe
        """
        if not t:
            t = datetime.now()
        current = self.data.loc[t-timedelta(seconds=duration):t]
        if len(current[current.code != -1]) == 0:
            return -1
        return current[current.code != -1]['elapsed'].mean().total_seconds()

    def get_response_codes(self, duration, t = None):
        """
        Returns counts of each HTTP status code received during [t-duration:t] timeframe
        """
        if not t:
            t = datetime.now()
        current = self.data.loc[t-timedelta(seconds=duration):t]
        return current.code.value_counts().to_dict()

    def check_alerts(self):
        """
        Checking alert logic
        Alert is raised if availabilty is below 80% during the last ALERT_INTERVAL seconds
        Alert is then recovered if availabilty is above 80% during the last ALERT_INTERVAL seconds
        """
        availability = self.get_availability(ALERT_INTERVAL)
        if availability<0.8 and self.up:
            self.up = False
            print("Website " + self.url + " is down. availability="+str(availability)+", time="+str(datetime.now()))
        elif availability>0.8 and not self.up:
            self.up = True
            print("Website " + self.url + " recovered. availability="+str(availability)+", time="+str(datetime.now()))

    def send_request(self):
        """
        Sends request to website and store metrics
        If there is a timeout or the website is unreachable, we store -1 as the status code
        """
        try:
            r = requests.get(self.url, timeout=5)
            d = pd.DataFrame([[r.status_code, r.elapsed]], index=[pd.Timestamp(datetime.now())], columns=['code','elapsed'])
        except:
            d = pd.DataFrame([[-1, None]], index=[pd.Timestamp(datetime.now())], columns=['code','elapsed'])
        self.data = self.data.append(d)
        # We can check for alerts here because availabilty only gets updated there
        self.check_alerts()
        return
