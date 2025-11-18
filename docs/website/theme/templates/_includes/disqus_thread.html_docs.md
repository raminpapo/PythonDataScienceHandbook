# Documentation: disqus_thread.html
**Path:** `website/theme/templates/_includes/disqus_thread.html`
**Type:** .html
**Size:** 907 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/_includes/disqus_thread.html`
- **File Name:** `disqus_thread.html`
- **Extension:** `.html`
- **Size:** 907 bytes
- **Last Modified:** 2025-11-18T22:10:25.699523

## Original Source
```html
{% if DISQUS_SITENAME and SITEURL and article.status != "draft" %}
  <section>
    <h1>Comments</h1>
    <div id="disqus_thread" aria-live="polite"><noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript></div>
    <script type="text/javascript">
      var disqus_shortname = '{{ DISQUS_SITENAME }}';
      var disqus_identifier = '/{{ article.url }}';
      var disqus_url = '{{ SITEURL }}/{{ article.url }}';
      var disqus_title = '{{ article.title | replace("'", "\\'")}}';
      (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = "//" + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
      })();
    </script>
  </section>
{% endif %}

```

## High-Level Overview
This is a web asset file (`disqus_thread.html`).

Content length: 907 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 907
- Words: 83
- Lines: 18


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/_includes/disqus_thread.html`

## Performance and Security Notes
- File size: 907 bytes
- Consider security implications when using or modifying this file
