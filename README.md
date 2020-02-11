# pdfcombine

[![Travis](https://travis-ci.org/tdegeus/pdfcombine.svg?branch=master)](https://travis-ci.org/tdegeus/pdfcombine)
[![Build status](https://ci.appveyor.com/api/projects/status/d0v6sudee1m7iuvh?svg=true)](https://ci.appveyor.com/project/tdegeus/pdfcombine)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pdfcombine.svg)](https://anaconda.org/conda-forge/pdfcombine)


Simple module to combine (concatenate) PDF-files using GhostScript:

## Command-line script 

```none
pdfcombine [options] <files>...
```

## Python module

```python
import pdfcombine
pdfcombine.combine(...)
```

# Contents

<!-- MarkdownTOC -->

- [Disclaimer](#disclaimer)
- [Getting pdfcombine](#getting-pdfcombine)
    - [Using conda](#using-conda)
    - [Using PyPi](#using-pypi)
    - [From source](#from-source)
- [Usage](#usage)
    - [Basic usage](#basic-usage)
    - [Meta-data using PostScript](#meta-data-using-postscript)
    - [Manipulate PostScript script from command-line](#manipulate-postscript-script-from-command-line)
        - [Customise](#customise)
        - [Manually specify](#manually-specify)
        - [Suppress](#suppress)
    - [Customise meta-data using YAML input file](#customise-meta-data-using-yaml-input-file)
- [Usage from Python](#usage-from-python)
    - [Basic usage](#basic-usage-1)
    - [Arguments](#arguments)
    - [Options](#options)

<!-- /MarkdownTOC -->

# Disclaimer

This library is free to use under the [MIT license](https://github.com/tdegeus/pdfcombine/blob/master/LICENSE). Any additions are very much appreciated, in terms of suggested functionality, code, documentation, testimonials, word-of-mouth advertisement, etc. Bug reports or feature requests can be filed on [GitHub](https://github.com/tdegeus/pdfcombine). As always, the code comes with no guarantee. None of the developers can be held responsible for possible mistakes.

Download: [.zip file](https://github.com/tdegeus/pdfcombine/zipball/master) | [.tar.gz file](https://github.com/tdegeus/pdfcombine/tarball/master).

(c - [MIT](https://github.com/tdegeus/pdfcombine/blob/master/LICENSE)) T.W.J. de Geus (Tom) | tom@geus.me | www.geus.me | [github.com/tdegeus/pdfcombine](https://github.com/tdegeus/pdfcombine)

# Getting pdfcombine

## Using conda

```bash
conda install -c conda-forge pdfcombine
```

This will install all necessary dependencies.

## Using PyPi

```bash
pip install pdfcombine
```

This will install the necessary Python modules, **but not GhostScript**.

## From source

```bash
# Download pdfcombine
git checkout https://github.com/tdegeus/pdfcombine.git
cd pdfcombine

# Install
python -m pip install .
```

This will install the necessary Python modules, **but not GhostScript**.

# Usage

## Basic usage

The usage is as follows (see `pdfcombine --help`):

```
Usage:
    pdfcombine [options] <files>...

Options:
    -y, --yaml              Read input files (and settings) from a YAML-file.
        --openleft          Enforce that each 'chapter' starts on an even page.
        --openright         Enforce that each 'chapter' starts on an odd page.
        --title=<arg>       Set the title of the output PDF.
        --author=<arg>      Set the author of the output PDF.
        --no-bookmarks      Do include bookmarks to the first page of each document.
        --add-ps=<arg>      Add commands to the generated PostScript script.
        --ps=<arg>          Overwrite the automatically generated PostScript script.
        --no-ps             Do not run any PostScript script (to edit meta-data).
    -o, --output=<arg>      Name of the output file. [default: binder.pdf]
    -f, --force             Force overwrite of existing output-file.
    -s, --silent            Do not print any progress.
        --verbose           Verbose all commands.
    -h, --help              Show help.
        --version           Show version.
```

## Meta-data using PostScript

By default a PostScript script is used to set the meta-data of the output PDF-file. 
In particular, the output PDF gets a table of contents with bookmarks to the first page of each input 'document' and the input filename at title. To customise these titles and add meta-data use a [YAML input file](#yaml-input-file) and/or [customise](#customise-postscript-script) the default PostScript script.

## Manipulate PostScript script from command-line

### Customise

`--title`
    
Set title of the output PDF.

`--author`
    
Set the author of the output PDF.

`--no-bookmarks`
    
Switch-off bookmarks added for each 'document'.

`--add-ps`
    
Add lines of PostScript code to the automatically generated script.

### Manually specify

`--ps`
    
Set PostScript script (overwrites automatically generated script).

### Suppress

`--no-ps`
    
Switch-off the use of a PostScript script.

## Customise meta-data using YAML input file

To include custom bookmarks a YAML input file can be used, e.g.:

```yaml
files:
    - file: 1.pdf
      title: First file
    - file: 2.pdf
      title: Second file

openleft: True
title: Binder
author: Tom de Geus
output: binder.pdf
```

>   Run *pdfcombine* as follows:
>   
>       pdfcombine -y input.yaml
>       
>   All PDFs have the specified in the YAML file: 
>   no additional PDFs can be added from the command-line.

As observed the `files` field contains all input files (in the correct order) and the
bookmark titles. 
In addition, any of the command-line options (long name without `--`) can be included. 
Note that specifying them will overwrite the corresponding command-line option.
To use with automatic bookmarks (i.e. filenames), the above input file can be shortened to:

```yaml
files:
    - 1.pdf
    - 2.pdf

openleft: True
title: Binder
author: Tom de Geus
output: binder.pdf
```

# Usage from Python

## Basic usage

```python
import pdfcombine
pdfcombine.combine(...)
```

## Arguments

+   `files` (`<str>` | `<list<str>>`)
    
    List of PDF files to combine.

+   `output` (`<str>`)
    
    Name of output file (overwritten if exists).

## Options

+   `openleft` (**`False`** | `True`)
    
    Make sure each 'document' begins on a left-page.

+   `openright` (**`False`** | `True`)
    
    Make sure each 'document' begins on a right-page.

+   `meta` (**`True`** | `False`)
    
    Write meta-data using a PostScript script
    (see below for options: `ps`, `add_ps`, `bookmarks`, `title`, `author`).

+   `ps` (`<str>`)
    
    If specified the automatically generated PostScript script is overwritten with
    the specified script.

+   `add_ps` (`<str>`)
    
    Append generated/specified PostScript script with the specified script.

+   `bookmarks` (**`True`** | `False` | `<list<str>>`)
    
    If `True` the filenames are used as bookmarks in the automatically generated
    PostScript script. One can customise the bookmarks by specifying a list with 
    one label per file.

+   `title` (`<str>`)
    
    Specify PDF title. Defaults to "Binder".

+   `author` (`<str>`)
    
    Specify PDF author. Defaults to "pdfcombine".

+   `verbose` (**`False`** | `True`)
    
    Verbose all commands and their output.
