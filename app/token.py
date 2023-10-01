import json

file_name = 'config.json'

def get_token():
    with open(file_name) as config_file:
        config = json.load(config_file)
    try:
        return config["token"]
    except json.decoder.JSONDecodeError:
        return None
    except KeyError:
        return None

def store_token(token):
    data = {
        "token": token,
    }
    with open(file_name, 'w') as file:
        json.dump(data, file)

def get_state():
    with open(file_name) as config_file:
        config = json.load(config_file)
    return config['state']

def store_state(state):
    data = {
        "state": state,
    }
    with open(file_name, 'w') as file:
        json.dump(data, file)
