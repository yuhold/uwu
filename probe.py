import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from utils import load_config, send_email
import time
from datetime import datetime
import subprocess

def check_website(config):
    url = config.get('WEBSITE', 'url')
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Website {url} is online. Status code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Website {url} is offline. Error: {e}")
        return False

def trigger_uploader(config):
    try:
        subprocess.run(['/usr/bin/python3', '/path/to/your/script/uploader.py'], check=True, capture_output=True)
        logging.info(f"Uploader triggered at {datetime.now()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to trigger uploader: {e.stderr.decode()}")

def probe_task(config, failure_count = [0] ):
    if check_website(config):
        failure_count[0] = 0
    else:
        failure_count[0] += 1
        if failure_count[0] >= 3:
            send_email(config, f"Runyun website {config.get('WEBSITE', 'url')} is down for 3 consecutive checks. Current time: {datetime.now()}")
            failure_count[0] = 0
    
def main():
    config_path = "config.ini"
    config = load_config(config_path)
    
    log_file = config.get('DEFAULT', 'log_file')
    log_level = config.get('DEFAULT', 'log_level')
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    scheduler = BackgroundScheduler()
    scheduler.add_job(probe_task, 'interval', seconds=config.getint('WEBSITE', 'probe_interval'), args=[config])
    scheduler.add_job(trigger_uploader, 'interval', seconds=config.getint('UPLOADER', 'uploader_interval'), args=[config])
    
    scheduler.start()
    logging.info("Probe started.")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Probe stopped.")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
