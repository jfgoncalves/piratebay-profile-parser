### Installation

[Download](https://github.com/jfgoncalves/piratebay-profile-parser/archive/develop.zip) and extract zipball.

Install the dependencies:

```sh
$ pip3 install -r requirements.txt
```

and make it executable:

```sh
$ chmod +x tpb.py
```

### Configuration

Make sure to edit `config.yml` and update all the fields to your needs.
Also edit line 74 to match the path of the config file and line 1 (shebang) of `tpb.py` to match your python3 path:
```sh
$ which python3
```

### Misc

I haven't tried, but the parser can probably work with search queries and content categories if you tweak line 18 and pass the full url via baseURL, though it'll probably be limited to the first page (30 items?) of results.

Outputed RSS will work with [Sonarr](https://github.com/Sonarr/Sonarr/) via the `Torrent RSS Feed` indexer. Make sure to set `Allow Zero Size` to `ON` and set `Minimum Seeders` to `0` just in case.
