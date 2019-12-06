'''pdfcombine
  Combine several PDFs to a single PDF.

  Note that by default a PostScript script is used to set the meta-data of the output PDF-file.
  This default PostScript script can be customised (--title, --author, --no-bookmarks, --add-ps),
  completely manually specified (--ps), or suppressed altogether (--no-ps).

Usage:
  pdfcombine [options] <files>...

Options:
      --openleft      Enforce that the next PDF always starts on an even page.
      --openright     Enforce that the next PDF always starts on an odd page.
      --title=<N>     Set the title of the output PDF.
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

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me
'''

# ==================================================================================================

import sys
import os
import re
import subprocess
import shutil
import tempfile
import docopt
import click

__version__ = '1.0.0'

# --------------------------------------------------------------------------------------------------
# Command-line error: show message and quit with exit code "1"
# --------------------------------------------------------------------------------------------------

def Error(text):

    print(text)
    sys.exit(1)

# --------------------------------------------------------------------------------------------------
# Run command (and verbose it), and return the command's output
# --------------------------------------------------------------------------------------------------

def Run(cmd, verbose=False):

    out = subprocess.check_output(cmd, shell=True).decode('utf-8')

    if verbose:
        print(cmd)
        print(out)

    return out

# --------------------------------------------------------------------------------------------------
# Read number of pages of each document
# --------------------------------------------------------------------------------------------------

def NumberOfPages(files, verbose=False):

    if verbose:
        print('\n---- reading number of pages per file ----')

    n_pages = []

    for file in files:
        cmd = 'gs -q -dNODISPLAY -c "({0:s}) (r) file runpdfbegin pdfpagecount = quit"'.format(file)
        out = Run(cmd, verbose)
        n_pages += [int(out)]

    return n_pages

# --------------------------------------------------------------------------------------------------
# Construct default PostScript script
# --------------------------------------------------------------------------------------------------

def DefaulPostScript(files, n_pages, title, author, bookmarks=True):

    out = []

    if title:
        out += ['/Title ({0:s})'.format(title)]

    if author:
        out += ['/Author ({0:s})'.format(author)]

    if bookmarks:
        i = 1
        for file, n in zip(files, n_pages):
            out += ['/Page {0:d} /Title ({1:s}) /OUT pdfmark'.format(i, file)]
            i += n

    return '[ ' + '\n[ '.join(out)

# --------------------------------------------------------------------------------------------------
# Main routine
# --------------------------------------------------------------------------------------------------

def main():

    args = docopt.docopt(__doc__, version=__version__)

    # Change keys to simplify implementation:
    # - remove leading "-" and "--" from options
    # - change "-" to "_" to facilitate direct use in print format
    # - remove "<...>"
    args = {re.sub(r'([\-]{1,2})(.*)',r'\2',key): args[key] for key in args}
    args = {key.replace('-','_'): args[key] for key in args}
    args = {re.sub(r'(<)(.*)(>)',r'\2',key): args[key] for key in args}

    if not shutil.which('gs'):
        Error('"gs" not found')

    if args['openright'] and args['openleft']:
        Error('"--openright" and "--openleft" are exclusive options')

    for file in args['files']:
        if not os.path.isfile(file):
            Error('"{0:s}" does not exist'.format(file))

    for file in args['files']:
        if os.path.abspath(file) == os.path.abspath(args['output']):
            Error('"{output:s}" is also an input-file, this might cause problems'.format(**args))

    if os.path.isfile(args['output']) and not args['force']:
        if not click.confirm('Overwrite existing "{output:s}"'.format(**args)):
            sys.exit(1)

    # Read number of pages
    if args['openleft'] or args['openright'] or not args['no_bookmarks']:
        n_pages = NumberOfPages(args['files'], args['verbose'])
        is_even = [False if n % 2 != 0 else True for n in n_pages]

    # Store PostScript commands to set metadata in a temporary file
    if not args['no_ps']:

        # Generate (or read) PostScript commands to set metadata
        if args['ps']:
            ps = args['ps']
        else:
            ps = DefaulPostScript(
              files = args['files'],
              n_pages = n_pages,
              title = args['title'],
              author = args['author'],
              bookmarks = not args['no_bookmarks'])

        # Add PostScript commands from command-line
        if args['add_ps']:
            ps += '\n' + args['add_ps']

        # Store in temporary file
        tempFile = os.path.join(tempfile.mkdtemp(), 'pdfcombine.ps')
        open(tempFile, 'w').write(ps)
        if args['verbose']:
            print('\n---- created "{0:s}" ----\n\n{1:s}'.format(tempFile, ps))

    # Construct GhostScript command to combine PDFs
    if True:

        if args['verbose']:
            print('\n---- combining files ----\n')

        cmd = 'gs -sDEVICE=pdfwrite -dBATCH -dNOPAUSE -q -sPAPERSIZE=a4 -o "{output:s}"'.format(
          **args)

        # Open left: start with a blank page
        if args['openleft']:
            cmd += ' -c showpage'

        # Loop of insert the files in order of appearance
        # Optionally insert banks page if the previous document had an odd number of pages
        for i, file in enumerate(args['files']):
            if i > 0:
                if (args['openleft'] or args['openright']) and not is_even[i-1]:
                    cmd += ' -c showpage'
            cmd += ' -f "{0:s}"'.format(file)

        # Add pdfmarks
        if not args['no_ps']:
            cmd += ' ' + tempFile

    # Execute the GhostScript command
    Run(cmd, args['verbose'])

    # Clean-up: remove temporary file and directory
    if not args['no_ps']:
        if args['verbose']:
            print('\n---- cleaning up ----\n')
        shutil.rmtree(os.path.split(tempFile)[0])
        if args['verbose']:
            print('rm -r {tempFile:s}'.format(tempFile=tempFile))

    # Print progress
    if not args['silent']:
        print('[pdfcombine] {output:s}'.format(**args))

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
