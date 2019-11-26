# pdfcombine

Simple command-line script that allows you to combine (concatenate) PDF-files:

```none
pdfcombine [options] <files>...
```

Note that the script is in fact a simple Python script that wraps Ghostscript. 

>   **Disclaimer**
>   
>   This library is free to use under the [MIT license](https://github.com/tdegeus/pdfcombine/blob/master/LICENSE). Any additions are very much appreciated, in terms of suggested functionality, code, documentation, testimonials, word-of-mouth advertisement, etc. Bug reports or feature requests can be filed on [GitHub](https://github.com/tdegeus/pdfcombine). As always, the code comes with no guarantee. None of the developers can be held responsible for possible mistakes.
>   
>   Download: [.zip file](https://github.com/tdegeus/pdfcombine/zipball/master) | [.tar.gz file](https://github.com/tdegeus/pdfcombine/tarball/master).
>   
>   (c - [MIT](https://github.com/tdegeus/pdfcombine/blob/master/LICENSE)) T.W.J. de Geus (Tom) | tom@geus.me | www.geus.me | [github.com/tdegeus/pdfcombine](https://github.com/tdegeus/pdfcombine)

# Contents

<!-- MarkdownTOC -->

- [Getting pdfcombine](#getting-pdfcombine)
  - [Using conda](#using-conda)
  - [Using PyPi](#using-pypi)
  - [From source](#from-source)
- [Usage](#usage)

<!-- /MarkdownTOC -->

# Getting pdfcombine

## Using conda

```bash
conda install -c conda-forge pdfcombine
```

## Using PyPi

```bash
pip install pdfcombine
```

## From source

```bash
# Download pdfcombine
git checkout https://github.com/tdegeus/pdfcombine.git
cd pdfcombine

# Install
python -m pip install .
```

# Usage

The usage is as follows (see `pdfcombine --help`):

```bash
pdfcombine
  Combine several PDFs to a single PDF.

Usage:
  pdfcombine [options] <files>...

Options:
      --openleft      Enforce that the next PDF always starts on an even page.
      --openright     Enforce that the next PDF always starts on an odd page.
      --title=<N>     Set the title  of the output PDF.
      --author=<N>    Set the author of the output PDF.
      --no-bookmarks  Do not use original filenames as bookmarks.
      --add-ps=<N>    Add commands to the generated PostScript program (inspect using '--verbose').
      --ps=<N>        Overwrite the automatically generated PostScript program.
      --no-ps         Do not run any PostScript program (to edit meta-data).
  -o, --output=<N>    Name of the output file. [default: binder.pdf]
  -f, --force         Force overwrite of existing output.
  -s, --silent        Do not print any progress.
      --verbose       Verbose all commands.
  -h, --help          Show help.
      --version       Show version.
```
