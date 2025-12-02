import json
def read_settings_file(id):
    path = "src/settings.json"
    with open(path, 'r') as file:
        data = json.load(file)
        channel_id = data['settings']['main'][id]
        return channel_id
        