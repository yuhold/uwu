import time
import logging
from datetime import datetime
import configparser

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
    
config_path = "config.ini"
config = load_config(config_path)
log_file = config.get('DEFAULT', 'log_file')
log_level = config.get('DEFAULT', 'log_level')
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info(f"Uploader started at {datetime.now()}")
    # 这里添加你的上传逻辑
    # ...
    time.sleep(5) # 模拟上传过程
    logging.info(f"Uploader finished at {datetime.now()}")
