import os
import shutil
import subprocess
import tempfile
from itertools import accumulate

from ._version import version  # noqa: F401


def run(cmd: str, verbose: bool = False):
    """
    Run command and return output.
    :param verbose: Print command and output.
    """

    if verbose:
        print(cmd)

    out = subprocess.check_output(cmd, shell=True).decode("utf-8")

    if verbose:
        print(out)

    return out


def number_of_pages(files: list[str], verbose: bool = False) -> list[int]:
    """
    Read the number of pages of a (list of) PDF(s), using GhostScript.
    :param verbose: Verbose operation.
    """

    return_int = False

    if type(files) == str:
        files = [files]
        return_int = True

    if verbose:
        print("\n---- reading number of pages per file ----\n")

    n_pages = []

    for f in files:
        cmd = f'gs -q -dNOSAFER -dNODISPLAY -c "({f:s}) (r) file runpdfbegin pdfpagecount = quit"'
        out = run(cmd, verbose)
        n_pages += [int(out)]

    if return_int:
        return n_pages[0]

    return n_pages


def generate_postscript(
    title: str = None,
    author: str = None,
    bookmarks: list[str] = None,
    pages: list[int] = None,
):
    """
    Generate PostScript script.

    :param title: PDF title.
    :param author: PDF author.
    :param bookmarks: List of bookmarks. Length must mage ``pages``.
    :param pages: List of page-numbers. Length must mage ``bookmarks``.
    """

    if type(bookmarks) == str:
        bookmarks = [bookmarks]

    if type(pages) == int:
        pages = [pages]

    out = []

    if title:
        out += [f"/Title ({title:s})"]

    if author:
        out += [f"/Author ({author:s})"]

    if bookmarks:
        for bookmark, page in zip(bookmarks, pages):
            out += [f"/Page {page:d} /Title <FEFF{bookmark.encode(encoding='utf-16-BE').hex().upper()}> /OUT pdfmark"]

    if len(out) == 0:
        return ""

    return "[ " + "\n[ ".join(out)


def combine(
    files: str | list[str],
    output: str,
    openleft: bool = False,
    openright: bool = False,
    meta: bool = True,
    ps: str = None,
    add_ps: str = None,
    bookmarks: bool | list[str] = True,
    title: str = "Binder",
    author: str = "pdfcombine",
    verbose: bool = False,
):
    """
    Combine PDFs

    :param files: List of PDF files to combine.
    :param output: Name of output file (overwritten if exists).
    :param openleft: Start each file on a left-page.
    :param openright: Start each file on a right-page.
    :param meta: Write meta-data using a PostScript script.
    :param ps: Overwrite automatically generated PostScript script.
    :param add_ps: Append generated/specified PostScript script.
    :param bookmarks: If ``True`` the filenames are the bookmarks. Otherwise specify name per file.
    :param title: PDF title.
    :param author: PDF author.
    :param verbose: Verbose all commands and their output.
    """

    temp_dir = None

    if type(files) == str:
        files = [files]

    if type(bookmarks) == str:
        bookmarks = [bookmarks]

    if bookmarks is True:
        bookmarks = [file for file in files]

    if not meta:
        bookmarks = False

    # Basic checking

    if not shutil.which("gs"):
        raise OSError('"gs" not found')

    if openright and openleft:
        raise OSError('"openright" and "openleft" are exclusive options')

    for file in files:
        if not os.path.isfile(file):
            raise OSError(f'"{file:s}" does not exist')

    for file in files:
        if os.path.abspath(file) == os.path.abspath(output):
            raise OSError(f'"{output}" is also an input-file, choose a different output')

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
        temp_ps = os.path.join(temp_dir, "pdfcombine.ps")

        if type(ps) != str:
            ps = generate_postscript(
                title=title, author=author, bookmarks=bookmarks, pages=start_page
            )

        if type(add_ps) == str:
            ps += "\n" + add_ps

        if verbose:
            print(f'\n---- created "{temp_ps:s}" ----\n')
            print(ps)

        open(temp_ps, "w").write(ps)

    # Construct and run GhostScript command to combine PDFs

    if verbose:
        print("\n---- combining files ----\n")

    cmd = f'gs -dNOSAFER -sDEVICE=pdfwrite -dBATCH -dNOPAUSE -q -sPAPERSIZE=a4 -o "{output}"'

    if openleft:
        cmd += " -c showpage"

    for i, file in enumerate(files):

        if i > 0:
            if (openleft or openright) and not is_even[i - 1]:
                cmd += " -c showpage"

        cmd += f' -f "{file:s}"'

    if meta:
        cmd += " " + temp_ps

    run(cmd, verbose)

    # Clean-up: remove temporary directory (including its contents)

    if temp_dir is None:
        return

    if verbose:
        print("\n---- cleaning up ----\n")
        print(f"rm -r {temp_dir:s}")
        print("")

    shutil.rmtree(temp_dir)
