"""Contrato estructural del sitio; SITE_DIR selecciona la compilación a revisar."""
import os
import re
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

SITE = Path(os.environ.get("SITE_DIR", "site")).resolve()
LEGACY_ROUTES = ("migration-manual", "spiral-strategy", "migration-templates",
                 "versions", "recipes", "validation", "known-errors", "ai-guide", "case-template")
ROUTES = ("", "procedure", "user-instructions", "gentle-shell", "architecture",
          *LEGACY_ROUTES)
BASE = "https://hito2026.github.io/hito-migrations/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.primary_links = []
        self.primary_link_levels = []
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
                self.primary_link_levels.append((href, self._primary_depth - 1))

    def handle_endtag(self, tag):
        if tag == "nav" and self._primary_depth:
            self._primary_depth -= 1

    def has(self, tag, key, value):
        return any(t == tag and a.get(key) == value for t, a in self.tags)


class SiteContract(unittest.TestCase):
    def page(self, route=""):
        return Page(SITE / route / "index.html")

    def test_publication_excludes_draft_reports_and_local_notes(self):
        for path in ("migrando", "technical-plan", ".local-work", "odd"):
            self.assertFalse((SITE / path).exists(), path)
        search = (SITE / "search/search_index.json").read_text(encoding="utf-8")
        self.assertNotIn('"location": "migrando/', search)
        self.assertNotIn("Calendario planificado", search)

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

    def test_bounded_content_without_right_sidebar(self):
        for route in ROUTES:
            with self.subTest(route=route):
                page = self.page(route)
                self.assertNotIn("md-sidebar--secondary", page.text)
                self.assertIn("md-sidebar--primary", page.text)
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.md-grid\s*\{[^}]*max-width:\s*1280px\s*;")
        self.assertRegex(css, r"\.md-grid\s*\{[^}]*margin-inline:\s*auto\s*;")
        self.assertRegex(css, r"\.md-content__inner\s*\{[^}]*max-width:\s*936px\s*;")
        self.assertRegex(css, r"\.process-diagram\s*\{[^}]*overflow-x:\s*auto\s*;")

    def test_right_margin_and_diagrams_fit_available_width(self):
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.md-content__inner\s*\{[^}]*margin-right:\s*clamp\(\.8rem, 3vw, 3rem\)\s*;")
        image = re.search(r"\.md-typeset \.process-diagram img\s*\{([^}]*)\}", css)
        self.assertIsNotNone(image)
        for declaration in ("width: 100%;", "min-width: 0;", "max-width: 100%;", "height: auto;"):
            self.assertIn(declaration, image.group(1))
        self.assertNotIn("min-width: 48rem", image.group(1))

    def test_copyable_blocks_use_smaller_courier_font(self):
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        block = re.search(r"\.md-typeset pre > code\s*\{([^}]*)\}", css)
        self.assertIsNotNone(block)
        for declaration in ('font-family: "Courier New", Courier, monospace;',
                            'font-size: .65rem;', 'line-height: 1.5;'):
            self.assertIn(declaration, block.group(1))

    def test_migrando_menu_only_lists_the_three_remaining_guides(self):
        expected = {BASE, BASE + "procedure/", BASE + "gentle-shell/"}
        for route in ROUTES:
            with self.subTest(route=route):
                page = self.page(route)
                current = BASE + (route + "/" if route else "")
                self.assertEqual({urljoin(current, link) for link in page.primary_links}, expected)
                expected_levels = {url: 1 for url in expected}
                self.assertEqual({urljoin(current, link): level for link, level in page.primary_link_levels},
                                 expected_levels)
                nav_levels = [attrs["data-md-level"] for tag, attrs in page.tags
                              if tag == "nav" and "data-md-level" in attrs]
                self.assertEqual(nav_levels, ["0", "1"])
                for label in ("Introducción", "Procedimiento", "Gentle Shell"):
                    self.assertIn(label, page.text)
        intro = self.page()
        for text in ("La idea del proyecto", "Cómo trabajamos", "Borrador no verificado"):
            self.assertIn(text, intro.text)
        self.assertTrue(intro.has("a", "href", "procedure/"))
        self.assertFalse(intro.has("a", "href", "user-instructions/"))
        self.assertTrue(intro.has("a", "href", "gentle-shell/"))
        self.assertNotIn("Abrir el manual de Gentle Shell", intro.text)

    def test_introduction_distinguishes_code_database_and_migration_acceptance(self):
        page = self.page()
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for topic in ("17.0", "19.0", "OCA", "ADHOC", "Hito", "custom-cliente",
                      "Python", "XML", "repositorio principal", "submódulos",
                      "código", "datos históricos", "Staging", "producción"):
            self.assertIn(topic, plain)
        self.assertTrue(page.has("a", "href", "https://upgrade.odoo.com/"))
        for limitation in ("no adapta automáticamente", "no acredita aceptación",
                           "autorización específica", "Borrador no verificado"):
            self.assertIn(limitation, plain)

    def test_introduction_explains_both_repository_strategies_and_replacement_risks(self):
        page = self.page()
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for heading in ("adaptar-el-repositorio-actual", "preparar-el-repositorio-de-destino"):
            self.assertTrue(page.has("h3", "id", heading))
        for detail in ("Equipavic", "Smarttract", "localización", "payment_group",
                       "account-payment-pro", "no demuestra equivalencia", "en paralelo", "espiral"):
            self.assertIn(detail, plain)
        # El esquema se explica por función, sin exponer nombres de repositorios internos.
        self.assertNotIn("hito-devman", plain)
        self.assertNotIn("account-payment-hito", plain)

    def test_introduction_scopes_agent_support_and_unverified_functional_testing(self):
        page = self.page()
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for detail in ("Qué aporta el agente", "migrados", "pendientes", "reemplazo",
                       "dependencias", "pruebas técnicas", "pruebas funcionales",
                       "capacidad no probada", "No sustituye la aceptación humana"):
            self.assertIn(detail, plain)
        self.assertTrue(page.has("a", "href", "procedure/"))
        self.assertTrue(page.has("a", "href", "gentle-shell/"))

    def test_technical_plan_is_the_single_spiral_document(self):
        page = self.page("spiral-strategy")
        for phrase in ("Estrategia de migración en espiral", "S1 — Entrada", "S2 — Inventario",
                       "S3 — Portado", "S4 — Runtime", "S5 — Aceptación", "S6 — Plan",
                       "Clasificar antes de portar", "Estados del tablero y evidencia",
                       "Coordinación por oleadas", "no verificada"):
            self.assertIn(phrase, page.text)
        raw = "https://raw.githubusercontent.com/hito2026/hito-migrations/refs/heads/docs/spiral-strategy/docs/spiral-strategy.md"
        self.assertTrue(page.has("a", "href", raw))
        self.assertIn("Plan técnico general de migración", page.text)
        self.assertFalse((SITE / "technical-plan").exists())





    def test_diagrams_are_thirty_percent_shorter_at_same_width(self):
        expected_heights = {"migration-process.svg": 1498, "solution-architecture.svg": 1840.3}
        for filename, expected_height in expected_heights.items():
            with self.subTest(diagram=filename):
                svg = ElementTree.parse(SITE / "assets" / filename).getroot()
                _, _, width, height = map(float, svg.attrib["viewBox"].split())
                self.assertEqual(width, 960)
                self.assertAlmostEqual(height, expected_height)
                self.assertFalse(any("transform" in node.attrib for node in svg.iter()))
                style = next(node.text for node in svg.iter() if node.tag.endswith("}style"))
                self.assertRegex(style, r"text\s*\{[^}]*font-size:\s*14px;")
                self.assertRegex(style, r"\.note\s*\{[^}]*font-size:\s*12\.6px;")
        css = (SITE / "stylesheets/extra.css").read_text(encoding="utf-8")
        figure = re.search(r"\.md-typeset \.process-diagram\s*\{([^}]*)\}", css).group(1)
        for declaration in ("width: 100%;", "max-width: 100%;", "box-sizing: border-box;", "padding: .25rem;"):
            self.assertIn(declaration, figure)

    def test_procedure_has_seven_copyable_operator_steps(self):
        page = self.page("procedure")
        headings = [unescape(re.sub(r"<[^>]+>", "", heading)).strip()
                    for heading in re.findall(r"<h2\b[^>]*>(.*?)</h2>", page.text, re.S)]
        self.assertEqual(headings, ["1. Conectarse al servidor", "2. Entrar al proyecto",
                                    "3. Abrir Gentle Shell", "4. Iniciar o continuar",
                                    "5. Si inicia: informar repositorio y accesos",
                                    "6. En paralelo: solicitar la actualización de la base",
                                    "7. Seguir al agente y el plan en espiral"])
        commands = [unescape(command).strip() for command in re.findall(
            r'<pre><code class="language-sh">(.*?)</code></pre>', page.text, re.S)]
        self.assertEqual(commands, ["ssh servidor-migraciones",
                                    'cd "/srv/migraciones/cases/MIG-Nombre del proyecto"',
                                    "gentle-shell"])
        prompts = [unescape(prompt) for prompt in re.findall(
            r'<pre><code class="language-text">(.*?)</code></pre>', page.text, re.S)]
        self.assertEqual(len(prompts), 7)
        self.assertIn("Continúe", prompts[0])
        self.assertIn("Inicie", prompts[1])
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for phrase in ("ya creado y asignado", "no abra otro coordinador",
                       "Nombre del proyecto", "no autoriza operaciones sobre bases ni producción"):
            self.assertIn(phrase, plain)
        self.assertTrue(page.has("a", "href", "../spiral-strategy/"))
        self.assertTrue(page.has("a", "href", "../gentle-shell/#7-retomar-el-trabajo"))
        self.assertFalse(page.has("img", "src", "../assets/migration-process.svg"))

    def test_procedure_new_case_collects_repository_and_both_ssh_endpoints(self):
        page = self.page("procedure")
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for label in ("Repositorio principal:", "SSH de origen:", "SSH de destino:",
                      "No pegue contraseñas", "claves privadas", "canal privado del caso"):
            self.assertIn(label, plain)

    def test_procedure_database_test_upgrade_runs_in_parallel_not_production(self):
        page = self.page("procedure")
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        self.assertTrue(page.has("a", "href", "https://upgrade.odoo.com/"))
        for label in ("En paralelo", "Staging", "UPGRADE", "Test Upgrade", "Testing",
                      "No seleccione Production", "no acredita aceptación de los datos"):
            self.assertIn(label, plain)

    def test_procedure_agent_follows_the_named_spiral_specification(self):
        page = self.page("procedure")
        plain = unescape(re.sub(r"<[^>]+>", "", page.text))
        for phrase in ("migration-spiral-strategy-spec.md", "Siga las indicaciones del agente",
                       "permisos correspondientes"):
            self.assertIn(phrase, plain)

    def test_technical_process_diagram_remains_available_as_a_reference(self):
        svg = ElementTree.parse(SITE / "assets/migration-process.svg").getroot()
        self.assertEqual(svg.attrib.get("role"), "img")
        text = " ".join(svg.itertext())
        for label in ("Usuario", "Coordinación", "Equipo técnico", "Proveedor",
                      "Entrada", "Plan", "Código", "Historia", "Ensayo", "Corte"):
            self.assertIn(label, text)
        self.assertTrue(any(node.attrib.get("class") == "gateway" for node in svg.iter()))
        self.assertTrue(any(node.attrib.get("class") == "event" for node in svg.iter()))

    def test_user_instructions_are_integrated_at_the_corresponding_procedure_steps(self):
        page = self.page("procedure")
        sections = dict(re.findall(r'<h2 id="([^"]+)"[^>]*>.*?</h2>(.*?)(?=<h2\b|$)',
                                   page.text, re.S))
        start = sections["5-si-inicia-informar-repositorio-y-accesos"]
        for text in ("Origen y destino:", "Fuentes permitidas:", "Fuera de alcance:",
                     "Responsables:", "Restricciones:", "No modifique archivos", "No restaure bases"):
            self.assertIn(text, start)
        upgrade = sections["6-en-paralelo-solicitar-la-actualizacion-de-la-base"]
        self.assertIn("Testing", upgrade)
        self.assertNotIn("El responsable de datos autoriza", upgrade)
        follow = sections["7-seguir-al-agente-y-el-plan-en-espiral"]
        for label in ("Para adaptar código", "Para probar el funcionamiento", "Para validar los datos",
                      "Para ensayar el corte", "Para decidir producción", "Cómo responder una consulta o un bloqueo"):
            self.assertIn(label, follow)
        for text in ("No amplíe el alcance", "No use datos productivos", "No modifique el origen",
                     "No ejecute el corte real", "Si se pospone: no ejecute", "aprobación", "bloqueo"):
            self.assertIn(text, follow)

    def test_legacy_user_instructions_route_links_to_the_merged_content(self):
        page = self.page("user-instructions")
        self.assertEqual(sum(tag == "pre" for tag, _ in page.tags), 0)
        targets = ("5-si-inicia-informar-repositorio-y-accesos", "para-adaptar-codigo",
                   "para-probar-el-funcionamiento", "para-validar-los-datos", "para-ensayar-el-corte",
                   "para-decidir-produccion", "como-responder-una-consulta-o-un-bloqueo")
        for target in targets:
            self.assertTrue(page.has("a", "href", "../procedure/#" + target), target)
        for route in ROUTES:
            current = BASE + (route + "/" if route else "")
            self.assertNotIn(BASE + "user-instructions/",
                             {urljoin(current, link) for link in self.page(route).primary_links})

    def test_gentle_shell_manual_is_linked_and_scoped(self):
        self.assertTrue(self.page("procedure").has("a", "href", "../gentle-shell/"))
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
        self.assertFalse(page.has("a", "href", "../user-instructions/"))
        self.assertTrue(page.has("a", "href", "../procedure/"))

    def test_gentle_shell_has_platform_specific_client_steps(self):
        page = self.page("gentle-shell")
        for anchor in ("windows", "linux", "macos"):
            self.assertTrue(any(tag in ("h2", "h3", "h4") and attrs.get("id") == anchor
                                for tag, attrs in page.tags), anchor)
        plain = re.sub(r"<[^>]+>", "", page.text)
        for command in ("PowerShell", "OpenSSH.Client~~~~0.0.1.0", "Invoke-WebRequest",
                        "Get-Content", "notepad", "$HOME\\.ssh\\config",
                        "openssh-client", "openssh-clients", "cloudflared-linux-amd64",
                        "cloudflared-linux-arm64", "brew install cloudflared", "nano ~/.ssh/config"):
            self.assertIn(command, plain)
        self.assertIn("A partir de aquí", plain)
        self.assertIn("comandos de Linux en el servidor", plain)
        self.assertIn("C:/Users/", plain)
        self.assertIn("Windows o macOS", plain)

    def test_each_platform_offers_a_safe_copyable_ai_prompt(self):
        page = self.page("gentle-shell")
        blocks = [unescape(block) for block in re.findall(
            r'<pre><code class="language-text">(.*?)</code></pre>', page.text, re.S)]
        for platform in ("Windows", "Linux", "macOS"):
            prompts = [block for block in blocks
                       if block.startswith("Ayúdeme a configurar el acceso a PC-ALE desde " + platform)]
            self.assertEqual(len(prompts), 1, platform)
            prompt = prompts[0]
            for rule in ("hostname", "usuario", "huella", "autorización", "sin sobrescribir",
                         "clave privada", "tokens", "navegador", "whoami", "gentle-shell --version",
                         "No modifique el servidor"):
                self.assertIn(rule, prompt, (platform, rule))
        windows = next(block for block in blocks if block.startswith(
            "Ayúdeme a configurar el acceso a PC-ALE desde Windows"))
        self.assertIn("PowerShell", windows)
        self.assertIn("no OpenSSH Server", windows)
        linux = next(block for block in blocks if block.startswith(
            "Ayúdeme a configurar el acceso a PC-ALE desde Linux"))
        self.assertIn("distribución", linux)
        self.assertIn("arquitectura", linux)
        mac = next(block for block in blocks if block.startswith(
            "Ayúdeme a configurar el acceso a PC-ALE desde macOS"))
        self.assertIn("Homebrew", mac)
        self.assertIn("Intel", mac)
        self.assertIn("Apple Silicon", mac)

    def guided_start_steps(self):
        page = self.page("gentle-shell")
        section = re.search(r'<h2 id="ejemplo-guiado-de-inicio"[^>]*>.*?</h2>(.*?)(?=<h2\b|\Z)', page.text, re.S)
        self.assertIsNotNone(section, "Falta el ejemplo guiado de inicio")
        steps = re.findall(r'<h3\b[^>]*>.*?Paso (\d+)\b.*?</h3>(.*?)(?=<h3\b|\Z)', section.group(1), re.S)
        self.assertEqual([int(number) for number, _ in steps], list(range(1, 12)))
        return dict((int(number), body) for number, body in steps)

    def test_guided_start_covers_the_observed_user_workflow(self):
        steps = self.guided_start_steps()
        expected = {
            1: ("whoami", "Darwin", "Get-Command"),
            2: ("ssh -l dev1 servidor-migraciones", "navegador"),
            3: ("tmux new-session -A -s main", "reinicio"),
            4: ("gentle-shell", "actualizaciones"),
            5: ("CONEXIÓN OK", "consumir", "credenciales"),
            6: ("Ctrl+b", "mig-case list", "vacía"),
            7: ("MIG-DEMO-1719", "MIG-DEMO1719-001", "mig-case new"),
            8: ("mig-case claim MIG-DEMO1719-001", "&&", "no borre"),
            9: ("gentle-shell", "Trust (this session only)", "instalar", "extensiones"),
            10: ("case-intake.yml", "module-board.yml", "runbook.md", "<RUTA_DE_GUIA_DE_LECCIONES>", "Engram"),
            11: ("Versión de Odoo de origen:", "Rama de origen:", "plantilla", "19.0"),
        }
        for number, tokens in expected.items():
            plain = unescape(re.sub(r'<[^>]+>', '', steps[number]))
            for token in tokens:
                self.assertIn(token, plain, (number, token))
        page = self.page("gentle-shell")
        self.assertTrue(page.has("a", "href", "#ejemplo-guiado-de-inicio"))

    def test_each_guided_start_step_has_an_approval_scoped_ai_prompt(self):
        for number, body in self.guided_start_steps().items():
            with self.subTest(step=number):
                prompts = [unescape(block) for block in re.findall(
                    r'<pre><code class="language-text">(.*?)</code></pre>', body, re.S)
                    if unescape(block).startswith("Asístame en el paso " + str(number) + ".")]
                self.assertEqual(len(prompts), 1)
                prompt = prompts[0]
                self.assertIn("Explique el paso y pida mi autorización antes de ejecutarlo.", prompt)
                self.assertIn("No avance al siguiente paso sin una nueva autorización.", prompt)
                self.assertIn("No pida ni muestre secretos.", prompt)
        readonly = unescape(self.guided_start_steps()[10])
        for limit in ("No modifique archivos", "no instale", "no clone", "servicios externos", "memoria persistente"):
            self.assertIn(limit, readonly)

    def guided_resume_steps(self):
        page = self.page("gentle-shell")
        section = re.search(r'<h2 id="ejemplo-guiado-para-retomar-un-caso"[^>]*>.*?</h2>(.*?)(?=<h2\b|\Z)', page.text, re.S)
        self.assertIsNotNone(section, "Falta el ejemplo guiado para retomar")
        steps = re.findall(r'<h3\b[^>]*>.*?Paso (\d+)\b.*?</h3>(.*?)(?=<h3\b|\Z)', section.group(1), re.S)
        self.assertEqual([int(number) for number, _ in steps], list(range(1, 7)))
        return dict((int(number), body) for number, body in steps)

    def test_guided_resume_covers_disconnect_reconnect_and_existing_instance(self):
        steps = self.guided_resume_steps()
        expected = {
            1: ("terminal", "waiting for input", "main"),
            2: ("Ctrl+b", "prompt remoto", "exit", "no libera"),
            3: ("ssh -l dev1 servidor-migraciones", "cuenta"),
            4: ("tmux list-sessions", "tmux list-panes -a -F", "#{pane_current_path}", "mig-case status MIG-DEMO1719-001"),
            5: ("tmux attach-session -t main:1", "No ejecute de nuevo", "gentle-shell"),
            6: ("runbook.md", "module-board.yml", "case-intake.yml", "plantilla", "No use Engram"),
        }
        for number, tokens in expected.items():
            plain = unescape(re.sub(r'<[^>]+>', '', steps[number]))
            for token in tokens:
                self.assertIn(token, plain, (number, token))
        page = self.page("gentle-shell")
        self.assertTrue(page.has("a", "href", "#ejemplo-guiado-para-retomar-un-caso"))
        plain = unescape(re.sub(r'<[^>]+>', '', page.text))
        for limit in ("variante no se probó", "no recupera automáticamente la conversación", "cd /srv/migraciones/cases/MIG-DEMO1719-001"):
            self.assertIn(limit, plain)

    def test_each_guided_resume_step_has_an_approval_scoped_ai_prompt(self):
        for number, body in self.guided_resume_steps().items():
            with self.subTest(step=number):
                prompts = [unescape(block) for block in re.findall(
                    r'<pre><code class="language-text">(.*?)</code></pre>', body, re.S)
                    if unescape(block).startswith("Para retomar, asístame en el paso " + str(number) + ".")]
                self.assertEqual(len(prompts), 1)
                for limit in ("Explique el paso y pida mi autorización antes de ejecutarlo.",
                              "No avance al siguiente paso sin una nueva autorización.",
                              "No pida ni muestre secretos."):
                    self.assertIn(limit, prompts[0])

    def test_architecture_has_accessible_local_diagram_and_boundaries(self):
        page = self.page("architecture")
        self.assertTrue(page.has("img", "src", "../assets/solution-architecture.svg"))
        self.assertTrue(page.has("img", "alt", "Arquitectura de Mac de Ale, usuarios y PC-ALE"))
        self.assertTrue(page.has("figure", "tabindex", "0"))
        svg = ElementTree.parse(SITE / "assets/solution-architecture.svg").getroot()
        self.assertEqual(svg.attrib.get("role"), "img")
        ids = {node.attrib.get("id") for node in svg.iter()}
        self.assertTrue(set(svg.attrib["aria-labelledby"].split()).issubset(ids))
        text = " ".join(svg.itertext())
        for label in ("Mac de Ale", "Windows", "Linux", "macOS", "PC-ALE", "Gentle Shell",
                      "Pi", "Cloudflare Access", "SSH", "tmux", "Kit", "Casos", "Odoo.sh",
                      "GitHub", "Engram", "pendiente", "Tailscale"):
            self.assertIn(label, text)
        for label in ("Administración", "Ejecución", "Credenciales", "Límites y pendientes"):
            self.assertIn(label, page.text)
        plain = re.sub(r"<[^>]+>", "", page.text)
        self.assertIn("no pasa por la Mac", plain)
        self.assertIn("un coordinador por caso", plain)
        self.assertIn("sin sudo ni Docker", plain)
        self.assertTrue(page.has("a", "href", "../gentle-shell/"))
        self.assertFalse(any(node.tag.rsplit("}", 1)[-1] in ("script", "foreignObject", "image")
                             for node in svg.iter()))

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
                self.assertTrue(page.has("span", "data-doc-version", "0.3.0"))
                self.assertIn("Versión documental 0.3.0", page.text)
                self.assertTrue(page.has("time", "datetime", "2026-10-21"))
                self.assertIn("Actualizado", page.text)
                self.assertIn("21/10/2026", page.text)

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
