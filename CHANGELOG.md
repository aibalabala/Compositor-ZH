## 1.4.9-zh.1 — 2026-10-11

- Rename application and GitHub project to **Compositor-ZH**.
- Rename `.app`, DMG and ZIP outputs, app-visible branding, Finder file type labels, and macOS build/test paths.
- Retain the internal Swift module/scheme `Compositor` and legacy `.comp` project format. Use bundle identifier `com.aibalabala.compositorzh` for the renamed app.
- Functional upstream base remains Compositor v1.4.9.

# Changelog

Compositor-ZH follows the upstream Compositor version and adds a Compositor-ZH revision suffix:

`<upstream-version>-zh.<revision>`

Example: `1.3.7-zh.1`.

The macOS app's `CFBundleShortVersionString` remains the numeric upstream-compatible version (for example `1.3.7`). The Compositor-ZH revision is tracked by Git tags, `COMPOSITOR_ZH_VERSION`, release notes, and build metadata.


历史版本记录保留在 GitHub Releases 页面。
