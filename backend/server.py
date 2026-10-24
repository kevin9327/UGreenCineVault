import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .uliya_engine import (
    WORKSPACE_PRESETS,
    load_catalog_summary,
    run_official_skill_checker,
    run_ugreen_benchmark,
    get_skill_files_bundle,
)
from .mcp_server import MCP_TOOLS, handle_mcp_request

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(
    title="CineVault Studio — UGREEN AI NAS Uliya Skill Orchestrator & Workbench",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_static_bundle() -> dict:
    return {
        "project": "CineVault Studio (cinevault-roughcut-director)",
        "hackathon": "UGREEN Hackathon 2026 on AI NAS ($46,000 Prize Pool)",
        "track": "Unleash Your Creativity",
        "catalog": load_catalog_summary(),
        "checker": run_official_skill_checker(),
        "workspaces": WORKSPACE_PRESETS,
        "benchmark": run_ugreen_benchmark(),
        "skill_files": get_skill_files_bundle(),
        "mcp_tools": MCP_TOOLS,
    }


@app.get("/api/health")
def api_health():
    return {"ok": True, "skill": "cinevault-roughcut-director", "catalogVersion": "2.0.0"}


@app.get("/api/bundle")
def api_bundle():
    return build_static_bundle()


@app.get("/api/check-skill")
def api_check_skill():
    return run_official_skill_checker()


@app.get("/api/orchestrate/{workspace_id}")
def api_orchestrate(workspace_id: str):
    return WORKSPACE_PRESETS.get(workspace_id, WORKSPACE_PRESETS["tokyo-neon-doc-2026"])


@app.get("/api/benchmark")
def api_benchmark():
    return run_ugreen_benchmark()


@app.post("/api/mcp")
async def api_mcp(req: Request):
    body = await req.json()
    return handle_mcp_request(body)


def export_static_bundle():
    api_dir = PUBLIC_DIR / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    bundle = build_static_bundle()
    out_file = api_dir / "static_bundle.json"
    out_file.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_file


if PUBLIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="public")
