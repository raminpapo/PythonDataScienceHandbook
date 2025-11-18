# Documentation: add_book_info.py
**Path:** `tools/add_book_info.py`
**Type:** .py
**Size:** 1486 characters

---

## File Metadata
- **Full Path:** `tools/add_book_info.py`
- **File Name:** `add_book_info.py`
- **Extension:** `.py`
- **Size:** 1486 bytes
- **Last Modified:** 2025-11-18T22:10:25.693523

## Original Source
```py
import os

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import iter_notebooks, NOTEBOOK_DIR


BOOK_COMMENT = "<!--BOOK_INFORMATION-->"


BOOK_INFO = BOOK_COMMENT + """
<img align="left" style="padding-right:10px;" src="figures/PDSH-cover-small.png">

*This notebook contains an excerpt from the [Python Data Science Handbook](http://shop.oreilly.com/product/0636920034919.do) by Jake VanderPlas; the content is available [on GitHub](https://github.com/jakevdp/PythonDataScienceHandbook).*

*The text is released under the [CC-BY-NC-ND license](https://creativecommons.org/licenses/by-nc-nd/3.0/us/legalcode), and code is released under the [MIT license](https://opensource.org/licenses/MIT). If you find this content useful, please consider supporting the work by [buying the book](http://shop.oreilly.com/product/0636920034919.do)!*"""


def add_book_info():
    for nb_name in iter_notebooks():
        nb_file = os.path.join(NOTEBOOK_DIR, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        is_comment = lambda cell: cell.source.startswith(BOOK_COMMENT)

        if is_comment(nb.cells[0]):
            print('- amending comment for {0}'.format(nb_name))
            nb.cells[0].source = BOOK_INFO
        else:
            print('- inserting comment for {0}'.format(nb_name))
            nb.cells.insert(0, new_markdown_cell(BOOK_INFO))
        nbformat.write(nb, nb_file)


if __name__ == '__main__':
    add_book_info()

```

## High-Level Overview
This Python file (`add_book_info.py`) contains Python source code.

**Imports:**
- `import os`
- `import nbformat`
- `from nbformat.v4.nbbase`
- `from generate_contents`

**Functions Defined:** add_book_info


## Detailed Analysis
**Content Metrics:**
- Characters: 1486
- Words: 120
- Lines: 38


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `tools/add_book_info.py`

## Performance and Security Notes
- File size: 1486 bytes
- Consider security implications when using or modifying this file
