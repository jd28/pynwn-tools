### 2dilate v0.4

#### Description:
2dilate is a new (and slightly different) 2da merger.  It adds a new
file type: 2dx (specification below).  To simplify and ease the 2da
merging process.

#### Goals:
* A merger that did not require using directories to separate multiple
  merge files.
* A file format that is simple, compact, and familiar.  Something that
  could ideally be distributed with custom content to ease merging or
  shared by community members.  And also trivially implementable in
  any programming language/environment.
* A simple straight forward interface, that does not require a PhD to learn.

#### 2dx file format version 2.1

* Header: **2DX V2.1**
* YAML Metadata: The following is optional if not specified there must be one blank line between the Header and
  the Column Labels.  The YAML metadata is enclosed within two lines containing
  "---".  If you are not familiar with YAML visit [yaml.org](http://www.yaml.org/).
  Please note that you can put _anything_ in the metadata so long as it
  conforms to the YAML specification.  Anything that 2dx doesn't understand, it ignores.
  **Note**: YAML does not like tabs, you should always uses spaces for indentation.
* Column Labels: As 2da, note however that a 2dx file needn't have all
  the columns of it's parent 2da.  Only the columns that are being
  merged need to be included.  Also, new columns can be added.
* Rows: As 2da with a couple exceptions:
  * Row numbers are significant, this is how 2dilate decides where to
    merge the 2dx file.
  * Row numbers are not expected to start from 0, they should be start
    wherever you want to merge.  They need not be contiguous or even
    ordered.
  * **####** is a new entry type that tells 2dilate to ignore the row
    entry as far as merging goes.  This is very handy when you want to
    merge changes from a few different columns but only change some
    values on certain rows.

Reserved YAML Metadata Entries:

* `description` - A string description for prompting users.
* `tlk` - A table of column names and integer offsets.
* `column_rename` - A table of old column names and new column names.

Example:

```yaml
---
description: |
  This renames some columns and modifies some TLK entries.

tlk:
  SomeColumn: 1000 # For all non-empty column entries the TLK entry will be calculated
  Column2: 1500    # offset + column entry + 0x01000000 (Custom TLK starting point).

column_rename:
  OldColumnName: NewColumnName   # OldColumnName will be renamed to NewColumnName.
  OldColumnName1: NewColumnName2 # There can be any number of these.

date: 2015-07-04 # Custome metadata entry.  Note that 2dilate and the 2dx reader will simply
                 # ignore this.
---
```

#### 2dx file format version 2.0 (**OBSOLETE**).
* Header: **2DX V2.0**
* Specifications: The following lines are optional, their ordering
  does not matter.  Their contents are limited to a single line.  If
  none are used there must be one blank line between the Header and
  the Column Labels.
  * **TLK: \<offset\> (\<Column Label\>, ...)** - Any number of Column
    Labels can be used, they must be lines referencing tlk entries.
  * **DESCRIPTION: \<Some text\>** - This will be used in future
    versions to prompt users as to whether or not they'd like to merge
    a particular 2dx file.
* Column Labels: As 2da, note however that a 2dx file needn't have all
  the columns of it's parent 2da.  Only the columns that are being
  merged need to be included.  Also, new columns can be added.
* Rows: As 2da with a couple exceptions:
  * Row numbers are significant, this is how 2dilate decides where to
    merge the 2dx file.
  * Row numbers are not expected to start from 0, they should be start
    wherever you want to merge.  They need not be contiguous or even
    ordered.
  * **####** is a new entry type that tells 2dilate to ignore the row
    entry as far as merging goes.  This is very handy when you want to
    merge changes from a few different columns but only change some
    values on certain rows.

#### Command Line Usage:

```
usage: 2dilate [-h] [-v] [-o OUTPUT] [--non-default] twodx files [files ...]

positional arguments:
  twodx                 Directory containing 2dx files.
  files                 2da file(s).

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        Output directory.  Default: merged.
  --non-default         Ignore non-default 2da row entries.

```

#### Change Log
* v0.4:
  * Introduce TwoDX v2.1 and YAML metadata header.
    This will simplify any feature additions in the future, as well
    as allowing anyone to add any metadata that they find useful.
  * Fix file globbing in the windows command shell.

* v0.3:
  * Add Yes/No/All prompt before merging.
