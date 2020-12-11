import os, time, sys
import requests
import wget
from zipfile import ZipFile
import shutil
from requests.exceptions import RequestException
from pathlib import Path

if len(sys.argv) < 2:
    print('Please specify the server IP. Foldername is optional, default is custom_charts.\nUsage: call updater_cab_client ip:port foldername')
    time.sleep(3)
    sys.exit()
else:
    ip = sys.argv[1]

if len(sys.argv) > 2:
    folderName = sys.argv[2]
else:
    folderName = "custom_charts"


update_url = f'http://{ip}/update'
result_url = f'http://{ip}/update/result'
delete_url = f'http://{ip}/update/delete'
diffs_url = f'http://{ip}/diffs/'


def main():
    if not os.getcwd().split(os.sep)[-1] == 'contents':
        os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
        if not os.getcwd().split(os.sep)[-1] == 'contents':
            print('Please run the updater from the contents folder.')
            time.sleep(3)
            sys.exit(1)

    print('Museca Customs - Personal Updater\n\n')

    if os.path.exists(f'data_mods/{folderName}-cache.json'):
        try:
            with open(f'data_mods/{folderName}-cache.json', 'rb') as f:
                response = requests.post(update_url, data=f).json()
        except JSONDecodeError as e:
            print(f"Exception")
            print("Unexpected response from the server. The cache file may be corrupt. Please delete it and try again.")
            print(response.status_code, response.reason, response.url)
            time.sleep(3)
            sys.exit(1)
        except RequestException as e:
            print(f"Exception: {e}")
            time.sleep(3)
            sys.exit(1)
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(3)
            sys.exit(1)
    else:
        response = requests.post(update_url, json={}).json()
    print(response)
    os.makedirs('data_mods', exist_ok=True)
    os.chdir('data_mods')


    if response['status'] == 'no updates':
        print('No updates.')
        time.sleep(3)
        return

    # Polling method
    def get_result(_id):
        time.sleep(4)
        result = requests.get(result_url, params={'id': _id}).json()
        return result

    if response['status'] == 'accepted':
        print('Updates available. Fetching...')
        _id = response['id']
        while True:  # loop get_result() until server returns done or failed.
            status = get_result(_id)
            if status['status'] not in ['done', 'failed']:
                print(f"Job status: {status['status']}")
                continue
            break
        if status['status'] == 'failed':
            print(f'Updated failed with server exception: {status["result"]}')
        if status['status'] == 'done':
            try:
                zipfile = status["result"][0]
                wget.download(f'{diffs_url}{zipfile}')
                print()
                requests.delete(delete_url, params={'id': _id})
                for item in status['result'][1]['removed']:
                    try:
                        print(f"Removing {item}")
                        os.remove(item)
                    except OSError as e:
                        print(e)
                folderPath = Path(folderName)
                folderlist = [x for x in folderPath.rglob("*") if x.is_dir()]
                for item in folderlist:
                    if not os.listdir(item):
                        print(f"Removing empty folder: {item}")
                        os.rmdir(item)
                with ZipFile(f"{zipfile}", 'r') as f:
                    for item in f.namelist():
                        print(f"Extracting {item}")
                        f.extract(item)
                os.remove(zipfile)
                if os.path.exists('_cache'):
                    print('Clearing the ifs cache')
                    shutil.rmtree('_cache')
                print("\n Done.")
                time.sleep(3)
                return
            except Exception as e:
                print(e)
                time.sleep(3)
                sys.exit(1)


if __name__ == "__main__":
    main()
