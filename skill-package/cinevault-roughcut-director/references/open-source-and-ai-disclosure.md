# Third-Party Components and AI Tool Disclosures

This reference discloses all third-party components, open-source libraries, and AI tools used in the design, validation, and companion simulation studio of `cinevault-roughcut-director` for the **UGREEN Hackathon 2026 on AI NAS**.

## 1. Principal Functionality Developed During the Hackathon

- **`cinevault-roughcut-director` Uliya Orchestration Skill (`SKILL.md` and `references/*.md`)**: Newly authored during the Hackathon Period (October 2026) in strict compliance with the official **UGREEN Uliya Skill Development Standard (`uliya-skill-kit` v0.7.3, `catalogVersion: 2.0.0`)**.
- **5-Expert Cross-Domain Chaining Architecture**: Coordinates `photo-agent` (`ug-photo`), `media-agent` (`ug-video`, `ug-music`), `document-agent` (`ug-document`), `knowledge-agent` (`ug-knowledge`), and `file-agent` (`ug-filesystem`, `ug-filemgr`, `file-workflow`) with deterministic `waiting_approval` gates and empty-result abstention.
- **Companion UGOS AI NAS Interactive Workbench and Static Checker Studio**: A browser-based simulation and validation workbench (`MIT` License) that visualizes the 5-expert delegation pipeline, runs the official `check-skill.mjs` ruleset, and previews timecoded rough-cut edit decision sheets.

## 2. Official UGREEN Packages and Standards Used

| Component | Version | Source | License / Terms | Principal Use |
| :--- | :--- | :--- | :--- | :--- |
| `uliya-skill-kit` | `0.7.3-en` (`catalogVersion 2.0.0`) | Official UGREEN Hackathon Starter Kit | UGREEN Hackathon Official Rules & User Agreement | Capability catalog verification (`capability-catalog.json`) and static validation (`check-skill.mjs`). |

## 3. Open-Source Libraries (Companion Workbench & Verification Suite)

Note: The Pre-test Skill Package ZIP itself is pure Markdown (`SKILL.md` and `references/*.md`) and contains zero external code or binaries. The companion web simulator and test suite in our public repository use:

| Library | Version | Source | License | Principal Use |
| :--- | :--- | :--- | :--- | :--- |
| FastAPI | `0.115+` | `https://pypi.org/project/fastapi/` | MIT License | Companion local API and MCP server simulation for testing NAS skill workflows. |
| Pydantic | `2.9+` | `https://pypi.org/project/pydantic/` | MIT License | Schema validation for simulated Uliya CLI envelopes and capability contracts. |
| Pytest | `8.3+` | `https://pypi.org/project/pytest/` | MIT License | Automated unit testing of capability mappings and static checker compliance. |
| ReportLab | `4.2+` | `https://pypi.org/project/reportlab/` | BSD License | Generating the Round 1 Project Proposal PDF document. |
| HyperFrames | `0.8.192` | `https://github.com/heygen-com/hyperframes` | Apache-2.0 / MIT | Rendering the deterministic 1080p companion demonstration video. |

## 4. AI Tools Disclosure

In accordance with the UGREEN Hackathon Official Rules, the following AI tools were used during development:
- **AI Coding Assistant (Claude / Gemini in Antigravity IDE)**: Used to cross-check `capability-catalog.json` parameter schemas, verify compliance with `check-lib.mjs` diagnostic rules, and assist in writing unit tests for the companion workbench.
- **Google AI Studio (`Gemini 3.8 Flash TTS`)**: Used solely to generate English voiceover narration for the optional companion demonstration video.
- **FlowMusic (`flowmusic.app`)**: Used solely to generate royalty-free background music stems for the companion demonstration video and sample media library fixtures.

## 5. Data Privacy and Security Compliance

- Zero real personal data, private NAS paths, account credentials, or API keys are included in this Skill package.
- All configuration examples and test scenarios use synthetic, anonymized production media fixtures.
- All state-changing operations strictly respect UGREEN UGOS / Uliya platform permissions and `gateway` / `workflow` approval controls.
