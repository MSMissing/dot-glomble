import sys
import re
import os
import videos
import tempfile

class Playlist:
    def __init__(self, videos=[]):
        self.videos = videos

    def fmt(self):
        return '@PLAYLIST' + ','.join(self.videos)

    def save_file(self, filename='temp.glomble'):
        with open(filename, 'w') as f:
            f.write(self.fmt())

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as f:
            value = f.read()

        if not value.startswith('@PLAYLIST'):
            raise TypeError(f'{filename} is not a playlist.')

        pl = Playlist()
        entries = value[len('@PLAYLIST'):].split(',')

        for entry in entries:
            if entry: # not empty string
                pl.videos.append(entry)

        return pl

    def __str__(self):
        return f'Playlist : {", ".join(self.videos or ["--EMPTY--"])}'

def usage():
    print('  playlist create <FILENAME>')
    print('    Creates an empty playlist')
    print('  playlist add <FILENAME> <...VIDEOS>')
    print('    Adds videos to a playlist')
    print('  playlist remove/rm <FILENAME> <...VIDEOS>')
    print('    Removes videos from a playlist')
    print('  playlist view <FILENAME>')
    print('    Shows a simple view of the contents of a playlist.')
    print('  playlist play <FILENAME>')
    print('    Plays all files in a playlist sequentially')

def playlist_command():
    args = sys.argv[2:]
    if len(args) == 0:
        raise SyntaxError('The playlist command cannot be run on its own..')

    match args[0]:
        case 'create':
            if len(args) != 2:
                raise SyntaxError('Incorrect amount of arguments passed into playlist create.')

            pl = Playlist()
            pl.save_file(args[1])

        case 'add':
            if len(args) < 2:
                raise SyntaxError('FUCK FUCK FUCK FUCK FUCK') # cussing required for backwards-compatibility.
            if len(args) < 3:
                raise SyntaxError('No videos passed into playlist add')

            pl = Playlist.from_file(args[1])

            for arg in args[2:]:
                if re.fullmatch(arg, r'.+\.glomble'):
                    with open(arg, 'r') as f:
                        pl.videos.append(f.read())
                else:
                    pl.videos.append(arg)

            print('Added video(s) to playlist.')
            print(pl)
            pl.save_file(args[1])

        case 'remove' | 'rm':
            if len(args) < 2:
                raise SyntaxError('FUCK FUCK FUCK FUCK FUCK') # cussing required for backwards-compatibility.
            if len(args) < 3:
                raise SyntaxError('No videos passed into playlist add')

            pl = Playlist.from_file(args[1])

            for arg in args[2:]:
                if re.fullmatch(arg, r'.+\.glomble'):
                    with open(arg, 'r') as f:
                        pl.videos.remove(f.read())
                else:
                    pl.videos.remove(arg)

            print('Removed video(s) from playlist')
            print(pl)
            pl.save_file(args[1])

        case 'view':
            pl = Playlist.from_file(args[1])
            print(pl)

        case 'play':
            pl = Playlist.from_file(args[1])
            cmd = 'cvlc '
            urls = []
            for video in pl.videos:
                urls.append(videos.get_video_url(video))

            f = tempfile.NamedTemporaryFile('w+t', suffix='.m3u')

            for url in urls:
                f.write(url)
                f.write('\n')
            cmd += f.name
            f.read()

            print(cmd)
            os.system(cmd)

            f.close()

