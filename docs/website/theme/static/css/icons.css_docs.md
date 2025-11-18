# Documentation: icons.css
**Path:** `website/theme/static/css/icons.css`
**Type:** .css
**Size:** 1888 characters

---

## File Metadata
- **Full Path:** `website/theme/static/css/icons.css`
- **File Name:** `icons.css`
- **Extension:** `.css`
- **Size:** 1888 bytes
- **Last Modified:** 2025-11-18T22:10:25.697523

## Original Source
```css
/* Copied from https://github.com/porterjamesj/crowsfoot */

@font-face {
  font-family: 'icons';
  src: url('../font/icons.eot?79801659');
  src: url('../font/icons.eot?79801659#iefix') format('embedded-opentype'),
       url('../font/icons.woff?79801659') format('woff'),
       url('../font/icons.ttf?79801659') format('truetype'),
       url('../font/icons.svg?79801659#icons') format('svg');
  font-weight: normal;
  font-style: normal;
}
/* Chrome hack: SVG is rendered more smooth in Windozze. 100% magic, uncomment if you need it. */
/* Note, that will break hinting! In other OS-es font will be not as sharp as it could be */
/*
@media screen and (-webkit-min-device-pixel-ratio:0) {
  @font-face {
    font-family: 'icons';
    src: url('../font/icons.svg?79801659#icons') format('svg');
  }
}
*/

 [class^="icon-"]:before, [class*=" icon-"]:before {
  font-family: "icons";
  font-style: normal;
  font-weight: normal;
  speak: none;

  display: inline-block;
  text-decoration: inherit;
  width: 1em;
  margin-right: .2em;
  text-align: center;
  /* opacity: .8; */

  /* For safety - reset parent styles, that can break glyph codes*/
  font-variant: normal;
  text-transform: none;

  /* fix buttons height, for twitter bootstrap */
  line-height: 1em;

  /* Animation center compensation - margins should be symmetric */
  /* remove if not needed */
  margin-left: .2em;

  /* you can be more comfortable with increased icons size */
  /* font-size: 120%; */

  /* Uncomment for 3D effect */
  /* text-shadow: 1px 1px 1px rgba(127, 127, 127, 0.3); */
}

.icon-stackoverflow:before { content: '\e032'; } /* '' */
.icon-twitter:before { content: '\e801'; } /* '' */
.icon-facebook:before { content: '\e802'; } /* '' */
.icon-rss:before { content: '\e800'; } /* '' */
.icon-mail-alt:before { content: '\f0e0'; } /* '' */
.icon-github:before { content: '\f113'; } /* '' */
```

## High-Level Overview
This is a web asset file (`icons.css`).

Content length: 1888 characters


## Detailed Analysis
**Content Metrics:**
- Characters: 1888
- Words: 229
- Lines: 60


## Usage and Integration
This file is part of the PythonDataScienceHandbook repository.
Located at: `website/theme/static/css/icons.css`

## Performance and Security Notes
- File size: 1888 bytes
- Consider security implications when using or modifying this file
