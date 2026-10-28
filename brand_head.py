"""Shared <head> snippets for the NorthLedger Tools logo (icons, manifest, social image).

Used by gen.py, guides_gen.py (and the staged bill96_gen.py). Single source so every generated page gets the same links.
The privacy page is deliberately excluded by the callers (its output is kept byte-identical)."""
BASE = "https://northledgertools.com/"
OG_IMAGE = BASE + "assets/og-card.png"
OG_ALT = "NorthLedger Tools logo: an open book with a mountain M"

ICON_LINKS = ('<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">'
              '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">'
              '<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">'
              '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png">'
              '<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">'
              '<link rel="icon" type="image/png" sizes="512x512" href="/assets/icon-512.png">'
              '<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">'
              '<link rel="manifest" href="/assets/site.webmanifest">')

SOCIAL_META = (f'<meta property="og:image" content="{OG_IMAGE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
               f'<meta property="og:image:alt" content="{OG_ALT}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG_IMAGE}">')

OLD_ICON = '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'


def head_extra(path):
    """Icons + social image tags for a page at `path` (e.g. 'guides/x/'). Privacy page: old head kept unchanged."""
    if path == "privacy/":
        return OLD_ICON
    return SOCIAL_META + ICON_LINKS
