### clothing_renamer v0.1

Renames/updates NWN clothes models/plt/tga in bulk and updates parts
2das.

#### Setting up your input directories.
* Extract MDLs, PLTs, parts 2DAs (not these are required).

#### Setting up your input directories.
* Extract your base parts 2DAs from Bioware 2da packages or your own
  top hak.

#### Notes:
* Inorder to rename any model the corresponding part 2da must be in
  both the input directory and the output directory.

#### Command Line
```
usage: clothing_renamer [-h] [-v] output input [input ...]

positional arguments:
  output         Output directory.
  input          Input directory

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

```

#### Examples:

Suppose you'd like to use Lisa's clothes and Shemsu-Heru: Arabian
Clothes from the CCC.  Your output directory will be just `output`

1. Extract parts 2DAs from
   [ShadoOow's 2da compilation](http://neverwintervault.org/project/nwn1/other/nwn-hordes-underdark-169-full-2da-source)
   or from your server's top hak into `output`.
   Note that this is how clothing renamer picks new model numbers.  It
   checks respective parts 2DAs for the highest row # and appends all
   models.  So if you want to control numbers all you have to do is
   add or delete rows.
2. Extract Lisa's stuff into directory `lisa` and Shemsu-Heru into
   `shemsu`.  These should have all the mdls, plts and their respective
   parts 2da files.
3. Run `clothing_renamer output/ lisa/ shemsu/`

Then in your `output` directory you'll have all the renamed/updated
PLTs/MDLs and all the parts 2DAs that you extracted in step #1 will be
updated with 2DA line entries for the new models.
