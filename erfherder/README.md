### erfherder v0.1

erfherder is a command line application for modifying / working with
Bioware ERF file formats (HAK, MOD, ERF) with a git style interface.

##### `erfherder pack`

```
usage: erfherder pack [-h] [--exclude EXCLUDE] output input [input ...]

Pack files and directories into an ERF file.

positional arguments:
  output             Output ERF. Extension determines ERF type.
  input              Add files/directories to add.

optional arguments:
  -h, --help         show this help message and exit
  --exclude EXCLUDE  Exclude files, directories, patterns.
                     Can be used multiple times.
```

Notes:
* `erfherder pack` when given a directory, all sub-directories are walked.


##### `erfherder dump`

```
usage: erfherder dump [-h] [-p PATTERN] input output

Dump files from an ERF.

positional arguments:
  input                 Source ERF.
  output                Output directory.

optional arguments:
  -h, --help            show this help message and exit
  -p PATTERN, --pattern PATTERN
                        Unix wildcard pattern.
```

##### `erfherder ls`

```
usage: erfherder ls [-h] input

List files from an ERF.

positional arguments:
  input       Source ERF.

optional arguments:
  -h, --help  show this help message and exit
```

##### `erfherder rm`

```
usage: erfherder rm [-h] [-o OUTPUT] input pattern

Remove files from an ERF.

positional arguments:
  input                 Source ERF.
  pattern               File name or quoted unix file pattern.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output ERF. Optional.
```
