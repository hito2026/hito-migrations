"""Contrato estructural del sitio; SITE_DIR selecciona la compilación a revisar."""
import os
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

SITE = Path(os.environ.get("SITE_DIR", "site")).resolve()
LEGACY_ROUTES = ("migration-manual", "spiral-strategy", "migration-templates",
                 "versions", "recipes", "validation", "known-errors", "ai-guide", "case-template")
ROUTES = ("", "procedure", "user-instructions", "gentle-shell", *LEGACY_ROUTES)
BASE = "https://hito2026.github.io/hito-migrations/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.primary_links = []
        self._primary_depth = 0
        self.text = path.read_text(encoding="utf-8")
        self.feed(self.text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "nav":
            if self._primary_depth:
                self._primary_depth += 1
            elif "md-nav--primary" in attrs.get("class", "").split():
                self._primary_depth = 1
        if self._primary_depth and tag == "a" and "md-nav__link" in attrs.get("class", "").split():
            href = attrs.get("href", "")
            if href and not href.startswith("#"):
                self.primary_links.append(href)

    def handle_endtag(self, tag):
        if tag == "nav" and self._primary_depth:
            self._primary_depth -= 1

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

    def test_three_section_navigation_and_introduction(self):
        expected = {BASE, BASE + "procedure/", BASE + "user-instructions/"}
        for route in ROUTES:
            with self.subTest(route=route):
                page = self.page(route)
                current = BASE + (route + "/" if route else "")
                self.assertEqual({urljoin(current, link) for link in page.primary_links}, expected)
                for label in ("Introducción", "Procedimiento", "Instrucciones del usuario"):
                    self.assertIn(label, page.text)
        intro = self.page()
        for text in ("La idea del proyecto", "Cómo trabajamos", "Borrador no verificado"):
            self.assertIn(text, intro.text)
        self.assertTrue(intro.has("a", "href", "procedure/"))
        self.assertTrue(intro.has("a", "href", "user-instructions/"))
        self.assertTrue(intro.has("a", "href", "gentle-shell/"))

    def test_procedure_has_accessible_local_actor_diagram(self):
        page = self.page("procedure")
        self.assertTrue(page.has("img", "src", "../assets/migration-process.svg"))
        self.assertTrue(page.has("img", "alt", "Proceso de migración por actores, etapas y decisiones"))
        svg = ElementTree.parse(SITE / "assets/migration-process.svg").getroot()
        self.assertEqual(svg.attrib.get("role"), "img")
        text = " ".join(svg.itertext())
        for label in ("Usuario", "Coordinación", "Equipo técnico", "Proveedor",
                      "Entrada", "Plan", "Código", "Historia", "Ensayo", "Corte"):
            self.assertIn(label, text)
        self.assertIn("no es un modelo ejecutable", page.text)
        self.assertTrue(any(node.attrib.get("class") == "gateway" for node in svg.iter()))
        self.assertTrue(any(node.attrib.get("class") == "event" for node in svg.iter()))

    def test_user_instructions_offer_stage_specific_prompts(self):
        page = self.page("user-instructions")
        for label in ("Para comenzar", "Para adaptar código", "Para probar el funcionamiento",
                      "Para validar los datos", "Para ensayar el corte", "Para decidir producción"):
            self.assertIn(label, page.text)
        self.assertGreaterEqual(sum(tag == "pre" for tag, _ in page.tags), 6)
        for text in ("No modifique archivos", "No restaure bases", "aprobación", "bloqueo"):
            self.assertIn(text, page.text)

    def test_gentle_shell_manual_is_linked_and_scoped(self):
        self.assertTrue(self.page("user-instructions").has("a", "href", "../gentle-shell/"))
        page = self.page("gentle-shell")
        for heading in ("Preparar el acceso", "Entrar al servidor", "Abrir su sesión",
                        "Abrir el caso", "Conectar el modelo", "Empezar la migración",
                        "Retomar el trabajo", "Entregar el caso"):
            self.assertIn(heading, page.text)
        plain = re.sub(r"<[^>]+>", "", page.text)
        for command in ("cloudflared access login", "ssh servidor-migraciones", "tmux attach",
                        "mig-case new", "mig-case claim", "mig-case release", "/login",
                        "gentle-shell", "case-intake.yml", "No modifique repositorios"):
            self.assertIn(command, plain)
        self.assertNotIn("Estado de las comprobaciones", plain)
        self.assertNotIn("13 pruebas", plain)
        self.assertIn("No copie claves privadas", plain)
        self.assertTrue(page.has("a", "href", "../user-instructions/"))
        self.assertTrue(page.has("a", "href", "../procedure/"))

    def test_hito_palette_targets_light_theme_scope(self):
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        # Contrato del selector generado; el color calculado requiere un navegador.
        theme_rules = [body for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
                       if 'body[data-md-color-scheme="default"]' in
                       [selector.strip() for selector in selectors.split(",")]]
        self.assertTrue(theme_rules, "La paleta debe declararse en el tema, no solo heredarse de :root")
        for variable, value in (("--md-primary-fg-color", "#750014"),
                                ("--md-accent-fg-color", "#750014"),
                                ("--md-default-fg-color", "#212326"),
                                ("--md-default-fg-color--light", "#626a73"),
                                ("--md-typeset-a-color", "#750014")):
            self.assertTrue(any(re.search(rf"{re.escape(variable)}\s*:\s*{value}\s*;", body)
                                for body in theme_rules), variable)

    def test_documentation_edition_visible_on_every_page(self):
        pages = [(route or "inicio", self.page(route)) for route in ROUTES]
        pages.append(("404", Page(SITE / "404.html")))
        for route, page in pages:
            with self.subTest(route=route):
                self.assertTrue(page.has("aside", "aria-label", "Edición de la documentación"))
                self.assertTrue(page.has("span", "data-doc-version", "0.2.1"))
                self.assertIn("Versión documental 0.2.1", page.text)
                self.assertTrue(page.has("time", "datetime", "2026-10-17"))
                self.assertIn("Actualizado", page.text)
                self.assertIn("17/10/2026", page.text)

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
