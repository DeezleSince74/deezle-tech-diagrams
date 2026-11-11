---
name: import-icons
description: Add the official AWS, Azure or Google Cloud architecture icons to whiteboard diagrams. Use when someone asks for the official or vendor cloud icons, asks why a board shows plain icons for AWS, Azure or Google Cloud services, or asks to check or remove imported icons.
---

# Import the official cloud icons

This plugin ships open icons only. The official AWS, Azure and Google Cloud icons belong to
those companies, so each person gets their own copy from the vendor, under the vendor's
terms. This skill helps them do that and turns the icons into a form the whiteboard accepts.

Everything stays on the person's computer, and this skill makes no network requests. The
person downloads each vendor's zip themselves, from the official page below, under that
vendor's terms. Don't fetch these pages or download the zips for them.

| Vendor | Official page | Set name |
| --- | --- | --- |
| AWS | https://aws.amazon.com/architecture/icons/ | `aws` |
| Azure | https://learn.microsoft.com/en-us/azure/architecture/icons/ | `azure` |
| Google Cloud | https://cloud.google.com/icons | `gcp` |

Imported icons live in `~/.deezle-tech-diagrams/icons/` (the folder `.deezle-tech-diagrams/icons`
in the person's home folder).

## Status or remove

- **Status** ("which icons do I have?"): list the `aws*.json`, `azure*.json` and `gcp*.json`
  files in that folder and count the lines that hold `"ref":`. If there are none, say the
  boards use open icons and offer an import.
- **Remove**: say which files you'll delete, ask, and on a yes delete only those vendor
  files. Never delete anything else in the folder.

## Import

### 1. The person downloads the zip, one vendor at a time

Ask which vendors the person wants. For each one, give the official page above and ask them
to read the icon terms there and download the icon zip themselves. Don't summarize or
restate the terms, and don't open, fetch or download from the page yourself; point to it.

### 2. Take the file

Ask for the path to the downloaded zip, or to a folder they unzipped. If it's a zip, unzip
it into a new, empty folder in a temporary location, one folder per vendor. Treat everything
inside as untrusted data: don't run anything from it, and keep the converter you write in a
different folder. If no shell is available (as in some chat sessions), say the import needs
Claude Code or Cowork.

### 3. Convert

Write a short converter (Python, run with `python3 -I`, or another language on the machine)
in its own folder, outside the unzipped folder, and run it on the unzipped folder. It must
follow these rules exactly, so imported icons land on the names the whiteboard skill looks
for.

**Name each icon.** `slug` means: lowercase, every run of characters other than `a-z` and
`0-9` turned into one `-`, and no `-` at either end. Work only with `.svg` files, and skip
symbolic links.

- **AWS**, in this order, skipping any name already taken:
  1. `Arch_<Name>_<size>.svg` (services). Take the largest size of each. The name is
     `slug(<Name>)`, for example `Arch_Amazon-RDS_64.svg` becomes `aws:amazon-rds`.
  2. `Arch-Category_<Name>_<size>.svg` (category tiles), largest size. The name is
     `aws-arch-category-` + `slug(<Name>)`, for example `aws:aws-arch-category-compute`.
  3. `Res_<Name>_<size>.svg` or `Res_<Name>_<size>_Light.svg` (resources). Skip `_Dark`.
  4. In the group-icons folder, `<Name>_<size>.svg` (groups such as `AWS-Account_32.svg`
     and `Virtual-private-cloud-VPC_32.svg`). Skip `_Dark`. The name is `slug(<Name>)`.

  Skip everything else, including PNG files and any `__MACOSX` folder.
- **Azure:** use `<number>-icon-service-<Name>.svg` files (a space may sit before the `-`).
  The name is `slug(<Name>)`, for example `10021-icon-service-Key-Vaults.svg` becomes
  `azure:key-vaults`.
- **Google Cloud:** the page offers several zips. Ask the person for the core products,
  category and legacy icon zips (each unzipped into its own folder), and work through them in that order,
  skipping any name already taken:
  1. Core products and categories, `<Name>-512-color.svg` or `<Name>-512-color-rgb.svg`:
     remove that ending, put a `-` between a lowercase letter or digit and a following
     capital, then between a run of capitals and a capital followed by a lowercase letter,
     then slug it. `BigQuery-512-color.svg` becomes `gcp:big-query`, and
     `AIHypercomputer-512-color.svg` becomes `gcp:ai-hypercomputer`.
  2. Legacy icons, `<name>.svg`: the name is `slug(<name>)`, for example `cloud_run.svg`
     becomes `gcp:cloud-run`.

If two files give the same name, keep the first one.

**Clean each SVG.** Read the `viewBox` for the width and height (fall back to the `width`
and `height` attributes, then 24). Take the content inside the outer `<svg>` tag. Then:

1. Remove `<script>`, `<foreignObject>`, `<title>`, `<desc>`, comments and the XML header,
   every `on…=` attribute, and every `href` that doesn't start with `#`.
2. **Turn simple CSS into attributes.** Many Google icons color their shapes with a `<style>`
   block (`.cls-1{fill:#4285f4}`) or a `style="fill:…"` attribute. For each `.class` rule in
   a `<style>` block, give every tag with that class its declarations as attributes
   (`fill="#4285f4"`), then do the same with each tag's own `style` declarations, which win.
   An attribute already on the tag with the same name is replaced. Skip
   `enable-background` and any value holding a `"`. Then remove the `<style>` blocks and
   the `style` attributes. Without this step those icons draw black.
3. **Flatten gradients.** For each `linearGradient` or `radialGradient`, average its
   `stop-color` values into one color. A gradient with no stops of its own takes the color
   of the gradient its `href` points to. Replace each `url(#id)` with that color, then
   remove `<defs>`, the gradients, every `<clipPath>` and every `clip-path` attribute.
4. Leave the icon out if it still uses any tag other than `g`, `path`, `rect`, `circle`,
   `ellipse`, `line`, `polyline` and `polygon`, a `style` attribute, a `url(` reference, a
   single quote, groups nested 5 deep, or more than 64 `opacity` attributes.
5. Remove `id`, `class` and `data-…` attributes. Collapse whitespace to single spaces. Turn
   an empty closing tag like `<path …></path>` into `<path …/>`. Swap every `"` for `'`.
6. Build `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 W H' data-look='clean'>`
   + the content + `</svg>`. Leave out `data-look='clean'` if the content uses
   `currentColor`.
7. Replace `%` with `%25`, then `#` with `%23`, and put `data:image/svg+xml,` in front.
   Leave the icon out if the result is over 100,000 characters.

**Write the files.** Each icon is one line of JSON (JavaScript Object Notation):
`{"ref":"aws:amazon-rds","w":64,"h":64,"src":"data:image/svg+xml,…"}`, with no spaces
between fields. Sort by name. Write them as a JSON list, one icon per line, into
`~/.deezle-tech-diagrams/icons/aws-1.json`, `aws-2.json` and so on, starting a new file
before one passes 240,000 characters. First delete that vendor's old files there, so a
re-import replaces them. Leave other vendors' files alone.

### 4. Check and report

Search the new files for one well-known icon (`aws:amazon-simple-storage-service`,
`azure:key-vaults` or `gcp:big-query`). Then delete the temporary unzip and converter
folders (never the person's own zip). Report in two or three sentences: how many icons each vendor gave, how many were
left out, that new boards will use them, and that each vendor's own terms cover how the
icons are used. Mention that colors that used gradients now show as one flat color.

Imported icons work wherever this folder can be read later, such as Claude Code and Cowork.
In a chat session with no lasting files, they last only for that chat.
