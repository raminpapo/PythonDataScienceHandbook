# Documentation: booksection.html
**Path:** `website/theme/templates/booksection.html`
**Type:** .html
**Size:** 1419 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/booksection.html`
- **File Name:** `booksection.html`
- **Extension:** `.html`
- **Size:** 1419 bytes
- **Last Modified:** 2025-11-18T22:10:25.701523

## Original Source
```html
{% extends "base.html" %}
{% block title %}{{ page.title }}{% endblock %}
{% block headerimg %}{% if page.headerimg %}{{ page.headerimg }}{% else %}{{ DEFAULT_HEADER_BG }}{% endif %}{% endblock %}

{% block content %}

<div class="container bookinfo">
<p>
<img align="left" style="padding-right:10px;" src="/PythonDataScienceHandbook/figures/PDSH-cover-small.png">
<em>This is an excerpt from the <a href="http://shop.oreilly.com/product/0636920034919.do">Python Data Science Handbook</a> by Jake VanderPlas; Jupyter notebooks are available <a href="https://github.com/jakevdp/PythonDataScienceHandbook">on GitHub</a>.</em>
</p>
<p>
<em>The text is released under the <a href="https://creativecommons.org/licenses/by-nc-nd/3.0/us/legalcode">CC-BY-NC-ND license</a>, and code is released under the <a href="https://opensource.org/licenses/MIT">MIT license</a>. If you find this content useful, please consider supporting the work by <a href="http://shop.oreilly.com/product/0636920034919.do">buying the book</a>!</em>
</p>
</div>


<div class="container post">

    <article>
        <header>
            <h1>{{ page.title }}</h1>
            {% if page.date %}
                <time datetime="page.date.isoformat()" pubdate>{{ page.locale_date }}</time>
            {% endif %}
        </header>

        <div class="article_content">
            {{ page.content }}
        </div>

    </article>
</div>
{% endblock %}

```

## High-Level Overview
This is a web asset file (`booksection.html`).

Content length: 1419 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1419
- Words: 132
- Lines: 35


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/booksection.html`

## Performance and Security Notes
- File size: 1419 bytes
- Consider security implications when using or modifying this file
