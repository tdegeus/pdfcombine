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

import os
import subprocess
import shutil
import tempfile
from itertools import accumulate

__version__ = '1.1.0'

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
        print('\n---- reading number of pages per file ----\n')

    n_pages = []

    for file in files:
        cmd = 'gs -q -dNODISPLAY -c "({0:s}) (r) file runpdfbegin pdfpagecount = quit"'.format(file)
        out = Run(cmd, verbose)
        n_pages += [int(out)]

    return n_pages

# --------------------------------------------------------------------------------------------------
# Construct default PostScript script
# --------------------------------------------------------------------------------------------------

def DefaultPostScript(files, start_page, title, author, bookmarks=True):

    out = []

    if title:
        out += ['/Title ({0:s})'.format(title)]

    if author:
        out += ['/Author ({0:s})'.format(author)]

    if type(bookmarks) == str:
        bookmarks = [bookmarks]
    if type(bookmarks) != list:
        bookmarks = [i for i in files]

    if bookmarks:
        for title, page in zip(bookmarks, start_page):
            out += ['/Page {0:d} /Title ({1:s}) /OUT pdfmark'.format(page, title)]

    return '[ ' + '\n[ '.join(out)

# --------------------------------------------------------------------------------------------------
# Combine PDFs
# --------------------------------------------------------------------------------------------------

def combine(
        files, # list of files
        output, # name of output file (overwritten if exists)
        openleft = False, # True/False
        openright = False, # True/False
        ps = True, # None/True -> generate automatically, str -> Use user input, False = switch off
        add_ps = None, # str, to append generated PostScript script
        bookmarks = True, # True -> use filename, list(str) -> specify per file
        title = 'Binder', # title of output PDF
        author = 'pdfcombine', # author of output PDF
        verbose = False, # verbose
    ):
    r'''
Combine PDFs

:arguments:

        **files** (``<str>`` | ``<list<str>>``)
            List of PDF files to combine.

        **output** (``<str>``)
            Name of output file (overwritten if exists).

:options:

        **openleft** ([``False``] | ``True``)
            Make sure each 'chapter' begins on a left-page.

        **openright** ([``False``] | ``True``)
            Make sure each 'chapter' begins on a left-page.

        **ps** ([``True``] | ``False`` | ``<str>``)
            If ``True``: generate a PostScript script with set title, author, and bookmarks.
            If ``False``: no meta-data is written.

        **add_ps**
            None, # str, to append generated PostScript script
        **print_ps**
            False,
        **bookmarks**
            True, # True -> use filename, list(str) -> specify per file
        **title**
            'Binder', # title of output PDF
        **author**
            'pdfcombine', # author of output PDF
        **verbose**
            False, # verbose
    '''

    temp_dir = None

    if type(files) == str:
        files = [files]

    # Basic checking

    if not shutil.which('gs'):
        raise IOError('"gs" not found')

    if openright and openleft:
        raise IOError('"openright" and "openleft" are exclusive options')

    for file in files:
        if not os.path.isfile(file):
            raise IOError('"{0:s}" does not exist'.format(file))

    for file in files:
        if os.path.abspath(file) == os.path.abspath(output):
            raise IOError('"{0:s}" is also an input-file, choose a different output'.format(output))

    # Read number of pages

    if openleft or openright or bookmarks:
        n_pages = NumberOfPages(files, verbose)
        is_even = [False if n % 2 != 0 else True for n in n_pages]

    if openleft:
        start_page = [2] + [i if e else i + 1 for i, e in zip(n_pages, is_even)][:-1]
    elif openright:
        start_page = [1] + [i if e else i + 1 for i, e in zip(n_pages, is_even)][:-1]
    else:
        start_page = [1] + [i for i in n_pages]

    start_page = list(accumulate(start_page))

    # Store PostScript commands to set metadata in a temporary file

    if ps != False:

        temp_dir = tempfile.mkdtemp()
        temp_ps = os.path.join(temp_dir, 'pdfcombine.ps')

        if ps == True or ps is None:
            ps = DefaultPostScript(
              files = files,
              start_page = start_page,
              title = title,
              author = author,
              bookmarks = bookmarks)
        elif type(ps) != str:
            raise IOError('Unknown type "ps"')

        if add_ps:
            ps += '\n' + add_ps

        if verbose:
            print('\n---- created "{0:s}" ----\n'.format(temp_ps))
            print(ps)

        open(temp_ps, 'w').write(ps)

    # Construct and run GhostScript command to combine PDFs

    if verbose:
        print('\n---- combining files ----\n')

    cmd = 'gs -sDEVICE=pdfwrite -dBATCH -dNOPAUSE -q -sPAPERSIZE=a4 -o "{0:s}"'.format(output)

    if openleft:
        cmd += ' -c showpage'

    for i, file in enumerate(files):

        if i > 0:
            if (openleft or openright) and not is_even[i-1]:
                cmd += ' -c showpage'

        cmd += ' -f "{0:s}"'.format(file)

    if type(ps) == str:
        cmd += ' ' + temp_ps

    Run(cmd, verbose)

    # Clean-up remove temporary file and directory

    if temp_dir is None:
        return

    if verbose:
        print('\n---- cleaning up ----\n')
        print('rm -r {0:s}'.format(temp_dir))

    shutil.rmtree(temp_dir)
