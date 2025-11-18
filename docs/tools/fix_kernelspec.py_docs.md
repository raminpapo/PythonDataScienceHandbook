# Documentation: fix_kernelspec.py
**Path:** `tools/fix_kernelspec.py`
**Type:** .py
**Size:** 468 characters

---

## File Metadata
- **Full Path:** `tools/fix_kernelspec.py`
- **File Name:** `fix_kernelspec.py`
- **Extension:** `.py`
- **Size:** 468 bytes
- **Last Modified:** 2025-11-18T22:10:25.693523

## Original Source
```py
import os

import nbformat

from generate_contents import iter_notebooks, NOTEBOOK_DIR

def fix_kernelspec():
    for nb_name in iter_notebooks():
        nb_file = os.path.join(NOTEBOOK_DIR, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        print("- Updating kernelspec for {0}".format(nb_name))
        nb['metadata']['kernelspec']['display_name'] = 'Python 3'

        nbformat.write(nb, nb_file)


if __name__ == '__main__':
    fix_kernelspec()

```

## High-Level Overview
This Python file (`fix_kernelspec.py`) contains Python source code.

**Imports:**
- `import os`
- `import nbformat`
- `from generate_contents`

**Functions Defined:** fix_kernelspec


## Detailed Analysis
**Content Metrics:**
- Characters: 468
- Words: 39
- Lines: 20


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `tools/fix_kernelspec.py`

## Performance and Security Notes
- File size: 468 bytes
- Consider security implications when using or modifying this file
