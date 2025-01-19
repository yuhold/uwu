import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from utils import load_config, send_email
import time
from datetime import datetime
import subprocess
import sys
import json
import os

def check_website(url):
    logging.info(f"Checking website: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Website {url} is online. Status code: {response.status_code}")
        update_status(url, "online", response.status_code)
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Website {url} is offline. Error: {e}")
        update_status(url, "offline", str(e) )
        return False

def trigger_uploader(config):
    logging.info("Triggering uploader...")
    try:
        # 获取当前 Python 解释器的路径
        python_executable = sys.executable
        # 获取 uploader.py 的绝对路径
        uploader_path = os.path.join(os.path.dirname(__file__), config['UPLOADER']['uploader_path'])
        subprocess.run([python_executable, uploader_path], check=True, capture_output=True)
        logging.info(f"Uploader triggered at {datetime.now()}")
        update_status("uploader", "success")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to trigger uploader: {e.stderr.decode()}")
        update_status("uploader", "failed", str(e.stderr.decode()))


def probe_task(config, failure_counts = {}):
    logging.info("Probe task started.")
    for section in config.sections():
        if section.startswith('WEBSITE_'):
            url = config[section]['url']
            if url not in failure_counts:
                failure_counts[url] = 0
            if check_website(url):
                failure_counts[url] = 0
            else:
                failure_counts[url] += 1
                if failure_counts[url] >= 3:
                    send_email(config, f"Runyun website {url} is down for 3 consecutive checks. Current time: {datetime.now()}")
                    failure_counts[url] = 0

    logging.info("Probe task finished.")

def update_status(target, status, details=None):
    status_file = "./status.json"
    logging.info(f"Updating status: target={target}, status={status}, details={details}")
    try:
        with open(status_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[target] = {
        "status": status,
        "time": str(datetime.now()),
        "details": details
    }
    logging.info(f"Writing to status.json: {data}")
    with open(status_file, "w") as f:
            json.dump(data, f, indent=4)

def main():
    config_path = "config.ini"
    config = load_config(config_path)
    
    log_file = config.get('DEFAULT', 'log_file')
    log_level = config.get('DEFAULT', 'log_level')
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    scheduler = BackgroundScheduler()
    for section in config.sections():
      if section.startswith('WEBSITE_'):
          probe_interval = config.getint(section, 'probe_interval')
          scheduler.add_job(probe_task, 'interval', seconds=probe_interval, args=[config], next_run_time=datetime.now())
    scheduler.add_job(trigger_uploader, 'interval', seconds=config.getint('UPLOADER', 'uploader_interval'), args=[config], next_run_time=datetime.now())
    
    scheduler.start()
    logging.info("Probe started.")
    update_status("probe", "running")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Probe stopped.")
        update_status("probe", "stopped")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
