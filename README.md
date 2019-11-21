# pdfcombine

Combine PDF files with Ghostscript.

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
    - [From source](#from-source)
- [Create a new release](#create-a-new-release)

<!-- /MarkdownTOC -->

# Getting pdfcombine

## Using conda

```bash
conda install -c conda-forge pdfcombine
```

## From source

```bash
# Download pdfcombine
git checkout https://github.com/tdegeus/pdfcombine.git
cd pdfcombine

# Install
cmake .
make install
```
# Create a new release

1.  Update the version number in `pdfcombine`. 

2.  Upload the changes to GitHub and create a new release there (with the correct version number).

3.  Update the package at [conda-forge](https://github.com/conda-forge/pyxtensor-feedstock).
