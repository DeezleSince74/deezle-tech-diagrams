# Security

## Reporting a problem

Please report security problems privately, through GitHub's private vulnerability
reporting: open the repository's **Security** tab and choose **Report a vulnerability**.
If that isn't available, open an
[issue](https://github.com/DeezleSince74/deezle-tech-diagrams/issues) that says you
have a security report, without the details, and you'll be contacted.

## What the plugin does

The plugin ships no code and makes no network requests. Its skills tell Claude how to draw
whiteboards and how to convert icon zips you downloaded yourself. During an icon import,
Claude unzips your file into a new, empty temporary folder, treats its contents as
untrusted data, never runs anything from it, and writes only to
`~/.deezle-tech-diagrams/icons`.

## Supported versions

Only the latest version gets fixes.
