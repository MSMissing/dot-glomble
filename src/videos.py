import http.client as client
import utils

def get_id_from_url(url: str) -> str:
    return url.replace('https://glomble.com/videos/', '')

# Gets the url where the video at _id is stored
def get_redirected_url(_id: str) -> str:
    glom = client.HTTPSConnection('glomble.com')

    # get redirect stuff
    print(f'Requesting file at https://glomble.com/videos/{_id}/download...')
    glom.request('GET', f'/videos/{_id}/download')
    redirect_response = glom.getresponse()
    print(redirect_response.status, redirect_response.reason)

    # close the connection.
    glom.close()

    if redirect_response.status != 302:
        raise ConnectionError(f'Expected response status 302 Found, but got {redirect_response.status} {redirect_response.reason}')
    return redirect_response.getheader('Location')


def load_raw_video(_id: str) -> (bytes, str):
    # get the redirect URL
    loc = get_redirected_url(_id)

    # request the file
    print(f'redirecting to {loc}...')
    media_conn = client.HTTPSConnection('media.glomble.com')
    media_conn.request('GET', loc)

    # get response and return the thing
    media_response = media_conn.getresponse()
    print(media_response.status, media_response.reason)
    return (media_response.read(), media_response.getheader('Content-Type'))

def get_file_ext(text):
    match text:
        case 'video/mp4':
            return '.mp4'
        case 'video/quicktime':
            return '.mov'
        case _:
            raise NotImplemented() # Glomble only supports mp4 and mov file formats rn.

def create_file(filename, content):
    if not filename.endswith('.glomble'):
        filename += '.glomble'
    print(f'Creating file {filename}...')
    with open(filename, 'x') as f:
        f.write(content)
    print(f'Successfully created file {filename}.')





