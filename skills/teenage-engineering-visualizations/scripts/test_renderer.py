#!/usr/bin/env python3
"""Free contract checks. These do not launch a browser or contact a service."""
import copy
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch
import xml.etree.ElementTree as ET

from render import COLORS, Drawing, ROOT, check_spec, html_document


class RenderingContracts(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "examples/sequence.json"
        self.spec = json.loads(self.path.read_text(encoding="utf-8"))

    def test_generation_is_deterministic(self):
        state = check_spec(self.spec)[-1]
        first = Drawing(self.spec, self.path, "slide", state).render()
        second = Drawing(self.spec, self.path, "slide", state).render()
        self.assertEqual(first, second)

    def test_code_preserves_indentation_and_spaces(self):
        spec = copy.deepcopy(self.spec)
        spec["steps"][-1]["code"] = "if passed:\n    release(artifact)  # checked"
        svg = Drawing(spec, self.path, "slide", check_spec(spec)[-1]).render()
        tree = ET.fromstring(svg)
        text = [element.text for element in tree.iter("{http://www.w3.org/2000/svg}text")]
        self.assertIn("    release(artifact)  # checked", text)
        self.assertIn('xml:space="preserve"', svg)

    def test_unknown_state_component_is_rejected(self):
        self.spec["states"][0]["focus"] = ["invented"]
        with self.assertRaisesRegex(ValueError, "unknown"):
            check_spec(self.spec)

    def test_transformations_require_explicit_intermediate_values(self):
        spec = json.loads((ROOT / "examples/transformation.json").read_text(encoding="utf-8"))
        del spec["steps"][1]["input"]
        with self.assertRaisesRegex(ValueError, "explicit input and output"):
            check_spec(spec)

    def test_focused_callout_uses_large_dark_text(self):
        drawing = Drawing(self.spec, self.path, "slide", check_spec(self.spec)[0])
        drawing.number(2, 30, 30, True)
        text = ET.fromstring('<svg>' + ''.join(drawing.items) + '</svg>').find('text')
        self.assertEqual(text.attrib['fill'], COLORS['ink'])
        self.assertEqual(text.attrib['font-weight'], '600')
        self.assertGreaterEqual(float(text.attrib['font-size']), 19)

    def test_ids_are_unique_across_frames(self):
        ids = []
        for state in check_spec(self.spec):
            tree = ET.fromstring(Drawing(self.spec, self.path, "slide", state).render())
            ids.extend(node.attrib["id"] for node in tree.iter() if "id" in node.attrib)
        self.assertEqual(len(ids), len(set(ids)))

    def test_html_has_no_network_or_execution_api(self):
        states = check_spec(self.spec)
        frames = [(state, Drawing(self.spec, self.path, "slide", state).render()) for state in states]
        document = html_document(self.spec, frames)
        for prohibited in ["fetch(", "XMLHttpRequest", "WebSocket", "navigator.sendBeacon"]:
            self.assertNotIn(prohibited, document)
        self.assertIn("ArrowRight", document)
        self.assertIn("prefers-reduced-motion", document)

    def test_html_colors_come_from_tokens(self):
        with patch.dict(COLORS, {"paper": "#010203", "disabled": "#040506"}):
            document = html_document(self.spec, [])
        self.assertIn("--paper:#010203", document)
        self.assertIn("--disabled:#040506", document)
        self.assertIn("color:var(--disabled)", document)
        self.assertNotIn("--paper:#f4f3ef", document)

    def test_generic_poster_roles_do_not_require_forge(self):
        spec = json.loads((ROOT / "examples/poster.json").read_text(encoding="utf-8"))
        self.assertIn("roles", spec["poster"])
        self.assertNotIn("forge", spec["poster"])
        check_spec(spec)

    def test_poster_text_alternative_survives_a_hero_only_diagram(self):
        spec = json.loads((ROOT / "examples/poster.json").read_text(encoding="utf-8"))
        spec["steps"] = []
        document = html_document(spec, [])
        for outcome in spec["poster"]["outcomes"]:
            self.assertIn(outcome, document)
        for key in ("duration", "prerequisites", "dataset"):
            self.assertIn(spec["poster"][key], document)
        self.assertIn(spec["poster"]["cta"]["url"], document)
        self.assertNotIn('<ol></ol>', document)

    def test_native_capture_has_separate_provenance(self):
        self.spec["native_capture"] = {"title":"Saved record","investigation":"Find the source","media":"unused.svg","source_url":"https://example.com/record"}
        state = check_spec(self.spec)[-1]
        drawing = Drawing(self.spec, self.path, "slide", state)
        drawing.header()
        self.assertIn(">RECORDED</text>", "".join(drawing.items))
        self.assertNotIn(">ILLUSTRATIVE</text>", "".join(drawing.items))
        document = html_document(self.spec, [(check_spec(self.spec)[0], ""), (state, "")])
        self.assertIn('const provenances=["illustrative", "recorded"]', document)
        self.assertIn("document.querySelector('.status').textContent=provenances[current]", document)

    def test_all_compositions_have_distinct_reference_examples(self):
        kinds = set()
        for path in (ROOT / "examples").glob("*.json"):
            spec = json.loads(path.read_text(encoding="utf-8"))
            check_spec(spec)
            kinds.add(spec["kind"])
        self.assertEqual(kinds, {"overview","sequence","transformation","comparison","branches","poster"})

    def test_authored_drawing_keeps_geometry_text_and_local_marker_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scene.json"
            (path.parent / "scene.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675"><defs><marker id="arrow"/></defs><path d="M10 10L20 20" marker-end="url(#arrow)"/><text x="20" y="50">Actual field value</text></svg>', encoding="utf-8")
            state = {**check_spec(self.spec)[0], "artwork": "scene.svg"}
            spec = {**self.spec, "states": [state]}
            drawing = Drawing(spec, path, "notebook", state)
            tree = ET.fromstring(drawing.render())
            self.assertEqual((drawing.w, drawing.h), (1200, 675))
            self.assertIn("Actual field value", "".join(tree.itertext()))
            ids = [node.attrib["id"] for node in tree.iter() if "id" in node.attrib]
            self.assertEqual(len(ids), len(set(ids)))
            targets = [node.attrib["marker-end"][5:-1] for node in tree.iter() if "marker-end" in node.attrib]
            self.assertTrue(all(target in ids for target in targets))

    def test_artwork_cannot_load_remote_media_or_execute_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scene.json"
            for content in ('<script>run()</script>', '<image href="https://example.com/image.png"/>'):
                (path.parent / "scene.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675">'+content+'</svg>', encoding="utf-8")
                state = {**check_spec(self.spec)[0], "artwork": "scene.svg"}
                with self.assertRaises(ValueError):
                    Drawing({**self.spec, "states": [state]}, path, "slide", state).render()

    def test_inlined_artwork_styles_do_not_recolor_poster_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scene.json"
            (path.parent / "scene.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675"><style>text{fill:black}.mono{font-family:monospace}</style><text>Field</text></svg>', encoding="utf-8")
            state = {**check_spec(self.spec)[0], "artwork": "scene.svg"}
            svg = Drawing({**self.spec, "states": [state]}, path, "slide", state).render()
            tree = ET.fromstring(svg)
            styles = ''.join(node.text or '' for node in tree.iter('{http://www.w3.org/2000/svg}style'))
            self.assertIn('] text{fill:black}', styles)
            self.assertNotIn('<style>text{fill:black}', svg)


if __name__ == "__main__":
    unittest.main()
