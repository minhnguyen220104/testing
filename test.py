import urllib
import socket
from loguru import logger
import requests
import os
import webbrowser

chrome_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

def strava_oauth2(client_id=None, client_secret=None):
    """Run strava authorization flow. This function will open a default system
    browser alongside starting a local webserver. The authorization procedure will be completed in the browser.

    The access token will be returned in the browser in the format ready to copy to the .env file.
    
    Parameters:
    -----------
    client_id: int, if not provided will be retrieved from the STRAVA_CLIENT_ID env viriable
    client_secret: str, if not provided will be retrieved from the STRAVA_CLIENT_SECRET env viriable
    """
    if client_id is None:
        client_id = os.getenv('STRAVA_CLIENT_ID', None)
        if client_id is None:
            raise ValueError('client_id is None')
    if client_secret is None:
        client_secret = os.getenv('STRAVA_CLIENT_SECRET', None)
        if client_secret is None:
            raise ValueError('client_secret is None')
    
    port = 8000
    _request_strava_authorize(client_id, port)

    logger.info(f"serving at port {port}")

    token = run_server_and_wait_for_token(
        port=port,
        client_id=client_id,
        client_secret=client_secret
    )

    return token


def _request_strava_authorize(client_id, port):
    params_oauth = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": f"http://localhost:{port}/authorization_successful",
        "scope": "read,profile:read_all,activity:read",
        "state": 'https://github.com/sladkovm/strava-http',
        "approval_prompt": "force"
    }
    values_url = urllib.parse.urlencode(params_oauth)
    base_url = 'https://www.strava.com/oauth/authorize'
    rv = base_url + '?' + values_url
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(rv)
    return None


def run_server_and_wait_for_token(port, client_id, client_secret):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen()
        conn, addr = s.accept()

        request_bytes = b''
        with conn:
            while True:
                chunk = conn.recv(512)
                request_bytes += chunk

                if request_bytes.endswith(b'\r\n\r\n'):
                    break
            conn.sendall(b'HTTP/1.1 200 OK\r\n\r\nsuccess\r\n')

        request = request_bytes.decode('utf-8')
        status_line = request.split('\n', 1)[0]
        
        method, raw_url, protocol_version = status_line.split(' ')
        
        url = urllib.parse.urlparse(raw_url)
        query_string = url.query
        query_params = urllib.parse.parse_qs(query_string, keep_blank_values=True)

        if url.path == "/authorization_successful":
            code = query_params.get('code')[0]
            logger.debug(f"code: {code}")
            params = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code"
            }
            r = requests.post("https://www.strava.com/oauth/token", params)
            data = r.json()
            logger.debug(f"Authorized athlete: {data.get('access_token', 'Oeps something went wrong!')}")
        else:
            data = url.path.encode()
        
        return data
    
