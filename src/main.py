import sys
import os
import http.client as client
import urllib.request
import playlist
import search
from videos import *

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
