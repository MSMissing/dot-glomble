import sys
import os
import http.client as client
import urllib.request

def verbose(*args):
    print(*args)

def version():
    print('dot-glomble v1.1')

def usage():
    print('Commands:')
    print('  create [FILE] [VALUE]')
    print('    Creates a new .glomble file')
    print('  detail [FILE]')
    print('    Opens a detailed view of the video with your default browser.')
    print('  play [FILE]')
    print('    Plays the file using VLC.')
    print('  --help or -h')
    print('    See this useful thingy')
    print('  --version')
    print('    See the version of this app.')

def get_video_file(_id: str) -> bytes:
    glom = client.HTTPSConnection('glomble.com')
    print(f'requesting file at https://glomble.com/videos/{_id}/download...')
    glom.request('GET', f'/videos/{_id}/download')
    redirect_response = glom.getresponse()
    glom.close()
    print(redirect_response.status, redirect_response.reason)
    if redirect_response.status == 302:
        print()
        loc = redirect_response.getheader('Location')
        print(f'redirecting to {loc}...')

        media_conn = client.HTTPSConnection('media.glomble.com')
        media_conn.request('GET', loc)
        media_response = media_conn.getresponse()
        print()
        print(media_response.status, media_response.reason)
        return (media_response.read(), media_response.getheader('Content-Type'))
    else:
        raise ConnectionError(f'Expected response status of 302 Found, but got {redirect_response.status} {redirect_response.reason}')

def get_file_ext(text):
    match text:
        case 'video/mp4':
            return '.mp4'
        case 'video/quicktime':
            return '.mov'
        case _:
            raise NotImplemented()

def main():
    if len(sys.argv) < 2:
        usage()
        return

    match sys.argv[1]:
        case 'create':
            if len(sys.argv) < 4:
                raise SyntaxError('create command requires two arguments')
            if not sys.argv[2].endswith('.glomble'):
                raise NameError('Filename must end with ".glomble"')

            with open(sys.argv[2], 'x') as f:
                f.write(sys.argv[3])
            print(f'Successfully created {sys.argv[2]}')
        case 'detail':
            with open(sys.argv[2], 'r') as f:
                os.system(f'xdg-open https://glomble.com/videos/{f.read()}')
        case 'play':
            with open(sys.argv[2], 'r') as f:
                os.system(f'cvlc https://glomble.com/videos/{f.read()}/download')
        case '--help' | '-h':
            version()
            print()
            usage()
        case 'version' | '--version':
            version()
        case 'download':
            if len(sys.argv) != 3:
                raise SyntaxError('Too many arguments.')
            with open(sys.argv[2], 'r') as f:
                video_id = f.read()
                (media, media_type) = get_video_file(video_id)
            with open('.'.join(sys.argv[2].split('.')[0:-1]) + get_file_ext(media_type), 'wb') as f:
                print(f'writing to file {f.name}')
                f.write(media)

        case _:
            raise SyntaxError('Invalid syntax.')


if __name__ == "__main__":
    try:
        main()
    except SyntaxError as err:
        print(err)
        usage()
    except Exception as err:
        print(err)
