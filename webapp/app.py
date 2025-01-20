import time
from flask import Flask, render_template, jsonify, request
import configparser
import requests
import threading
import logging
import os

app = Flask(__name__)

# Load configuration
def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

def save_config(config, config_path):
     with open(config_path, 'w', encoding='utf-8') as configfile:
         config.write(configfile)

config_path = "../config.ini"
config = load_config(config_path)

# Configure logging
log_file = config.get('DEFAULT', 'log_file', fallback='runyun_probe.log')
log_level = config.get('DEFAULT', 'log_level', fallback='INFO').upper()
logging.basicConfig(filename=log_file, level=getattr(logging, log_level), format='%(asctime)s - %(levelname)s - %(message)s')

websites = []
for section in config.sections():
    if section.startswith('WEBSITE_'):
        website_number = section.split('_')[1]
        url = config[section]['url']
        probe_interval = int(config[section]['probe_interval'])
        websites.append({
            'id': website_number,
            'url': url,
            'probe_interval': probe_interval,
            'status': 'pending',
            'response_time': None,
            'last_check': None,
            'error': None
        })

def probe_website(website):
    try:
        start_time = time.time()
        response = requests.get(website['url'], timeout=10)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        website['response_time'] = round(response_time, 2)
        website['status'] = 'online' if response.status_code == 200 else 'offline'
        website['error'] = None
        if response.status_code != 200:
             website['error'] = f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        website['status'] = 'offline'
        website['response_time'] = None
        website['error'] = str(e)
    finally:
        website['last_check'] = time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Probed {website['url']}, status: {website['status']}, response_time: {website['response_time']}, error: {website['error']}")


def probe_all_websites():
    while True:
        for website in websites:
            probe_website(website)
        time.sleep(1) # Adjust the sleep time if needed

# Start probing in a separate thread
probe_thread = threading.Thread(target=probe_all_websites, daemon=True)
probe_thread.start()

@app.route('/api/websites')
def get_websites():
     status_filter = request.args.get('status')
     sort_by = request.args.get('sort_by')
     search_term = request.args.get('search')

     filtered_websites = websites

     if status_filter:
         filtered_websites = [site for site in filtered_websites if site['status'] == status_filter]

     if search_term:
         filtered_websites = [site for site in filtered_websites if search_term.lower() in site['url'].lower()]
        

     if sort_by:
         if sort_by == 'url':
             filtered_websites.sort(key=lambda site: site['url'])
         elif sort_by == 'status':
              filtered_websites.sort(key=lambda site: site['status'])
         elif sort_by == 'response_time':
              filtered_websites.sort(key=lambda site: site['response_time'] if site['response_time'] is not None else float('inf'))
         elif sort_by == 'last_check':
             filtered_websites.sort(key=lambda site: site['last_check'], reverse=True)
     return jsonify(filtered_websites)
 
@app.route('/api/websites', methods=['POST'])
def manage_websites():
    global websites
    action = request.json.get('action')
    if action == 'add':
        url = request.json.get('url')
        probe_interval = request.json.get('probe_interval')
        if not url or not probe_interval:
             return jsonify({'message':'URL and probe interval are required'}), 400
        new_website_number = len(config.sections())
        new_section_name = f"WEBSITE_{new_website_number+1}"
        config[new_section_name] = {
            'url': url,
            'probe_interval': str(probe_interval)
        }
        save_config(config, config_path)
        websites.append({
             'id': str(new_website_number+1),
            'url': url,
            'probe_interval': probe_interval,
            'status': 'pending',
            'response_time': None,
            'last_check': None,
            'error': None
        })
        return jsonify({'message': 'Website added successfully'}), 201
    elif action == 'remove':
        website_id = request.json.get('website_id')
        if not website_id:
             return jsonify({'message':'Website ID is required'}), 400
        section_to_remove = f'WEBSITE_{website_id}'
        if section_to_remove in config.sections():
             config.remove_section(section_to_remove)
             save_config(config, config_path)
             websites = [site for site in websites if site['id'] != website_id]
             return jsonify({'message': 'Website removed successfully'}), 200
        else:
            return jsonify({'message': 'Website not found'}), 404
    elif action == 'modify':
         website_id = request.json.get('website_id')
         property_to_modify = request.json.get('property')
         new_value = request.json.get('value')
         if not website_id or not property_to_modify or not new_value:
             return jsonify({'message':'Website ID, property and value are required'}), 400
         section_to_modify = f'WEBSITE_{website_id}'
         if section_to_modify in config.sections():
             config[section_to_modify][property_to_modify] = new_value
             save_config(config, config_path)
             for website in websites:
                 if website['id'] == website_id:
                     website[property_to_modify] = new_value
                     break
             return jsonify({'message': 'Website modified successfully'}), 200
         else:
             return jsonify({'message': 'Website not found'}), 404
    else:
        return jsonify({'message': 'Invalid action'}), 400


@app.route('/')
def index():
    return render_template('index.html')

def create_app():
     return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)
