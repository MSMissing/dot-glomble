import sys
import os

def version():
    print('dot-glomble v1.0')

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
    print('  --verision')
    print('    See the version of this app.')

def read(file):
    file.name
    return file.read()

def main():
    match sys.argv[1]:
        case 'create':
            if len(sys.argv) < 4:
                raise SyntaxError('create command requires two arguments')
            if not sys.argv[2].endswith('.glomble'):
                raise NameError('Filename must end with ".glomble"')
            if len(sys.argv[3]) != 12:
                raise TypeError(f'Invalid value {sys.argv[3]}')

            with open(sys.argv[2], 'x') as f:
                f.write(sys.argv[3])
            print(f'Successfully created {sys.argv[2]}')
        case 'detail':
            with open(sys.argv[2], 'r') as f:
                os.system(f'xdg-open https://glomble.com/videos/{f.read()}')
        case 'play':
            with open(sys.argv[2], 'r') as f:
                os.system(f'vlc https://glomble.com/videos/{f.read()}/download')
        case '--help' | '-h':
            version()
            print()
            usage()
        case 'version' | '--version':
            version()
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
