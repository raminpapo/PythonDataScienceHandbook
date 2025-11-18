# Documentation: tag.html
**Path:** `website/theme/templates/tag.html`
**Type:** .html
**Size:** 617 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/tag.html`
- **File Name:** `tag.html`
- **Extension:** `.html`
- **Size:** 617 bytes
- **Last Modified:** 2025-11-18T22:10:25.702523

## Original Source
```html
{% extends "base.html" %}
{% block title %}Archives{% endblock %}
{% block headerimg %}{{ DEFAUT_HEADER_BG }}{% endblock %}

{% block content %}
<div class="container list">
    <article>
        <h1 style="margin-bottom: 30px;">Tag: {{ tag }}</h1>

        <ul class="double-list">
        {% for article in articles %}
            <li>
                <a href='/{{ article.url }}'>
                    <h2>{{ article.title }}</h2>
                    <span>{{ article.date.strftime('%d.%m.%Y') }}</span>
                </a>
            </li>
        {% endfor %}
        </ul>
    </article>
</div>
{% endblock %}

```

## High-Level Overview
This is a web asset file (`tag.html`).

Content length: 617 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 617
- Words: 62
- Lines: 23


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/tag.html`

## Performance and Security Notes
- File size: 617 bytes
- Consider security implications when using or modifying this file
