### tlkie v0.1

Tlkie is a command line program to convert TLK files to and from
[Meaglyn's TLS format](http://neverwintervault.org/project/nwn1/other/tool/meaglyns-nwn-tlk-compiler).
I believe I've faithfully implmented the TLS format.  Tlkie's command
line is somewhat different.

#### Command Line
```
usage: tlkie [-h] [-v] [-l LANGUAGE] output file [file ...]

positional arguments:
  output                Output TLK or TLS file.
  file                  TLK or TLS file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LANGUAGE, --language LANGUAGE
                        TLK language.  Default: English
```
