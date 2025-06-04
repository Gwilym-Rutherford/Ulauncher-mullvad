from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import logging
import re
import urllib.parse
import subprocess

logger = logging.getLogger(__name__)


class ItemEnterEventHandler(EventListener):
    
    def get_number_spaces_infront(self, string):
        match = re.match(r"^(\s*)", string)
        spaces_infront = match.group(1)
        return len(spaces_infront)
    
    def format_countries(self, output):
        countries_cities_servers = dict()
        
        all_lines = str(output).splitlines()
        
        current_country = ""
        current_city = ""
        
        for line in all_lines:
            spaces_infront = self.get_number_spaces_infront(line)
            line = line.strip()
            
            if spaces_infront == 0:
                current_country = line
                countries_cities_servers[current_country] = {}
                
            elif spaces_infront == 1:
                current_city = line
                countries_cities_servers[current_country][current_city] = []
                
            elif spaces_infront == 2:
                countries_cities_servers[current_country][current_city].append(line)
                
        return countries_cities_servers
        
        
    def execute_command(self, command):
        response = subprocess.run(f"mullvad {command}",
                                  shell=True, capture_output=True, text=True)
        logger.debug(f"response output {response.stderr}")
        if "relay" in response.stderr:
            relay_list = subprocess.run(f"mullvad {command} list",
                                        shell=True, capture_output=True, text=True)
            logger.debug(f"relay output {relay_list.stdout}")
            self.servers = self.format_countries(relay_list.stdout)
            logger.debug(self.servers)
            logger.debug(list(dict.keys(self.servers)))
            
            items = []
            for country in list(dict.keys(self.servers)):
                items.append(
                    # ExtensionCustomAction()
                )
            
    
    def on_event(self, event, extension):
        data = event.get_data()
        if not data == {}:
            response = self.execute_command(data["command"])
            return ExtensionCustomAction(data={}, keep_app_open=False)
    