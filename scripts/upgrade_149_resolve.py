#!/usr/bin/env python3
"""Resolve the reviewed v1.4.5 -> v1.4.9 three-way conflicts.

The upstream branch owns new feature flow. Aips retains brand, localization
entry points, project compatibility and its own Sparkle release metadata.
Unknown conflicts fail closed instead of silently choosing a side.
"""
from pathlib import Path
import re
import sys

ALLOWED = {
    "Compositor.xcodeproj/project.pbxproj",
    "Compositor/CompositorApp.swift",
    "Compositor/ContentView.swift",
    "Compositor/Document/EditorSession.swift",
    "Compositor/Document/ProjectWorkspace.swift",
    "Compositor/IO/ImageFileDrop.swift",
    "Compositor/IO/ImageImporter.swift",
    "Compositor/IO/ProjectController.swift",
    "Compositor/UI/BrushControls.swift",
    "Compositor/UI/FilterSheet.swift",
    "Compositor/UI/GradientControls.swift",
    "Compositor/UI/LassoControls.swift",
    "Compositor/UI/LayerMaskMenu.swift",
    "Compositor/UI/LayersPanel.swift",
    "Compositor/UI/NewCanvasSheet.swift",
    "Compositor/UI/ProjectTabs.swift",
    "appcast.xml",
}
PATTERN = re.compile(r"(?ms)^<<<<<<< ours\n(.*?)^=======\n(.*?)^>>>>>>> theirs\n")
conflicts_file = Path("report/conflicts.txt")
conflicts = set(conflicts_file.read_text().splitlines())
if conflicts != ALLOWED:
    raise SystemExit(f"Conflict set changed. Unexpected: {sorted(conflicts - ALLOWED)}; Missing: {sorted(ALLOWED - conflicts)}")

for path in sorted(conflicts):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    blocks = list(PATTERN.finditer(s))
    if not blocks:
        raise SystemExit(f"Conflict markers missing: {path}")
    def choose(m):
        ours, theirs = m.group(1), m.group(2)
        if path == "appcast.xml":
            return ours
        if path.endswith("project.pbxproj"):
            return (
                "\t\t\t\tMARKETING_VERSION = 1.4.9;\n"
                "\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.aibalabala.aips;\n"
                "\t\t\t\tPRODUCT_NAME = Aips;\n"
                "\t\t\t\tPRODUCT_MODULE_NAME = Compositor;\n"
            )
        if path.endswith("CompositorApp.swift"):
            return ours + theirs
        return theirs
    s = PATTERN.sub(choose, s)
    if "<<<<<<<" in s or ">>>>>>>" in s:
        raise SystemExit(f"Residual conflict marker: {path}")
    if path.endswith("ContentView.swift"):
        s = s.replace('.navigationTitle(session.projectURL?.deletingPathExtension().lastPathComponent ?? "Untitled")',
                      '.navigationTitle(session.projectURL?.deletingPathExtension().lastPathComponent ?? localized("Untitled"))')
    if path.endswith("ImageFileDrop.swift"):
        s = s.replace('let message = "Some dropped items couldn’t be read. Drag JPEG, PNG, HEIC, TIFF, WebP, or Photoshop (PSD) files from Finder."',
                      'let message = localized("Some dropped items couldn’t be read. Drag JPEG, PNG, HEIC, TIFF, WebP, or Photoshop (PSD) files from Finder.")')
    if path.endswith("ImageImporter.swift"):
        s = s.replace('case .unreadable: "The image could not be read. It may be damaged or unavailable."',
                      'case .unreadable: localized("The image could not be read. It may be damaged or unavailable.")')
        s = s.replace('case .unsupported: "Choose a JPEG, PNG, HEIC, TIFF, WebP, or Photoshop (PSD) file."',
                      'case .unsupported: localized("Choose a JPEG, PNG, HEIC, TIFF, WebP, or Photoshop (PSD) file.")')
    if path.endswith("ProjectTabs.swift"):
        s = s.replace('.help("Close \\(tab.title)")', '.help(String(localized: "Close \\(tab.title)"))')
        s = s.replace('.accessibilityLabel("Close \\(tab.title)")', '.accessibilityLabel(String(localized: "Close \\(tab.title)"))')
    p.write_text(s, encoding="utf-8")
    print(f"{path}: resolved {len(blocks)} conflict block(s)")

Path("UPSTREAM_VERSION").write_text("v1.4.9\n", encoding="utf-8")
Path("AIPS_VERSION").write_text("1.4.9-aips.1\n", encoding="utf-8")
print("All reviewed conflicts resolved; version files advanced.")
