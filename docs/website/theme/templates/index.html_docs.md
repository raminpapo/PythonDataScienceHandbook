# Documentation: index.html
**Path:** `website/theme/templates/index.html`
**Type:** .html
**Size:** 1367 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/index.html`
- **File Name:** `index.html`
- **Extension:** `.html`
- **Size:** 1367 bytes
- **Last Modified:** 2025-11-18T22:10:25.701523

## Original Source
```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block headerimg %}{{ DEFAULT_HEADER_BG }}{% endblock %}

{% block content %}
<div class="container index">

  {% for article in articles_page.object_list %}
  <article>
    <header>
      <h2><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></h2>
      <time datetime="" title="{{ article.date.isoformat() }}" pubdate>{{ article.locale_date }}</time>
    </header>

    <div class="article_content">
      {{ article.summary }}
    </div>

    <div class="meta">
      <div>
        <a href="{{ SITEURL }}/{{ article.url }}" class="read_more">Read more &#8594;</a>
      </div>

      <div>
          {% for tag in article.tags %}
            <a href="{{ SITEURL }}/{{ tag.url }}" class="tag">{{ tag }}</a>
          {% endfor %}
      </div>

    </div>

  </article>
  <div class="separator"></div>
  {% endfor %}

  <nav class="pagination row">
    <div class="col-xs-6 left">
      {% if articles_page.has_next() %}
        <a class="prev" href="{{ SITEURL }}/{{ articles_next_page.url }}">&#8592; Past</a>
      {% endif %}
    </div>
    <div class="col-xs-6 right">
      {% if articles_page.has_previous() %}
        <a class="next" href="{{ SITEURL }}/{{ articles_previous_page.url }}">Future &#8594;</a>
      {% endif %}
    </div>
  </nav>

  </div>

</div>

{% endblock %}

```

## High-Level Overview
This is a web asset file (`index.html`).

Content length: 1367 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1367
- Words: 143
- Lines: 54


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/index.html`

## Performance and Security Notes
- File size: 1367 bytes
- Consider security implications when using or modifying this file
