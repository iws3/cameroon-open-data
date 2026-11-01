#!/usr/bin/env python3
"""Writes the web forms in .github/ISSUE_TEMPLATE from tools/forms_spec.py.

Run it again whenever you add a folder or change a form:
    python tools/build_forms.py
"""
import json
from pathlib import Path

from forms_spec import FORMS, human
from build_structure import STRUCTURE

OUT = Path(__file__).resolve().parent.parent / ".github" / "ISSUE_TEMPLATE"


def q(s):
    return json.dumps(s, ensure_ascii=False)


def render(spec):
    lines = [f"name: {q(spec['name'])}", f"description: {q(spec['desc'])}", f"title: {q(spec['title'])}", f"labels: [{q(spec['label'])}]", "body:"]
    lines += ["  - type: markdown", "    attributes:", f"      value: {q(spec['intro'])}"]
    for f in spec["fields"]:
        lines += [f"  - type: {f['kind']}", f"    id: {f['id']}", "    attributes:", f"      label: {q(f['label'])}"]
        if f.get("desc"):
            lines.append(f"      description: {q(f['desc'])}")
        if f["kind"] == "dropdown":
            lines.append("      options:")
            lines += [f"        - {q(o)}" for o in f["options"]]
        if f["kind"] == "checkboxes":
            lines.append("      options:")
            for o in f["options"]:
                lines += [f"        - label: {q(o)}", "          required: true"]
        if f.get("req") and f["kind"] != "checkboxes":
            lines += ["    validations:", "      required: true"]
    return "\n".join(lines) + "\n"


def recording_form():
    sectors = [human(k) for k in STRUCTURE if k != "_inbox"]
    spec = {
        "name": "Share a recording, scan or document", "desc": "Share audio, video or a scan. A volunteer will transcribe it.",
        "title": "Recording: ", "label": "needs-transcription",
        "intro": "Share a recording of a story, a song, a conversation, a radio programme, or a scan of a document. A volunteer will transcribe it. Please share only what you recorded yourself or have permission to share, and only recordings of people who agreed to be recorded.",
        "fields": [
            {"kind": "dropdown", "id": "sector", "label": "Sector", "req": True, "options": sectors + ["Not sure"]},
            {"kind": "textarea", "id": "files", "label": "Files", "desc": "Drag your audio, video, picture or PDF into this box.", "req": True},
            {"kind": "textarea", "id": "what", "label": "What is it?", "desc": "Who is speaking, about what, where and when. Keep full names of private people out if they did not agree.", "req": True},
            {"kind": "input", "id": "lang", "label": "Language", "desc": "For example Ewondo, Pidgin, French.", "req": True},
            {"kind": "input", "id": "contributor", "label": "Your name for credit"},
            {"kind": "checkboxes", "id": "consent", "label": "Consent", "req": True,
             "options": ["Every person speaking agreed to be recorded and to the recording being shared, and I have the right to share it."]},
        ],
    }
    return render(spec)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in FORMS.values():
        (OUT / spec["file"]).write_text(render(spec), encoding="utf-8")
        print("wrote", spec["file"], f"({len(spec['fields'])} boxes)")
    (OUT / "share-recording.yml").write_text(recording_form(), encoding="utf-8")
    print("wrote share-recording.yml")


if __name__ == "__main__":
    main()
