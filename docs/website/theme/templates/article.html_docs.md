# Documentation: article.html
**Path:** `website/theme/templates/article.html`
**Type:** .html
**Size:** 1224 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/article.html`
- **File Name:** `article.html`
- **Extension:** `.html`
- **Size:** 1224 bytes
- **Last Modified:** 2025-11-18T22:10:25.700523

## Original Source
```html
{% extends "base.html" %}
{% block title %}{{ article.title }}{% endblock %}
{% block headerimg %}{% if article.headerimg %}{{ article.headerimg }}{% else %}{{ DEFAULT_HEADER_BG }}{% endif %}{% endblock %}

{% block extra_head %}
{% if 'angular' in article.include %}
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.7/angular.min.js"></script>
{% endif %}
{% if 'jquery' in article.include %}
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
{% endif %}
{% endblock %}

{% block content %}
<div class="container post">
    <article>
        <header>
            <h1>{{ article.title }}</h1>
            <time datetime="article.date.isoformat()" pubdate>{{ article.locale_date }}</time>
        </header>

        <div class="article_content">
            {{ article.content }}
        </div>

        <div class="meta">
            <div>
                {% for tag in article.tags %}
                    <a href="{{ SITEURL }}/{{ tag.url }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </div>
        </div>
    </article>

  {% include '_includes/disqus_thread.html' %}

</div>

<style type="text/css">
{% include 'ipynb.css' %}
</style>

{% endblock %}

```

## High-Level Overview
This is a web asset file (`article.html`).

Content length: 1224 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1224
- Words: 121
- Lines: 44


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/article.html`

## Performance and Security Notes
- File size: 1224 bytes
- Consider security implications when using or modifying this file
