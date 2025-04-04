import pandas as pd
import time
from datetime import datetime

class Monitoring:
    def __init__(self):
        self.log_file = 'monitoring/service_log.csv'
        
    def log_service(self, status, response_time):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp},{status},{response_time}\n")
    
    def check_service_health(self):
        try:
            logs = pd.read_csv(self.log_file)
            last_hour = logs[logs['timestamp'] > (datetime.now() - pd.Timedelta(hours=1)).isoformat()]
            availability = len(last_hour[last_hour['status'] == '200']) / len(last_hour)
            return availability > 0.95
        except:
            return False