import sys
import re

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
        return f'Playlist - Videos: {", ".join(self.videos)}'

def usage():
    print('  playlist create')
    print('    Creates a playlist')

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


