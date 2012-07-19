===========
DirPyLint
===========

DirPyLint is a tool for analyzing directories based on criteria specified in the config.yaml file.
It is used from the command line with this syntax::
    ./dirpylint.py

Configuration
=========

DirPyLint is achieved through the config.yaml file.

The file itself follows yaml standards, for more information on
yaml, visit 'the wikipedia page <http://en.wikipedia.org/wiki/YAML>'_.

Fields::

* For any field, if you wish it to be blank, leave one entry with the
text of False*

* levels indicates the total amount of levels down that you want
  DirPyLint to access.

* ignore_tree specifies any directories of sub-directories that you
  wish to have it ignore completely. Any directories specified here
  will have all of their sub-directories ignored as well.

* level<number> is the criteria for the level in question

* dirs indicates directory specifications

* files indicates file format specifications

* needs indicates what directories/files are necessary in the level

* optional indicates directories/files that are optional

* not indicates directories/files that should not be there

* ignore indicates level-specific directories/files to ignore. **NOTE**,
  this does not ignore sub-directories/files as well. Use 
  ignore_tree for that.

* regex allows users to define a regular expression pattern to match
  to their files/directories per level. 

Example Config File::

levels: 3

root: /home/Documents

ignore_tree:
    - False

level0:
    dirs:
        needs:
            - need2
            - need3
            - need4
        optional:
            - blah
            - blahblah
        not:
            - arg
        regex: "[0-9]"
        ignore:
            - need1
            - ignore
    files:
        types:
            - .mp3
            - .flac
            - .txt
        needs:
            - README.txt
        optional:
            - False
        not:
            - hah.txt
        regex: "[0-9]"
        ignore:
            - asd.mp3
