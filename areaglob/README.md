### areaglob v0.1

areaglob is command line utility to take a bunch of ini files in the
areag.ini format and smush them in to one.  There are command line
options for setting the script settings for all the final areag.ini
tileset entries.

See the areag folder in the 7z for how you'd use it.  Most tileset
haks seem to come with a merged one, so there is a lot of needless
duplication in those files.

#### Command Line Arguments:
```
usage: areaglob [-h] [-v] [-e ENTER] [-x EXIT] [-b HEARTBEAT] [-u USER]
                base output input [input ...]

positional arguments:
  base                  Base areag.ini file.
  output                Output ini file.
  input                 Input ini files.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -e ENTER, --enter ENTER
                        OnEnter Script.
  -x EXIT, --exit EXIT  OnExit Script.
  -b HEARTBEAT, --heartbeat HEARTBEAT
                        OnHeartbeat Script.
  -u USER, --user USER  OnUserDefined Script.

```
