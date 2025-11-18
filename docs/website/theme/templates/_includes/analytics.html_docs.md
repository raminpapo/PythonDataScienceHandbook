# Documentation: analytics.html
**Path:** `website/theme/templates/_includes/analytics.html`
**Type:** .html
**Size:** 1482 characters

---

## File Metadata
- **Full Path:** `website/theme/templates/_includes/analytics.html`
- **File Name:** `analytics.html`
- **Extension:** `.html`
- **Size:** 1482 bytes
- **Last Modified:** 2025-11-18T22:10:25.699523

## Original Source
```html
{% if GOOGLE_UNIVERSAL_ANALYTICS %}
    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', '{{GOOGLE_UNIVERSAL_ANALYTICS}}', '{{GOOGLE_UNIVERSAL_ANALYTICS_COOKIEDOMAIN|default("auto")}}');
    ga('send', 'pageview');
    </script>
{% elif GOOGLE_ANALYTICS %}
    <script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', '{{GOOGLE_ANALYTICS}}']);
    _gaq.push(['_trackPageview']);
    (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();

    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', '{{GOOGLE_ANALYTICS}}');
    ga('send', 'pageview');
</script>
{% endif %}

```

## High-Level Overview
This is a web asset file (`analytics.html`).

Content length: 1482 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1482
- Words: 74
- Lines: 31


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/templates/_includes/analytics.html`

## Performance and Security Notes
- File size: 1482 bytes
- Consider security implications when using or modifying this file
