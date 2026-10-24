# Capability Mapping and Parameter Contracts

This document specifies the exact UGREEN AI NAS capability domains, CLI families, actions, parameters, effects, and approval levels used by `cinevault-roughcut-director`. Every capability listed below is verified against `capability-catalog.json` (`catalogVersion: 2.0.0`).

## 1. Visual Storyboard Domain (`album` via `ug-photo` → `photo-agent`)

| CLI | Action | Effect | Approval | Key Parameters Used | Purpose in Rough-Cut Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-photo` | `search-picture` | `read` | `none` | `location`, `dir`, `file-name-contains`, `ocr-contains`, `start-time`, `end-time`, `camera-model`, `lens-model`, `iso` | Discover candidate still photos and B-roll frames matching shooting dates, location, and camera metadata. |
| `ug-photo` | `meta` | `read` | `none` | `path`, `raw` | Inspect EXIF, lens, focal length, exposure, and capture timestamp metadata on discovered candidate images. |
| `ug-photo` | `vision-ocr` | `read` | `none` | `path` | Read slate boards, clapperboards, and street signage inside discovered images. |
| `ug-photo` | `vision-vlm` | `read` | `none` | `path`, `prompt`, `model`, `max-tokens`, `temperature` | Generate scene composition descriptions and lighting continuity tags for storyboard curation. |
| `ug-photo` | `create-album-condition` | `state-change` | `workflow` | `album-name`, `location`, `dir`, `camera-model`, `ocr-contains`, `start-time`, `end-time` | Create a curated project storyboard album from verified photo matches after workflow confirmation. |

## 2. Video and Music Domain (`media` and `music` via `ug-video`, `ug-music` → `media-agent`)

| CLI | Action | Effect | Approval | Key Parameters Used | Purpose in Rough-Cut Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-video` | `search` | `mixed` | `none` | `type`, `keyword`, `classification`, `video-type`, `release-start`, `release-end`, `limit` | Discover NAS video footage and B-roll clips matching the project keyword and date window without auto-playing. |
| `ug-video` | `subtitle-search` | `read` | `none` | `video-path`, `query`, `season-number`, `episode-number` | Check whether synchronized subtitle tracks exist for discovered project video clips. |
| `ug-video` | `subtitle-download` | `state-change` | `gateway` | `video-path`, `file-id` | Download a matched subtitle track using only verified `video-path` and `file-id` values after gateway approval. |
| `ug-music` | `search` | `mixed` | `none` | `type`, `keyword`, `album-name`, `start-year`, `end-year`, `play` | Search NAS audio stems and reference soundtrack cues by genre, mood keyword, or year range with `play=false`. |

## 3. Production Document Domain (`document` via `ug-document` → `document-agent`)

| CLI | Action | Effect | Approval | Key Parameters Used | Purpose in Rough-Cut Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-document` | `metadata` | `read` | `none` | `file`, `include-pages`, `directory-limit` | Read page count and document headers of scripts, call sheets, and release forms. |
| `ug-document` | `extract` | `read` | `none` | `query`, `file`, `schema`, `content-scope`, `max-files`, `dedupe` | Extract structured scene numbers, required shots, and talent clearance status from real project documents. |
| `ug-document` | `qa` | `read` | `none` | `query`, `file`, `intent`, `answer-mode`, `evidence-mode` | Answer targeted production continuity questions with verbatim document evidence. |
| `ug-document` | `reconcile` | `read` | `none` | `query`, `file`, `max-files` | Cross-check shooting scripts against signed release forms and shot lists to flag missing coverage. |

## 4. Knowledge and Audio Transcription Domain (`knowledge` via `ug-knowledge` → `knowledge-agent`)

| CLI | Action | Effect | Approval | Key Parameters Used | Purpose in Rough-Cut Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-knowledge` | `audio-transcription` | `read` | `none` | `path`, `language`, `speak-count` | Transcribe field interview recordings and director voice notes with speaker separation. |
| `ug-knowledge` | `collect-evidence` | `read` | `none` | `query`, `path`, `extension`, `full` | Aggregate verified text notes and production logs across the workspace. |
| `ug-knowledge` | `save-text` | `state-change` | `workflow` | `path`, `content`, `filename-hint` | Persist the compiled Markdown Rough-Cut Edit Decision Sheet after workflow confirmation. |

## 5. File System and Media Asset Management Domain (`file` via `ug-filesystem`, `ug-filemgr`, `file-workflow` → `file-agent`)

| CLI | Action | Effect | Approval | Key Parameters Used | Purpose in Rough-Cut Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-filesystem` | `find` | `read` | `none` | `path`, `pattern`, `type`, `start-timestamp`, `end-timestamp`, `max-depth`, `limit` | Locate candidate raw footage, audio recordings, and production documents inside the authorized source directory. |
| `ug-filesystem` | `ls` | `read` | `none` | `path`, `recursive`, `max-depth`, `limit` | Enumerate directory structure of the authorized project workspace. |
| `ug-filesystem` | `stat` | `read` | `none` | `path` | Inspect exact byte size and timestamps of candidate media files. |
| `ug-filesystem` | `sha256sum` | `read` | `none` | `path` | Compute cryptographic SHA-256 digests of selected master clips for integrity verification. |
| `ug-filemgr` | `mediainfo` | `read` | `none` | `path` | Read container codec, frame rate, resolution, and audio channel metadata. |
| `ug-filemgr` | `scan-dedupe` | `read` | `none` | `path`, `scope` | Detect duplicate camera card backups and redundant proxy files before archiving. |
| `ug-filemgr` | `tag-add-file` | `state-change` | `conditional` | `path`, `tag-id` | Apply project select tags to verified media files after user confirmation. |
| `ug-filesystem` | `mkdir` | `state-change` | `gateway` | `path`, `parents` | Create the structured destination vault directory after gateway approval. |
| `file-workflow` | `batch-move` | `state-change` | `workflow` | `data`, `actionType`, `sourceDir`, `destination`, `renameBy`, `dateField` | Consolidate approved non-duplicate selects into the destination project vault after workflow approval. |
