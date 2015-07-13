import logging
import network

DEFAULT_POINTS = 10

__ssid_of_accesspoint = network.get_ssid_of_accesspoint()
__mac_of_accesspoint = network.get_mac_of_accesspoint()
__connected_interfaces = network.get_connected_interfaces_and_ip()

def __check_ssid(location):
    if 'ssid' in location:
        if __ssid_of_accesspoint in location['ssid']:
            location['__score'] += DEFAULT_POINTS
            logging.debug('+SSID ==> {}'.format(location['__score']))
        else:
            location['__score'] = -1000
            logging.debug('-SSID ==> {}'.format(location['__score']))

def __check_mac(location):
    if 'mac' in location:
        if __mac_of_accesspoint in location['mac']:
            location['__score'] += DEFAULT_POINTS
            logging.debug('+MAC ==> {}'.format(location['__score']))
        else:
            location['__score'] = -1000
            logging.debug('-MAC ==> {}'.format(location['__score']))

def __check_ip(location):
    if 'ip' in location:
        if __connected_interfaces[location['interface']] in location['ip']:
            location['__score'] += DEFAULT_POINTS
            logging.debug('+IP ==> {}'.format(location['__score']))
        else:
            location['__score'] = -1000
            logging.debug('-IP ==> {}'.format(location['__score']))


def get_matching_config(config):
    best_config = config.dynstatus['default']
    best_config['__score'] = 0

    for location in config.dynstatus['locations']:
        logging.debug('='*45)
        logging.debug('Checking: {}'.format(location['name']))
        if location['interface'] in __connected_interfaces:
            location['__score'] = 0
            __check_ssid(location)
            __check_mac(location)
            __check_ip(location)

            if location['__score'] > best_config['__score']:
                best_config = location
        else:
            logging.debug('Interface not connected.')
    logging.debug('='*45)
    logging.info('Best location: {}'.format(best_config['name']))
    return best_config
