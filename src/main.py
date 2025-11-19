import sys
import os
import http.client as client
import urllib.request
import playlist
import search
import videos
import utils

def verbose(*args):
    print(*args)

def version():
    print('dot-glomble v1.1')

def usage():
    print('USAGE:')
    print('dot-glomble <FILE>')
    print('  Plays the Glomble file in VLC')
    print('dot-glomble <COMMAND>')
    print('  create <FILE> <VIDEO-ID>')
    print('    Creates a new .glomble file (not very useful)')
    print('  detail <FILE>')
    print('    Opens a detailed view of the video with your default browser. (May not work on some OSes)')
    print('  from-name <QUERY> <FILE>')
    print('    Finds the video with the closest match to QUERY, and creates a .glomble file from it.')
    print('  search <QUERY> <FILE>')
    print('    Searches for the query, and creates a playlist of results')
    print('  playlist <PLAYLIST-CMD>')
    print('    Playlist stuff')
    print('  help')
    print('    See this useful thingy')
    print('  version')
    print('    See the version of this app.')

def main():
    if len(sys.argv) < 2:
        usage()
        return

    args = sys.argv[2:]
    match sys.argv[1]:
        case 'create':
            videos.create_file(args[0], args[1])

        case 'detail':
            with open(args[0], 'r') as f:
                os.system(f'xdg-open https://glomble.com/videos/{f.read()}')

        case 'help':
            version()
            print()
            usage()

        case 'version':
            version()

        case 'download':
            if len(sys.argv) != 3:
                raise SyntaxError('Too many arguments.')
            if os.path.exists(args[0]):
                with open(args[0], 'r') as f:
                    video_id = f.read()
            else:
                video_id = args[0]
            (media, media_type) = videos.load_raw_video(video_id)
            with open('.'.join(args[0].split('.')[0:-1]) + videos.get_file_ext(media_type), 'wb') as f:
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
            print(f'Found video {videos.get_id_from_url(url)}.')
            videos.create_file(args[1], videos.get_id_from_url(url))

        case 'search':
            if len(args) < 2:
                raise SyntaxError('Not enough arguments')
            print(f'Searching glomble for {args[0]}')
            urls = search.search(args[0])
            print('found videos:')

            pl = playlist.Playlist()
            for url in urls:
                print(f' {videos.get_id_from_url(url)}')
                pl.videos.append(videos.get_id_from_url(url))

            pl.save_file(args[1])



        case _:
            if os.path.exists(sys.argv[1]):
                with open(sys.argv[1], 'r') as f:
                    content = f.read()
                if content.startswith('@PLAYLIST'):
                    playlist.play_playlist(playlist.Playlist.from_file(sys.argv[1]))
                else:
                    with open(sys.argv[1], 'r') as f:
                        os.system(f'vlc https://glomble.com/videos/{f.read()}/download')
            else:
                raise SyntaxError(f'Invalid command {sys.argv[1]}.')


if __name__ == "__main__":
    try:
        main()
    except SyntaxError as err:
        usage()
        raise err
