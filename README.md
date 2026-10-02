# hannahaline.github.io

Hannah Henry's academic website, served by GitHub Pages at <https://hannahaline.github.io>.
Built on the [Academic Pages](https://github.com/academicpages/academicpages.github.io) Jekyll template.

## Where things live

| To change | Edit |
|---|---|
| Name, sidebar bio, profile links | `_config.yml` (the `author:` block) |
| Header menu | `_data/navigation.yml` |
| Home page | `_pages/about.md` |
| Research / Past Research | `_pages/research.md`, `_pages/past-research.md` |
| Teaching & Outreach | `_pages/teaching-outreach.md` |
| TWS CMWG | `_pages/cmwg.md` |
| Published papers | one file per paper in `_publications/` |
| Papers in review or preparation | bottom of `_pages/publications.html` |
| CV | replace `files/Henry_CV.pdf` (keep the name) |
| Photos | `images/photos/`; the sidebar photo is `images/profile.jpg` |
| Extra styles | `_sass/layout/_custom.scss` |

`_drafts/` holds the old Wix blog posts. Jekyll does not publish drafts. To publish one, download its
images into `images/`, point the links at them, and move the file to `_posts/`.

## Preview locally

```
bundle install
bundle exec jekyll serve -l -H localhost
```

Then open <http://localhost:4000>. Pushing to `main` rebuilds the live site within a minute or two.
