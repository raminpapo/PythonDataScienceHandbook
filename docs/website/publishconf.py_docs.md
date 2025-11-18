# Documentation: publishconf.py
**Path:** `website/publishconf.py`
**Type:** .py
**Size:** 613 characters

---

## File Metadata
- **Full Path:** `website/publishconf.py`
- **File Name:** `publishconf.py`
- **Extension:** `.py`
- **Size:** 613 bytes
- **Last Modified:** 2025-11-18T22:10:25.695523

## Original Source
```py
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://jakevdp.github.io/PythonDataScienceHandbook'
RELATIVE_URLS = False

SHOW_FEED = False
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
FEED_USE_SUMMARY = True  # from the feed_summary plugin

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "pythonicperambulations"
GOOGLE_ANALYTICS = "UA-34061646-1"

```

## High-Level Overview
This Python file (`publishconf.py`) contains Python source code.

**Imports:**
- `from __future__`
- `import os`
- `import sys`
- `from pelicanconf`


## Detailed Analysis
**Content Metrics:**
- Characters: 613
- Words: 73
- Lines: 25


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/publishconf.py`

## Performance and Security Notes
- File size: 613 bytes
- Consider security implications when using or modifying this file
