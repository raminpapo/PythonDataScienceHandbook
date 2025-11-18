# Documentation: README.md
**Path:** `website/README.md`
**Type:** .md
**Size:** 1182 characters

---

## File Metadata
- **Full Path:** `website/README.md`
- **File Name:** `README.md`
- **Extension:** `.md`
- **Size:** 1182 bytes
- **Last Modified:** 2025-11-18T22:10:25.694523

## Original Source
```md
2# Tools for creating http://jakevdp.github.io/PythonDataScienceHandbook/

The website is generated using the [Pelican](http://docs.getpelican.com/) static site generator.
The themes here are adapted from those used for my blog: https://github.com/jakevdp/jakevdp.github.io-source

## Building the Website

Clone the repository & make sure submodules are included

```
$ git clone https://github.com/jakevdp/PythonDataScienceHandbook.git
$ git checkout origin/website
$ git submodule update --init --recursive
$ cd website
```

Install the required packages:

```
$ conda create -n pelican-blog python=3.5 jupyter notebook
$ source activate pelican-blog
$ pip install pelican Markdown ghp-import
$ mkdir plugins
$ git submodule add git://github.com/danielfrg/pelican-ipynb.git plugins/ipynb
$ git submodule add https://github.com/getpelican/pelican-plugins.git plugins/pelican-plugins
```

Copy the notebook content to the right location (this script also modifies some links for the HTML):
```
$ python copy_notebooks.py
```

Build the html and serve locally:

```
$ make html
$ make serve
$ open http://localhost:8000
```

Deploy to github pages

```
$ make publish-to-github
```

```

## High-Level Overview
This is a Markdown documentation file (`README.md`).

**Document Structure:**
  - Building the Website


## Detailed Analysis
**Content Metrics:**
- Characters: 1182
- Words: 146
- Lines: 46


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/README.md`

## Performance and Security Notes
- File size: 1182 bytes
- Consider security implications when using or modifying this file
