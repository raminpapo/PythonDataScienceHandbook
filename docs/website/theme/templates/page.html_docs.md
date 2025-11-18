# Documentation: page.html
**Path:** `website/theme/templates/page.html`
**Type:** .html
**Size:** 606 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/page.html`
- **File Name:** `page.html`
- **Extension:** `.html`
- **Size:** 606 bytes
- **Last Modified:** 2025-11-18T22:10:25.702523

## Original Source
```html
{% extends "base.html" %}
{% block title %}{{ page.title }}{% endblock %}
{% block headerimg %}{% if page.headerimg %}{{ page.headerimg }}{% else %}{{ DEFAULT_HEADER_BG }}{% endif %}{% endblock %}

{% block content %}
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
This is a web asset file (`page.html`).

Content length: 606 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 606
- Words: 65
- Lines: 23


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/page.html`

## Performance and Security Notes
- File size: 606 bytes
- Consider security implications when using or modifying this file
