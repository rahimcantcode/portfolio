# Rahim Latreche Portfolio

Static portfolio for AI engineering, machine learning, and data science opportunities.
Open `index.html` or serve the repository with `python3 -m http.server 8000`.
No JavaScript build step or Node dependencies are required.

## Resume maintenance

The downloadable PDF and preview image are built together to prevent content drift:

```sh
python3 -m pip install -r requirements-resume.txt
python3 scripts/build_resume.py
```

The generator contains the editable resume copy and produces:

- `files/Rahim_Latreche_Resume.pdf` (one page, selectable text)
- `images/resume-preview.png` (rendered directly from that PDF)

When experience changes, update both `index.html` and `scripts/build_resume.py`,
regenerate the assets, inspect the preview, and check dates/titles across both.
The generator rejects a resume longer than one page.

## Content verification

See [content review](docs/content-review.md) for evidence and editorial decisions
behind the November 2026 refresh. Avoid adding outcome metrics without supporting
records. Employer work is described without publishing employer source code.

## Checks

This repository has no existing automated test suite or CI workflow.
Before publishing, run `git diff --check`, rebuild the resume, check local links
and anchor targets, and inspect desktop/mobile layouts. Check carousel buttons,
resume fullscreen/open/download actions, reduced motion, and content visibility
with JavaScript disabled.
