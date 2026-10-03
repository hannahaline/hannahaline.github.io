# hannahaline.github.io

Hannah Henry's academic website, <https://hannahaline.github.io>, built with the
[al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Pushing to `main` runs
`.github/workflows/deploy.yml`, which builds the site and publishes it to the `gh-pages` branch.

## Where things live

| To change | Edit |
|---|---|
| Name, description, footer, feature switches | `_config.yml` |
| Social icons and CV link on the home page | `_data/socials.yml` |
| Home page bio and education | `_pages/about.md` |
| News on the home page | one file per item in `_news/` |
| Research cards and their pages | one file per project in `_projects/` (`img:` is the card photo) |
| Published papers | `_bibliography/papers.bib` (BibTeX) |
| Papers in review or preparation | bottom of `_pages/publications.md` |
| Talks | `_pages/talks.md` |
| Teaching & outreach, CMWG | `_pages/teaching-outreach.md`, `_pages/cmwg.md` |
| CV | replace `assets/pdf/Henry_CV.pdf` (keep the name) |
| Headshot | `assets/img/prof_pic.jpg` (square) |
| Accent colour and small style tweaks | bottom of `assets/css/main.scss` |

`_includes/news.liquid` and `assets/css/main.scss` are local copies of al-folio theme files,
changed to show news by month and to use the teal accent. `_drafts/` holds the old Wix blog posts,
which are not published.

## Preview locally (Windows)

```
bundle install
bundle exec jekyll serve --config _config.yml,_config_local.yml
```

Then open <http://localhost:4000>. `_config_local.yml` turns off image resizing, because Windows
has its own unrelated `convert` program; GitHub's build uses the real ImageMagick.
