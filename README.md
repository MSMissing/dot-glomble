# dot-glomble

A dedicated tool to save your favorite Glomble videos. I am not liable if this becomes outdated, especially the search function.

## Installation

i dunno man figure it out yourself.

## Requirements

### OS

This was made using SteamOS, and uses Bash. Probably won't work on windows?

### Apps

Requires VLC

## Syntax

`dot-glomble create <FILE> <VIDEO_ID>`

Creates a new .glomble file.

`dot-glomble detail <FILE>`

Shows a detailed view ow the .glomble file by opening it on glomble.com.

`dot-glomble play <FILE>`

Plays the .glomble file using VLC.

`dot-glomble download <FILE>`

Downloads the mp4/mov file from media.glomble.com

`dot-glomble playlist create <FILE>`

Creates a new (empty) playlist

`dot-glomble playlist add <FILE> <...VIDEOS>`

Adds videos to a playlist.

`dot-glomble playlist rm <FILE> <...VIDEOS>`

Removes videos from a playlist.

`dot-glomble playlist view <FILE>`

Shows a preview of the playlist. This only uses the video IDs so it's not exactly useful...

`dot-glomble playlist play <FILE>`

Plays a playlist using VLC.

`dot-glomble search <QUERY> <FILE>`

Searches Glomble for the *queer*y, then creates a playlist containing the videos.

`dot-glomble from-name <QUERY> <FILE>`

Searches Glomble for the query, then creates a video from the top result.
