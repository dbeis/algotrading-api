import json

def json_content_type():
    return {'ContentType':'application/json'} 

def ok(x = {}):
    return json.dumps(x), 200, json_content_type()

def error(x = ''):
    return json.dumps({'error': x}), 400, json_content_type()

def not_found():
    return None, 404