# pdfcombine

[![Travis](https://travis-ci.org/tdegeus/pdfcombine.svg?branch=master)](https://travis-ci.org/tdegeus/pdfcombine)
[![Build status](https://ci.appveyor.com/api/projects/status/d0v6sudee1m7iuvh?svg=true)](https://ci.appveyor.com/project/tdegeus/pdfcombine)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pdfcombine.svg)](https://anaconda.org/conda-forge/pdfcombine)


Simple command-line script that allows you to combine (concatenate) PDF-files.

```none
pdfcombine [options] <files>...
```

Note that the script is in fact a simple Python script that wraps GhostScript. 
Also not that a simple Python module is also available to do the same thing.

# Contents

<!-- MarkdownTOC -->

- [Disclaimer](#disclaimer)
- [Getting pdfcombine](#getting-pdfcombine)
  - [Using conda](#using-conda)
  - [Using PyPi](#using-pypi)
  - [From source](#from-source)
- [Usage](#usage)
  - [Meta-data using PostScript](#meta-data-using-postscript)
  - [YAML input file](#yaml-input-file)
- [Usage from Python](#usage-from-python)
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

This will also install all necessary dependencies.

## Using PyPi

```bash
pip install pdfcombine
```

This will also install the necessary Python modules, **but not GhostScript**.

## From source

```bash
# Download pdfcombine
git checkout https://github.com/tdegeus/pdfcombine.git
cd pdfcombine

# Install
python -m pip install .
```

This will also install the necessary Python modules, **but not GhostScript**.

# Usage

The usage is as follows (see `pdfcombine --help`):

```bash
Usage:
    pdfcombine [options] <files>...

Options:
    -y, --yaml              Read input files (and settings) from a YAML-file.
        --openleft          Enforce that each 'chapter' starts on an even page.
        --openright         Enforce that each 'chapter' starts on an odd page.
        --title=<arg>       Set the title of the output PDF.
        --author=<arg>      Set the author of the output PDF.
        --no-bookmarks      Do not write
        --add-ps=<arg>      Add commands to the generated PostScript script.
        --ps=<arg>          Overwrite the automatically generated PostScript script.
        --no-ps             Do not run any PostScript script (to edit meta-data).
    -o, --output=<arg>      Name of the output file. [default: binder.pdf]
    -f, --force             Force overwrite of existing output.
    -s, --silent            Do not print any progress.
        --verbose           Verbose all commands.
    -h, --help              Show help.
        --version           Show version.
```

## Meta-data using PostScript

By default a PostScript script is used to set the meta-data of the output PDF-file.
This default PostScript script can be:

+   Customised:

    `--title`
        Set title of the output PDF.

    `--author`
        Set the author of the output PDF.

    `--no-bookmarks`
        Switch-off bookmarks added for each 'document'.

    `--add-ps`
        Add custom PostScript code, to the automatically generated script.

+   Manually specified:

    `--ps`
        Set PostScript script (overwrites automatically generated script).

+   Suppressed:

    `--no-ps`
        Switch-off the use of a PostScript script.

## YAML input file

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

As observed the `files` field contains all input files (in the correct order) and the
bookmark titles. Other field allowed any of the command-line options (long name without `--``);
specifying them will overwrite the corresponding command-line option.
To use with automatic bookmarks, e.g.:

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

From Python one can use:

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
    
    Make sure each 'document' begins on a left-page.

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
    PostScript script. One can customise the bookmarks by specifying one label per file.

+   `title` (`<str>`)
    
    Specify PDF title. Defaults to "Binder".

+   `author` (`<str>`)
    
    Specify PDF author. Defaults to "pdfcombine".

+   `verbose` (**`False`** | `True`)
    
    Verbose all commands and their output.
