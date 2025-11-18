# Documentation: archives.html
**Path:** `website/theme/templates/archives.html`
**Type:** .html
**Size:** 867 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/archives.html`
- **File Name:** `archives.html`
- **Extension:** `.html`
- **Size:** 867 bytes
- **Last Modified:** 2025-11-18T22:10:25.700523

## Original Source
```html
{% extends "base.html" %}
{% block title %}Archives{% endblock %}
{% block headerimg %}{{ DEFAUT_HEADER_BG }}{% endblock %}

{% block content %}
<div class="container list">
    <article>
        <h1 style="margin-bottom: 30px;">Archives and tags</h1>

        <div class="meta" style="margin-bottom: 30px;">
            {% for tag, articles in tags %}
                <a href="{{ SITEURL }}/{{ tag.url }}" class="tag">{{ tag }} ({{ articles | length }})</a>
            {% endfor %}
        </div>

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
This is a web asset file (`archives.html`).

Content length: 867 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 867
- Words: 90
- Lines: 29


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/archives.html`

## Performance and Security Notes
- File size: 867 bytes
- Consider security implications when using or modifying this file
