import sys
import os
import http.client as client
import urllib.request
import playlist
import search

def verbose(*args):
    print(*args)

def version():
    print('dot-glomble v1.1')

def usage():
    print('Commands:')
    print('  create <FILE> <VIDEO-ID>')
    print('    Creates a new .glomble file')
    print('  detail <FILE>')
    print('    Opens a detailed view of the video with your default browser.')
    print('  play <FILE>')
    print('    Plays the file using VLC.')
    print('  from-name <QUERY> <FILENAME>')
    print('    Finds the video with the closest match to QUERY, and creates a .glomble file from it.')
    print('  search <QUERY> <FILENAME>')
    print('    Searches for the query, and creates a playlist of results')
    print('  playlist <PLAYLIST-CMD>')
    print('    Playlist stuff')
    print('  --help or -h')
    print('    See this useful thingy')
    print('  --version')
    print('    See the version of this app.')

def get_id(url):
    return url.replace('https://glomble.com/videos/', '')

def get_video_url(_id: str) -> str:
    glom = client.HTTPSConnection('glomble.com')
    print(f'requesting file at https://glomble.com/videos/{_id}/download...')
    glom.request('GET', f'/videos/{_id}/download')
    redirect_response = glom.getresponse()
    glom.close()
    print(redirect_response.status, redirect_response.reason)
    return redirect_response

def get_video_file(_id: str) -> bytes:
    redirect_response = get_video_url(_id)
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

def create_file(filename, video_id):
    if not filename.endswith('.glomble'):
        raise NameError('Filename must end with ".glomble"')

    with open(filename, 'x') as f:
        f.write(video_id)
    print(f'Successfully created file {filename}.')

def main():
    if len(sys.argv) < 2:
        usage()
        return

    args = sys.argv[2:]
    match sys.argv[1]:
        case 'create':
            create_file(args[0], args[1])

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

        case 'playlist':
            try:
                playlist.playlist_command()
            except SyntaxError as err:
                playlist.usage()
                raise err

        case 'from-name':
            print(f'Searching glomble for {args[0]}')
            url = search.search(args[0])[0]
            print(f'Found video {get_id(url)}.')
            create_file(args[1], get_id(url))

        case 'search':
            if len(args) < 2:
                raise SyntaxError('Not enough arguments')
            print(f'Searching glomble for {args[0]}')
            urls = search.search(args[0])
            print('found videos:')

            pl = playlist.Playlist()
            for url in urls:
                print(f' {get_id(url)}')
                pl.videos.append(get_id(url))

            pl.save_file(args[1])



        case _:
            raise SyntaxError(f'Invalid command {sys.argv[1]}.')


if __name__ == "__main__":
    try:
        main()
    except SyntaxError as err:
        usage()
        raise err
