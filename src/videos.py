import http.client as client

def get_id(url):
    return url.replace('https://glomble.com/videos/', '')

# Gets the url where the video at _id is stored
def get_video_url(_id: str) -> str:
    glom = client.HTTPSConnection('glomble.com')
    print(f'requesting file at https://glomble.com/videos/{_id}/download...')
    glom.request('GET', f'/videos/{_id}/download')
    redirect_response = glom.getresponse()
    glom.close()
    print(redirect_response.status, redirect_response.reason)
    if redirect_response.status != 302:
        raise ConnectionError(f'Expected 302 Found, but got {redirect_response.status} {redirect_response.reason}')
    return redirect_response.getheader('Location')


def get_video_file(_id: str) -> (bytes, str):
    loc = get_video_url(_id)
    print()
    print(f'redirecting to {loc}...')
    media_conn = client.HTTPSConnection('media.glomble.com')
    media_conn.request('GET', loc)
    media_response = media_conn.getresponse()
    print()
    print(media_response.status, media_response.reason)
    return (media_response.read(), media_response.getheader('Content-Type'))

def get_file_ext(text):
    match text:
        case 'video/mp4':
            return '.mp4'
        case 'video/quicktime':
            return '.mov'
        case _:
            raise NotImplemented()

def create_file(filename, video_id):
    if not filename.endswith('.glomble'):
        raise NameError('Filename must end with ".glomble"')

    with open(filename, 'x') as f:
        f.write(video_id)
    print(f'Successfully created file {filename}.')
