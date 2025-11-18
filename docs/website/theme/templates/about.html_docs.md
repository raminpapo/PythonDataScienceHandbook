# Documentation: about.html
**Path:** `website/theme/templates/about.html`
**Type:** .html
**Size:** 1507 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/about.html`
- **File Name:** `about.html`
- **Extension:** `.html`
- **Size:** 1507 bytes
- **Last Modified:** 2025-11-18T22:10:25.700523

## Original Source
```html
{% extends "base.html" %}
{% block title %}{{ page.title }}{% endblock %}
{% block headerimg %}{% if page.headerimg %}{{ page.headerimg }}{% else %}{{ DEFAULT_HEADER_BG }}{% endif %}{% endblock %}

{% block content %}

<div class="container post">
    <article>
        <header class="about">
          <h1>{{ page.title }}</h1>
          {% if page.date %}
          <time datetime="page.date.isoformat()" pubdate>{{ page.locale_date }}</time>
          {% endif %}
	  <div class="social-links">
	    <ul>
	      {% if AUTHOR_WEBSITE %}
	      <li><a href="{{ AUTHOR_WEBSITE }}" rel="me">website</a></li>
              {% endif %}
	      {% if AUTHOR_BLOG %}
	      <li><a href="{{ AUTHOR_BLOG }}" rel="me">blog</a></li>
              {% endif %}
	      {% if AUTHOR_CV %}
	      <li><a href="{{ AUTHOR_CV }}" rel="me">CV</a></li>
	      {% endif %}
	      {% if TWITTER_USERNAME %}
	      <li><a class="nodec icon-twitter" href="http://twitter.com/{{ TWITTER_USERNAME }}" rel="me"></a></li>
              {% endif %}
              {% if GITHUB_USERNAME %}
	      <li><a class="nodec icon-github" href="http://github.com/{{ GITHUB_USERNAME }}" rel="me"></a></li>
              {% endif %}
              {% if STACKOVERFLOW_ADDRESS %}
	      <li><a class="nodec icon-stackoverflow" href="{{ STACKOVERFLOW_ADDRESS }}" rel="me"></a></li>
	      {% endif %}
	    </ul>
        </header>

        <div class="article_content">
            {{ page.content }}
        </div>

    </article>
</div>
{% endblock %}

```

## High-Level Overview
This is a web asset file (`about.html`).

Content length: 1507 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1507
- Words: 148
- Lines: 44


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/about.html`

## Performance and Security Notes
- File size: 1507 bytes
- Consider security implications when using or modifying this file
