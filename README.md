[![PyPI version](https://badge.fury.io/py/musicmaster.svg)](https://badge.fury.io/py/musicmaster)

# Music

![example view](examples/artists.png?raw=true)

A project to analyze your favorite music

The package achieves this by:
* Letting you select your favorite artists in a web interface
    * Search for new artists with search bar
    * Click on suggestions provided by AI recommender system
* Downloading the songs of your favorite artists
    * All songs if the artist is marked as favorite
    * Top 10 songs otherwise
* Letting you select your favorite songs to download in a web interface
* Postprocessing the downloaded songs:
    * Adding lyrics, title, ...
    * Settings the modified time to the release date of the song 
        * useful for ordering
* Keeping track of all downloaded songs and only downloading new songs

## Installation

1) Install [npm](https://www.npmjs.com/)
2) Install the package
    ```shell
    pip install musicmaster
    ```
    
Developed for linux OS

## Usage
1) Start webapp server to manage liked/favorite artists:
    ```shell
    musicserver
    ```
2) Download new songs:
    ```shell
    music
    ```

![progress example](examples/updating.png?raw=true)

Make sure you have the following variables defined in your environment:
* SPOTAPI_ID:
* SPOTAPI_SECRET

obtain [here](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)
