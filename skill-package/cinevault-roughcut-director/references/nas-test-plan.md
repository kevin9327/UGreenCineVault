# Round 2 Hardware Validation and Test Plan

This document outlines the validation protocol for testing `cinevault-roughcut-director` on an assigned **UGREEN AI NAS iDX6011 Pro (64GB)** environment during Round 2 Finalist testing.

## 1. Core Test Case 1: End-to-End Multi-Modal Rough-Cut Vault Assembly

- **Objective**: Verify that all five delegated Uliya experts (`photo-agent`, `media-agent`, `document-agent`, `knowledge-agent`, and `file-agent`) chain real upstream outputs into downstream stages without path guessing.
- **Test Dataset on NAS**:
  - 24 RAW/JPEG still photos with EXIF camera/lens metadata and clapperboard text in an authorized project folder.
  - 6 MP4 B-roll video clips (4K H.264/HEVC) and 3 WAV/MP3 field interview voice recordings.
  - 2 PDF production documents (a shooting brief and a talent release checklist).
  - 4 royalty-free reference music tracks indexed in the NAS music library.
- **Execution Flow**:
  1. Trigger the Skill with a natural prompt requesting a rough-cut vault for the project theme and date window.
  2. Verify `photo-agent` discovers the matching photos, extracts clapperboard OCR and VLM scene descriptions, and requests `waiting_approval` before creating the storyboard album via `create-album-condition`.
  3. Verify `media-agent` matches the video clips and soundtrack stems without auto-playing.
  4. Verify `document-agent` reconciles the shooting brief against the release checklist, and `knowledge-agent` transcribes the interview recordings and requests `waiting_approval` before saving the Markdown Edit Decision Sheet via `save-text`.
  5. Verify `file-agent` runs `mediainfo`, `sha256sum`, and `scan-dedupe`, then requests `waiting_approval` before creating the target vault folder (`mkdir`) and consolidating selects (`batch-move`).
- **Expected Result**: All five delegations return `completed`, the storyboard album and Markdown Edit Decision Sheet are created, and only non-duplicate approved selects are consolidated.

## 2. Core Test Case 2: Duplicate Take Detection and Partial Approval Rejection

- **Objective**: Verify that the Skill preserves read-only discovery outputs and respects user rejection during `waiting_approval` without corrupting NAS directories.
- **Test Dataset on NAS**:
  - A workspace containing 3 byte-identical camera card backup clips alongside 5 unique clips and 1 interview audio file.
- **Execution Flow**:
  1. Run discovery and verify `ug-filemgr` `scan-dedupe` identifies the 3 byte-identical copies.
  2. Approve the read-only Edit Decision Sheet save (`save-text`), but decline the final `batch-move` approval prompt (`cancelled`).
- **Expected Result**: The Markdown Edit Decision Sheet is saved with the duplicate report intact, while the source directory files remain untouched and the Skill exits cleanly with `cancelled` status for the file movement stage.

## 3. Edge Case Test: Zero-Match Scope and Uncorrupted Abstention

- **Objective**: Verify strict empty-result abstention when the user queries a date window or keyword with zero matching assets on the NAS.
- **Execution Flow**:
  1. Trigger the Skill with a non-existent project keyword or a future date range (`2030-01-01` to `2030-01-07`).
- **Expected Result**: `photo-agent`, `media-agent`, and `document-agent` return empty results (`zero matches`). The Skill immediately reports `no results` to the user, halts all downstream write stages (`create-album-condition`, `save-text`, `mkdir`, `batch-move`), and never fabricates placeholder paths or synthetic media records.
