"""Contrato estructural del sitio; SITE_DIR selecciona la compilación a revisar."""
import os
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(os.environ.get("SITE_DIR", "site")).resolve()
ROUTES = ("", "migration-manual", "spiral-strategy", "migration-templates",
          "versions", "recipes", "validation", "known-errors", "ai-guide", "case-template")
BASE = "https://hito2026.github.io/hito-migrations/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.text = path.read_text(encoding="utf-8")
        self.feed(self.text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def has(self, tag, key, value):
        return any(t == tag and a.get(key) == value for t, a in self.tags)


class SiteContract(unittest.TestCase):
    def page(self, route=""):
        return Page(SITE / route / "index.html")

    def test_spanish_canonical_and_routes(self):
        for route in ROUTES:
            with self.subTest(route=route):
                page = self.page(route)
                self.assertTrue(page.has("html", "lang", "es"))
                self.assertTrue(page.has("link", "href", BASE + (route + "/" if route else "")))

    def test_material_search_and_persistent_navigation(self):
        for route in ROUTES:
            page = self.page(route)
            self.assertTrue(page.has("div", "data-md-component", "search"))
            self.assertTrue(page.has("nav", "data-md-level", "0"))
            self.assertIn("md-sidebar--primary", page.text)
            self.assertNotIn('class="md-tabs"', page.text)

    def test_guide_right_toc(self):
        for route in ROUTES[1:]:
            with self.subTest(route=route):
                page = self.page(route)
                self.assertIn("md-sidebar--secondary", page.text)
                self.assertTrue(page.has("nav", "aria-label", "Tabla de contenidos"))

    def test_home_cards_and_visible_evidence(self):
        page = self.page()
        self.assertTrue(any("topic-cards" in a.get("class", "").split() for _, a in page.tags))
        for route in ROUTES[1:]:
            self.assertTrue(page.has("a", "href", route + "/"))
        self.assertEqual(page.text.count('class="topic-card"'), 9)
        self.assertIn("Borrador no verificado", page.text)
        for label in ("No verificado", "Verificado en un contexto declarado", "Requiere revalidación"):
            self.assertIn(label, page.text)

    def test_hito_palette_targets_light_theme_scope(self):
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        # Contrato del selector generado; el color calculado requiere un navegador.
        theme_rules = [body for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
                       if 'body[data-md-color-scheme="default"]' in
                       [selector.strip() for selector in selectors.split(",")]]
        self.assertTrue(theme_rules, "La paleta debe declararse en el tema, no solo heredarse de :root")
        for variable, value in (("--md-primary-fg-color", "#174ea6"),
                                ("--md-accent-fg-color", "#174ea6"),
                                ("--md-default-fg-color", "#202b3c"),
                                ("--md-default-fg-color--light", "#48566a"),
                                ("--md-typeset-a-color", "#174ea6")):
            self.assertTrue(any(re.search(rf"{re.escape(variable)}\s*:\s*{value}\s*;", body)
                                for body in theme_rules), variable)

    def test_local_links_resources_and_no_external_fonts(self):
        for route in ROUTES:
            path = SITE / route / "index.html"
            page = Page(path)
            self.assertNotIn("fonts.googleapis.com", page.text)
            self.assertNotIn("fonts.gstatic.com", page.text)
            for tag, attrs in page.tags:
                for key in ("href", "src"):
                    url = urlsplit(attrs.get(key, ""))
                    if url.scheme or url.netloc or not url.path:
                        if tag in ("script", "link") and (key == "src" or attrs.get("rel") == "stylesheet"):
                            self.assertFalse(url.netloc, attrs)
                        continue
                    target = (SITE / unquote(url.path).lstrip("/") if url.path.startswith("/")
                              else path.parent / unquote(url.path))
                    self.assertTrue(target.exists(), f"{path}: {url.path}")


if __name__ == "__main__":
    unittest.main()
