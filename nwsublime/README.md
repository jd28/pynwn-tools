### nwsublime

#### Description:
nwsublime is a utility that creates CTAGS files and sublime-completions for use with [Sublime](https://www.sublimetext.com/) text editor.

#### Installation
* Install CTags with [Package Control](https://packagecontrol.io/).  Note that you don't need to setup up the ctags path, unless you want to...  It won't work well with NWScript tho, so nwsublime includes [Exuberant CTAGS](http://ctags.sourceforge.net/)
* Install [STNeverwinterScript](https://github.com/CromFr/STNeverwinterScript#manual-install-) manually.  Note that if you install via PackageControl it will read

#### Usage:
```
usage: nwsublime.py [-h] scripts [scripts ...]

positional arguments:
  scripts     Input scripts

optional arguments:
  -h, --help  show this help message and exit
```

#### Settings:

See `nwsublime.ini`