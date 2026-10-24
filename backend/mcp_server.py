from typing import Any, Dict, List
from .uliya_engine import (
    WORKSPACE_PRESETS,
    load_catalog_summary,
    run_official_skill_checker,
    run_ugreen_benchmark,
    get_skill_files_bundle,
)

MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "uliya_list_capabilities",
        "description": "List all 9 UGREEN AI NAS CLI capability families, 6 registered full-profile expert agents, and 55+ actions from capability-catalog.json v2.0.0.",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "uliya_check_skill_package",
        "description": "Execute the official UGREEN Uliya check-skill.mjs (v2.0.0) static validator on cinevault-roughcut-director and return SHA-256 file digests and diagnostics.",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "cinevault_run_orchestration",
        "description": "Run the 5-stage cinevault-roughcut-director expert delegation workflow on an authorized NAS workspace preset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_id": {
                    "type": "string",
                    "enum": ["tokyo-neon-doc-2026", "alpine-brand-film-2026", "zero-match-edge-2030"]
                }
            },
            "required": ["workspace_id"]
        }
    },
    {
        "name": "cinevault_generate_eds_markdown",
        "description": "Generate the timecoded Markdown Rough-Cut Edit Decision Sheet (EDS) with OCR/VLM storyboard tags, subtitle sync, FlowMusic stems, and SHA-256 deduplication manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {"workspace_id": {"type": "string"}},
            "required": ["workspace_id"]
        }
    },
    {
        "name": "cinevault_inspect_approval_gates",
        "description": "Return the read-only vs. waiting_approval boundary matrix for all 8 Uliya CLIs used by cinevault-roughcut-director.",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "cinevault_run_benchmark",
        "description": "Run the 12-scenario quantitative benchmark comparing CineVault Uliya 5-Expert Orchestration vs. Direct-CLI LLM vs. Manual UGOS 5-App Switching.",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    }
]


def handle_mcp_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    method = payload.get("method", "tools/list")
    req_id = payload.get("id", 1)
    params = payload.get("params", {}) or {}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name == "uliya_list_capabilities":
            data = load_catalog_summary()
        elif name == "uliya_check_skill_package":
            data = run_official_skill_checker()
        elif name == "cinevault_run_orchestration":
            ws_id = args.get("workspace_id", "tokyo-neon-doc-2026")
            data = WORKSPACE_PRESETS.get(ws_id, WORKSPACE_PRESETS["tokyo-neon-doc-2026"])
        elif name == "cinevault_generate_eds_markdown":
            ws_id = args.get("workspace_id", "tokyo-neon-doc-2026")
            ws = WORKSPACE_PRESETS.get(ws_id, WORKSPACE_PRESETS["tokyo-neon-doc-2026"])
            data = {"workspace_id": ws_id, "eds_markdown": ws["eds_markdown"]}
        elif name == "cinevault_inspect_approval_gates":
            data = {"files": get_skill_files_bundle()}
        elif name == "cinevault_run_benchmark":
            data = run_ugreen_benchmark()
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {name}"}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "json", "json": data}]}}

    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ok", "tools_count": len(MCP_TOOLS)}}
