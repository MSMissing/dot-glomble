# dot-glomble

A dedicated tool to save your favorite Glomble videos. I am not liable if this becomes outdated, especially the search function.

## Installation

i dunno man figure it out yourself.

## Requirements

Requires VLC. Probably some other things too.

## Syntax

`dot-glomble create <FILENAME> <VIDEO_ID>`

Creates a new .glomble file.

`dot-glomble detail <FILENAME>`

Shows a detailed view ow the .glomble file by opening it on glomble.com.

`dot-glomble play <FILENAME>`

Plays the .glomble file using VLC.

`dot-glomble download <FILENAME>`

Downloads the mp4/mov file from media.glomble.com

`dot-glomble playlist create <FILENAME>`

Creates a new (empty) playlist

`dot-glomble playlist add <FILENAME> <...VIDEOS>`

Adds videos to a playlist.

`dot-glomble playlist remove <FILENAME> <...VIDEOS>` or `dot-glomble playlist rm <FILENAME> <...VIDEOS>`

Removes videos from a playlist.

`dot-glomble playlist view <FILENAME>`

Shows a preview of the playlist. This only uses the video IDs so it's not exactly useful...

`dot-glomble playlist play <FILENAME>`

Plays a playlist using VLC.

`dot-glomble search <QUERY> <FILENAME>`

Searches Glomble for the *queer*y, then creates a playlist containing the videos.

`dot-glomble from-name <QUERY> <FILENAME>`

Searches Glomble for the query, then creates a video from the top result.
