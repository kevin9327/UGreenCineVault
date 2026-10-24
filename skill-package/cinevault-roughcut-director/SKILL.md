---
name: cinevault-roughcut-director
description: Curated multimedia rough-cut production package, timecoded edit decision sheet, and tagged NAS media archive when users ask to organize project footage, photos, interview recordings, production scripts, and reference music into a ready-to-edit creative vault.
---

# Goal

Assemble a verified multimedia rough-cut production package on UGREEN AI NAS for filmmakers, video editors, and creative teams. Given a user-defined project theme, date window, and authorized NAS workspace scope, this orchestration Skill coordinates five registered Uliya domain experts to discover matching photos and B-roll footage, verify or retrieve subtitles, pair reference soundtrack stems, transcribe field interview recordings, reconcile production brief documents, generate a timecoded Markdown Edit Decision Sheet, and consolidate tagged selects into an approved project directory.

For detailed capability contracts, approval matrices, NAS validation cases, and open-source disclosures, consult the linked references:
- Read [Capability Mapping and Parameter Contracts](references/capability-mapping.md) when reviewing exact CLI domains, actions, effects, and approval boundaries.
- Read [Approval Boundaries and Recovery Matrix](references/approval-and-recovery-matrix.md) when handling state transitions, partial completions, or user confirmation prompts.
- Read [Round 2 Hardware Validation and Test Plan](references/nas-test-plan.md) when executing core test cases and edge cases on UGREEN AI NAS iDX6011 Pro.
- Read [Third-Party Components and AI Tool Disclosures](references/open-source-and-ai-disclosure.md) when auditing hackathon compliance, licenses, and privacy safeguards.

# Required input

Before starting orchestration, confirm the following user-level inputs with the user:
1. **Project theme and creative brief**: Keywords, subject matter, person or object focus, or shooting location for the rough-cut vault.
2. **Time range**: Start date and end date for media and document discovery.
3. **Authorized workspace scope**: The user-designated source folder name and target archive folder name within authorized NAS storage.
4. **Confirmation preference**: Explicit acknowledgement that state-changing operations (album creation, subtitle download, saving the edit decision sheet, file tagging, folder creation, and batch file consolidation) require user or gateway approval before execution.

Do not pre-collect internal expert parameters or guess missing file identifiers. If any required scope input is missing or ambiguous, pause in the `waiting_user` state and ask the user to clarify before delegating. The parent Skill must not call `cli.invoke` directly.

# Generation-time capability evidence

- `ug-photo` → `photo-agent`
- `ug-video` → `media-agent`
- `ug-music` → `media-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `file-workflow` → `file-agent`

# Workflow

Execute the five expert stages sequentially. Each downstream step consumes only the verified real result returned by the upstream expert delegation. Never invent file paths, media identifiers, album identifiers, or transcript text. If any discovery step returns an empty result or zero matches, report the empty result accurately to the user and stop dependent downstream branches without substituting unrelated files.

## Stage 1: Visual Storyboard Discovery and Conditional Album Curation (`photo-agent`)

Delegate visual asset discovery, EXIF/camera metadata inspection, OCR/VLM scene analysis, and conditional storyboard album creation to `photo-agent`:

`delegate --target photo-agent --instruction 'Search authorized photos matching the user project theme, date range, location, and camera metadata using search-picture, meta, vision-ocr, and vision-vlm. If zero matches are found, report an empty result and stop. After returning verified photo items and requesting workflow confirmation, create a conditional project storyboard album via create-album-condition using only verified photo records.'`

## Stage 2: Video Footage, Subtitle Verification, and Reference Soundtrack Pairing (`media-agent`)

Pass the verified project theme and time window to `media-agent` to locate matching video footage, inspect or download matching subtitles, and pair reference soundtrack tracks from the NAS music library:

`delegate --target media-agent --instruction 'Search the NAS video library via ug-video search for footage matching the user project theme and release window, and check available subtitles via subtitle-search. If the user approves downloading a matched subtitle, execute subtitle-download using only the verified video-path and file-id returned by search. Search the NAS music library via ug-music search for reference soundtrack stems matching the project mood and year range without auto-playing unless requested.'`

## Stage 3: Production Brief Extraction and Interview Audio Transcription (`document-agent` and `knowledge-agent`)

Delegate production brief, script, and release form extraction to `document-agent`, and field audio transcription plus Markdown Edit Decision Sheet persistence to `knowledge-agent`:

`delegate --target document-agent --instruction 'Locate and analyze authorized production scripts, shooting briefs, and talent release documents for the project using metadata, extract, qa, and reconcile. Return only verbatim extracted scene cues, deliverable requirements, and reconciliation findings grounded in real documents, or report no results if no matching documents exist.'`

`delegate --target knowledge-agent --instruction 'Transcribe authorized field interview recordings and voice memos for the project using audio-transcription and gather supporting project notes via collect-evidence. Combine the verified upstream photo, video, music, and document results into a structured Markdown Edit Decision Sheet and, after workflow confirmation, persist it using save-text.'`

## Stage 4: Media Technical Inspection, Deduplication, Tagging, and Vault Consolidation (`file-agent`)

Pass the verified asset paths from upstream stages to `file-agent` for technical container inspection, duplicate take scanning, project tagging, and approval-gated directory consolidation:

`delegate --target file-agent --instruction 'Inspect verified project media files using ug-filesystem find, ls, stat, and sha256sum alongside ug-filemgr mediainfo and scan-dedupe to identify duplicate raw takes and verify container codecs. After receiving required gateway or workflow confirmation from the user, apply project tags via ug-filemgr tag-add-file, create the target vault folder via ug-filesystem mkdir, and consolidate only approved non-duplicate selects via file-workflow batch-move.'`

# Completion and failure

Handle every delegation status explicitly and deterministically:
- `completed`: Verify that the child expert returned `ok=true` with real business data before advancing to the next stage or presenting the final rough-cut production summary.
- `waiting_user`: If user input such as project theme, date range, or target folder disambiguation is missing, surface the exact question to the user and pause execution until answered.
- `waiting_approval`: When a stage reaches a state-changing operation (`create-album-condition`, `subtitle-download`, `save-text`, `tag-add-file`, `mkdir`, or `batch-move`), present the exact target items and planned write action to the user and wait for explicit approval before continuing.
- `cancelled`: If the user cancels an approval request or aborts the workflow, halt all remaining stages immediately, preserve any previously completed read-only findings, and report the cancelled status clearly.
- `failed`: If any delegated expert returns `failed`, halt dependent downstream steps immediately, report the exact failure reason and preserve completed upstream read results without fabricating fallback data.

The Skill is complete. You can upload it to [skillhub](https://skills.ugreen.com/skill-hub/publish).
