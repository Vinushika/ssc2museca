import os, random, json, subprocess, re, time, glob
from flask import Flask, request, jsonify, abort, send_from_directory, make_response, Response
from flask_executor import Executor
from zipfile import ZipFile, ZIP_DEFLATED
import click, logging
import socket
from socket import getaddrinfo, AF_INET, gethostname
import hash
app = Flask(__name__, static_url_path='/diffs', static_folder='diffs')
app.debug = False
app.use_reloader=False
executor = Executor(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

ip_list = [ip[4][0] for ip in getaddrinfo(host=gethostname(), port=None, family=AF_INET)]
print('custom_charts local/personal update server')
print(f"\nListening on {ip_list}, port 8000")


def dict_compare(new, old):
    new_keys = set(new.keys())
    old_keys = set(old.keys())
    intersect_keys = new_keys.intersection(old_keys)
    added = new_keys - old_keys
    removed = old_keys - new_keys
    modified = set(o for o in intersect_keys if new[o] != old[o])
    same = set(o for o in intersect_keys if new[o] == old[o])
    return added, removed, modified, same

def keygen():
    chars = '1234567890abcdef'
    return ''.join(random.choice(chars) for i in range(5))


# First, client sends a post req with the cache file to this endpoint.
# This endpoint is for home releases
@app.route("/update", methods=['POST'])
def main():
    print(f"Connection from {request.remote_addr}")
    folder = 'custom_charts/'
    if not os.path.exists(folder):
        print('The custom_charts folder does not exist!')
        return abort(400)
    if not os.path.exists(app.static_folder):
        os.mkdir(app.static_folder)
    if not os.path.exists("custom-charts-cache.json"):
        print("Cache file doesn't exist. Brb caching custom_charts...")
        hash.generate_hash('custom_charts')
    data = request.get_data()
    if not data:    # if client didn't send a cache file
        print('client did not send data')
        return abort(400)

    try:    # some basic prechecks
        clientcache = json.loads(data)
        # assert 'custom_charts' in os.path.dirname(list(clientcache.keys())[0])
    except Exception as e:
        print(e)
        return abort(400)

    # Now we compare the client's cache with the servers cache, immediately return 'no updates' if there are none,
    # or submit it to a background process and return the unique process id.
    with open('custom-charts-cache.json', 'r') as f:
        servercache = json.load(f)
    added, removed, modified, same = dict_compare(servercache, clientcache)
    updates = {'updates': list(added.union(modified)), 'removed': list(removed)}
    if not (updates['updates'] or updates['removed']):
        return jsonify({'status': 'no updates'})
    _id = keygen()
    executor.submit_stored(_id, generate_diff, updates, _id, folder)
    return jsonify({'status': 'accepted', 'id': _id}), 202


# The client will poll this endpoint every few seconds with the id it received from /update.
# future.result() is the returned val from generate_diff().
@app.route("/update/result", methods=['GET'])
def get_result():
    _id = request.args['id']
    if not executor.futures.done(_id):
        return jsonify({'status': executor.futures._state(_id)})
    future = executor.futures.pop(_id)
    if not future.exception():
        return jsonify({'status': 'done', 'result': future.result()})
    else:
        print(future.exception())
        return jsonify({'status': 'failed', 'result': str(future.exception())})


# Client will call this endpoint with the id after it has successfully downloaded the zip file.
@app.route("/update/delete", methods=['DELETE'])
def delete_diff():
    _id = request.args['id']
    if f"{_id}.zip" in os.listdir(app.static_folder):
        os.remove(f"{app.static_folder}/{_id}.zip")
    return '', 200


# Write the updated files to a zip file.
# We also return the updates dict, so the client knows which files to remove.
def generate_diff(updates, _id, folder):
    print('generating diff')
    os.makedirs('diffs', exist_ok=True)
    with ZipFile(f"diffs/{_id}.zip", mode='w', compression=ZIP_DEFLATED, compresslevel=6) as f:
        for item in updates['updates']:
            f.write(f'{item}', arcname=item)
        f.write(f'custom-charts-cache.json', arcname='custom-charts-cache.json')
    return f"{_id}.zip", updates


# This method allows us to use the hit counter for static downloads served by nginx at /download, which is mapped to the builds dir.
@app.route("/downloads/<file>", methods=['GET'])
def download(file):
    return send_from_directory(app.config('static_folder'), file, as_attachment=True)


def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
    except:
        print("Unable to get Hostname and IP")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
