'''pdfcombine
    Combine several PDFs to a single PDF.

    By default a PostScript script is used to set the meta-data of the output PDF-file.
    In particular, the output PDF gets a table of contents with bookmarks to the first page
    of each input 'document' and the input filename at title.
    To customise these titles and add meta-data use a YAML input file and/or
    customise the default PostScript script.

    Manipulate PostScript script:

    *   Customise:

            title
                Set title of the output PDF.

            author
                Set the author of the output PDF.

            no-bookmarks
                Switch-off bookmarks added for each 'document'.

            add-ps
                Add lines of PostScript code to the automatically generated script.

    *   Manually specify:

            ps
                Set PostScript script (overwrites automatically generated script).

    *   Suppress:

            no-ps
                Switch-off the use of a PostScript script.

    To include custom bookmarks a YAML input file can be used, e.g.::

        files:
            - file: 1.pdf
              title: First file
            - file: 2.pdf
              title: Second file

        openleft: True
        title: Binder
        author: Tom de Geus
        output: binder.pdf
        ...

    As observed the `files` field contains all input files (in the correct order) and the
    bookmark titles. In addition, any of the command-line options (long name without `--`)
    can be included. Note that specifying them will overwrite the corresponding
    command-line option. To use with automatic bookmarks (i.e. filenames),
    the above input file can be shortened to::

        files:
            - 1.pdf
            - 2.pdf

        openleft: True
        title: Binder
        author: Tom de Geus
        output: binder.pdf

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

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/pdfcombine
'''

import docopt
import click
import os
import sys

from .. import __version__
from .. import combine


def error(text):
    r'''
Command-line error: show message and quit with exit code "1"
    '''

    print(text)
    sys.exit(1)


def read_yaml(files):
    r'''
Read YAML file.
    '''

    import yaml

    if len(files) != 1:
        error('All input PDFs need to be specified in the YAML input')

    filename = files[0]

    if not os.path.isfile(filename):
        error('"{0:s} does not exist'.format(filename))

    return yaml.load(open(filename, 'r').read(), Loader=yaml.FullLoader)


def main():
    r'''
Main program.
    '''

    args = docopt.docopt(__doc__, version=__version__)

    files = args['<files>']
    output = args['--output']
    openleft = args['--openleft']
    openright = args['--openright']
    ps = args['--ps']
    add_ps = args['--add-ps']
    meta = not args['--no-ps']
    bookmarks = not args['--no-bookmarks']
    title = args['--title']
    author = args['--author']
    verbose = args['--verbose']
    silent = args['--silent']

    if args['--yaml']:

        info = read_yaml(files)

        if 'files' in info:
            if len(info['files']) > 0:
                if type(info['files'][0]) == dict:
                    files = [i['file'] for i in info['files']]
                    bookmarks = [i['title'] for i in info['files']]
                else:
                    files = [i for i in info['files']]

        if 'output' in info:
            output = info['output']

        if 'openleft' in info:
            openleft = info['openleft']

        if 'openright' in info:
            openright = info['openright']

        if 'ps' in info:
            ps = info['ps']

        if 'add-ps' in info:
            add_ps = info['add-ps']

        if 'bookmarks' in info:
            bookmarks = info['bookmarks']

        if 'title' in info:
            title = info['title']

        if 'author' in info:
            author = info['author']

        if 'verbose' in info:
            verbose = info['verbose']

        if 'silent' in info:
            silent = info['silent']

        if 'no-ps' in info:
            if info['no-ps']:
                meta = False

    if os.path.isfile(output) and not args['--force']:
        if not click.confirm('Overwrite existing "{0:s}"?'.format(output)):
            sys.exit(1)

    try:
        combine(
            files=files,
            output=output,
            openleft=openleft,
            openright=openright,
            meta=meta,
            ps=ps,
            add_ps=add_ps,
            bookmarks=bookmarks,
            title=title,
            author=author,
            verbose=verbose)
    except Exception as e:
        print(str(e))
        sys.exit(1)

    if not silent:
        print('[pdfcombine] {0:s}'.format(output))


if __name__ == '__main__':

    main()
