# Approval Boundaries and Recovery Matrix

`cinevault-roughcut-director` enforces strict separation between read-only discovery operations and state-changing operations across all five delegated Uliya experts.

## 1. Read-Only vs. Approval-Gated Operations

1. **Read-Only Discovery (No State Change)**:
   - `ug-photo`: `search-picture`, `meta`, `vision-ocr`, `vision-vlm`
   - `ug-video`: `search` (with playback disabled), `subtitle-search`
   - `ug-music`: `search` (with `play=false`)
   - `ug-document`: `metadata`, `extract`, `qa`, `reconcile`
   - `ug-knowledge`: `audio-transcription`, `collect-evidence`
   - `ug-filesystem`: `find`, `ls`, `stat`, `sha256sum`
   - `ug-filemgr`: `mediainfo`, `scan-dedupe`, `tag-list`

2. **State-Changing Operations Requiring Explicit Approval (`waiting_approval`)**:
   - `ug-photo` `create-album-condition` (`approval: workflow`): Presents the album name and matched photo count to the user before creating the storyboard album.
   - `ug-video` `subtitle-download` (`approval: gateway`): Presents the matched video path and subtitle `file-id` before writing subtitle files.
   - `ug-knowledge` `save-text` (`approval: workflow`): Displays a preview of the generated Markdown Edit Decision Sheet and target file name before saving.
   - `ug-filemgr` `tag-add-file` (`approval: conditional`): Lists the exact file paths and tag identifier before tagging.
   - `ug-filesystem` `mkdir` (`approval: gateway`): Confirms the new vault directory path before creation.
   - `file-workflow` `batch-move` (`approval: workflow`): Presents the complete manifest of non-duplicate source files, SHA-256 digests, and destination directory before moving or copying any file.

## 2. Public Delegation Status Handling Matrix

| Delegation Status | Trigger Condition | Orchestrator Action and User Feedback |
| :--- | :--- | :--- |
| `completed` | Delegated expert returns `ok=true` with verified business payload. | Record verified identifiers and paths, then advance to the next stage in the pipeline. |
| `waiting_user` | Required user scope (theme, date window, or workspace folder) is missing or ambiguous. | Pause orchestration immediately and ask the user a concise clarification question. |
| `waiting_approval` | Child expert reaches a gateway, workflow, or conditional write boundary. | Surface the exact items, target location, and impact summary; wait for explicit user approval. |
| `cancelled` | User declines an approval prompt or cancels the active task. | Stop all pending delegations immediately; preserve and display read-only discovery results collected so far. |
| `failed` | Child expert returns `ok=false` or encounters an unreadable file or unsupported format. | Halt dependent downstream delegations, report the exact error diagnostic, and never fabricate replacement paths. |

## 3. Empty-Result and Partial-Result Recovery Rules

- **Zero Visual Matches**: If `photo-agent` or `media-agent` returns zero matches (`empty result`), report that no matching photos or videos were found for the specified theme and date window, and do not invoke `create-album-condition` or `subtitle-download`.
- **Missing Audio or Documents**: If a project workspace contains photos and video clips but zero interview audio files or script documents, mark the corresponding section of the Edit Decision Sheet as "No matching files found in authorized scope" rather than inventing dialogue or script notes.
- **Duplicate File Safety**: When `ug-filemgr` `scan-dedupe` detects duplicate camera takes, `cinevault-roughcut-director` never performs automatic deletion. It reports the duplicate groups in the Edit Decision Sheet and excludes redundant copies from `file-workflow` `batch-move`.
