
import os
import subprocess
import shutil
import tempfile
from itertools import accumulate

__version__ = '1.1.2'


def run(cmd, verbose=False):
    r'''
Run command, optionally verbose command and output, and return output.
    '''

    out = subprocess.check_output(cmd, shell=True).decode('utf-8')

    if verbose:
        print(cmd)
        print(out)

    return out


def number_of_pages(files, verbose=False):
    r'''
Read the number of pages of a (list of) PDF(s), using GhostScript.
The output is a (list of) integers.
    '''

    return_int = False

    if type(files) == str:
        files = [files]
        return_int = True

    if verbose:
        print('\n---- reading number of pages per file ----\n')

    n_pages = []

    for file in files:
        cmd = 'gs -q -dNODISPLAY -c "({0:s}) (r) file runpdfbegin pdfpagecount = quit"'.format(file)
        out = run(cmd, verbose)
        n_pages += [int(out)]

    if return_int:
        return n_pages[0]

    return n_pages


def generate_postscript(
        title=None,
        author=None,
        bookmarks=None,
        pages=None,
):
    r'''
Generate PostScript script.

:options:

    **title** (``<str>``)
        PDF title.

    **author** (``<str>``)
        PDF author.

    **bookmarks** (``<list<str>>``)
        List of bookmarks. Length must mage ``pages``.

    **pages** (``<list<int>>``)
        List of page-numbers. Length must mage ``bookmarks``.
    '''

    if type(bookmarks) == str:
        bookmarks = [bookmarks]

    if type(pages) == int:
        pages = [pages]

    out = []

    if title:
        out += ['/Title ({0:s})'.format(title)]

    if author:
        out += ['/Author ({0:s})'.format(author)]

    if bookmarks:
        for bookmark, page in zip(bookmarks, pages):
            out += ['/Page {0:d} /Title ({1:s}) /OUT pdfmark'.format(page, bookmark)]

    if len(out) == 0:
        return ''

    return '[ ' + '\n[ '.join(out)


def combine(
        files,
        output,
        openleft=False,
        openright=False,
        meta=True,
        ps=None,
        add_ps=None,
        bookmarks=True,
        title='Binder',
        author='pdfcombine',
        verbose=False,
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
        Make sure each 'document' begins on a left-page.

    **openright** ([``False``] | ``True``)
        Make sure each 'document' begins on a right-page.

    **meta** ([``True``] | ``False``)
        Write meta-data using a PostScript script
        (see below for options: 'ps', 'add_ps', 'bookmarks', 'title', 'author').

    **ps** (``<str>``)
        If specified the automatically generated PostScript script is overwritten with
        the specified script.

    **add_ps** (``<str>``)
        Append generated/specified PostScript script with the specified script.

    **bookmarks** ([``True``] | ``False`` | ``<list<str>>``)
        If ``True`` the filenames are used as bookmarks in the automatically generated
        PostScript script. One can customise the bookmarks by specifying a list with
        one label per file.

    **title** (``<str>``)
        Specify PDF title. Defaults to "Binder".

    **author** (``<str>``)
        Specify PDF author. Defaults to "pdfcombine".

    **verbose** ([``False``] | ``True``)
        Verbose all commands and their output.
    '''

    temp_dir = None

    if type(files) == str:
        files = [files]

    if type(bookmarks) == str:
        bookmarks = [bookmarks]

    if bookmarks == True:
        bookmarks = [file for file in files]

    if not meta:
        bookmarks = False

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

    # Read number of pages and derive basic information

    if openleft or openright or bookmarks:

        n_pages = number_of_pages(files, verbose)

        is_even = [False if n % 2 != 0 else True for n in n_pages]

    if bookmarks:

        if openleft:
            start_page = [2] + [i if e else i + 1 for i, e in zip(n_pages, is_even)][:-1]
        elif openright:
            start_page = [1] + [i if e else i + 1 for i, e in zip(n_pages, is_even)][:-1]
        else:
            start_page = [1] + [i for i in n_pages]

        start_page = list(accumulate(start_page))

    # PostScript script to set metadata -> write to temporary file

    if meta:

        temp_dir = tempfile.mkdtemp()
        temp_ps = os.path.join(temp_dir, 'pdfcombine.ps')

        if type(ps) != str:
            ps = generate_postscript(
                title=title,
                author=author,
                bookmarks=bookmarks,
                pages=start_page)

        if type(add_ps) == str:
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

    if meta:
        cmd += ' ' + temp_ps

    run(cmd, verbose)

    # Clean-up: remove temporary directory (including its contents)

    if temp_dir is None:
        return

    if verbose:
        print('\n---- cleaning up ----\n')
        print('rm -r {0:s}'.format(temp_dir))
        print('')

    shutil.rmtree(temp_dir)
