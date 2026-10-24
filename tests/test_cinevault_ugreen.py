import os
import zipfile
from pathlib import Path
from fastapi.testclient import TestClient

from backend.uliya_engine import (
    load_catalog_summary,
    run_official_skill_checker,
    run_ugreen_benchmark,
    WORKSPACE_PRESETS,
    get_skill_files_bundle,
)
from backend.server import app, export_static_bundle

client = TestClient(app)


def test_official_uliya_skill_checker_static_pass():
    res = run_official_skill_checker()
    assert res["checkFormatVersion"] == "2.0.0"
    assert res["status"] == "static-pass"
    assert res["target"]["skillName"] == "cinevault-roughcut-director"
    assert res["summary"]["errors"] == 0
    assert res["summary"]["warnings"] == 0
    assert res["summary"]["info"] == 0
    assert len(res["files"]) == 5


def test_capability_catalog_contract():
    cat = load_catalog_summary()
    assert cat["catalogVersion"] == "2.0.0"
    assert cat["cli_count"] == 9
    assert cat["agent_count"] == 6
    assert cat["total_actions"] >= 55


def test_orchestration_workspaces_and_zero_match_edge_case():
    tokyo = WORKSPACE_PRESETS["tokyo-neon-doc-2026"]
    assert tokyo["status"] == "completed"
    assert len(tokyo["delegations"]) == 4
    assert "Tokyo Neon" in tokyo["eds_markdown"]

    edge = WORKSPACE_PRESETS["zero-match-edge-2030"]
    assert edge["status"] == "abstained_empty_result"
    assert edge["delegations"][0]["verified_outputs"]["matched_photos"] == 0


def test_benchmark_metrics():
    bm = run_ugreen_benchmark()
    assert bm["scenarios_count"] == 12
    assert bm["summary"]["cinevault_catalog_compliance_pct"] == 100.0
    assert bm["summary"]["cinevault_unapproved_write_leak_pct"] == 0.0
    assert bm["summary"]["cinevault_dedupe_sha256_recall_pct"] == 100.0


def test_round1_pdf_and_zip_deliverables():
    base = Path(__file__).resolve().parent.parent
    pdf_file = base / "dist" / "CineVault_UGREEN_Round1_Proposal.pdf"
    zip_file = base / "dist" / "cinevault-roughcut-director.zip"
    assert pdf_file.exists() and pdf_file.stat().st_size < 1024 * 1024
    assert zip_file.exists() and zip_file.stat().st_size < 10 * 1024 * 1024
    with zipfile.ZipFile(zip_file, "r") as zf:
        names = zf.namelist()
        assert "cinevault-roughcut-director/SKILL.md" in names
        assert len(names) == 5


def test_fastapi_and_mcp_endpoints():
    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    assert r_health.json()["ok"] is True

    r_mcp = client.post("/api/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert r_mcp.status_code == 200
    tools = r_mcp.json()["result"]["tools"]
    assert len(tools) == 6

    r_call = client.post(
        "/api/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "uliya_check_skill_package", "arguments": {}}
        }
    )
    assert r_call.status_code == 200
    check_payload = r_call.json()["result"]["content"][0]["json"]
    assert check_payload["status"] == "static-pass"

    out_bundle = export_static_bundle()
    assert out_bundle.exists()
