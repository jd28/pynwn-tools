### head_renamer v0.1

Renames/updates NWN head models/plt in bulk.

#### Setting up your input directories.
* Extract head MDLs and PLTs.

#### Setting up your input directories.
* Add your headmodels.2da to your output directory.

#### Command Line
```
usage: head_renamer [-h] [-v] [-t TWODA] [--use-nontoolset]
                    output input [input ...]

positional arguments:
  output                Output directory.
  input                 Input directories

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -t TWODA, --twoda TWODA
                        2da head lookup table. Default: headmodel.2da
  --use-nontoolset      Flag to se head model IDs that cannot be used in the
                        toolset.
```

#### Notes:
* `examples/heads/headmodel.2da` file is from CEP cepheadmodel.2da.  It's of no use
  to anything but the CEP crafting system, I think.  Its use
  here is just to get available head model entries.  If someone would
  like to contribute one without CEP entries...
* If you have your own 2da system, look at head_renamer.ini as to how
  to create look up tables from head model types.  Honestly, tho...the
  current program is limited to something that was identically
  formatted and structured.  Since an ID is considered available if
  the row entry doesn't equal the row number.  But it could have
  additional columns for your modules other races.
* This new model id is selected by the first available slot.  No clue
  if this a terrible idea.  There is an option to skip the model range
  that doesn't show in the toolset.

#### Examples:

Suppose you want to add
[Carcerian's animal and monster heads](http://neverwintervault.org/project/nwn1/model/pc-animal-and-monster-heads).
Your output directory will be just `output`.

1. Create your output directory and place your headmodel.2da into
   it.
2. Extract the animal heads zip to `animal` and monster heads zip to
   `monster`.
3. Run `head_renamer output/ animal/ monster/`

Then in your `output` directory you'll have all the renamed/updated
PLTs/MDLs and an updated headmodel.2da saved as headmodel.2da.new.
Adding new ones is as easy as following the same steps, except to you
use your new headmodel.2da.  You'd never want to add the same heads
twice, naturally.
