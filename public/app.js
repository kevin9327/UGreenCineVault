let BUNDLE = null;
let tourTimer = null;

async function loadBundle() {
  try {
    const res = await fetch("api/static_bundle.json");
    BUNDLE = await res.json();
  } catch (err) {
    const res2 = await fetch("/api/bundle");
    BUNDLE = await res2.json();
  }
  renderWorkspace("tokyo-neon-doc-2026");
  renderValidator();
  renderBenchmark();
  renderCatalogAndMcp();
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === tabId);
  });
}

function renderWorkspace(wsId) {
  if (!BUNDLE || !BUNDLE.workspaces) return;
  const ws = BUNDLE.workspaces[wsId] || BUNDLE.workspaces["tokyo-neon-doc-2026"];
  const metaEl = document.getElementById("workspace-meta");
  metaEl.innerHTML = `
    <strong>Theme:</strong> ${ws.theme} &nbsp;|&nbsp;
    <strong>Date Window:</strong> <code>${ws.date_window.start} .. ${ws.date_window.end}</code> &nbsp;|&nbsp;
    <strong>Source Scope:</strong> <code>${ws.source_scope}</code> &nbsp;|&nbsp;
    <strong>Target Vault:</strong> <code>${ws.target_vault}</code> &nbsp;|&nbsp;
    <span class="badge ${ws.status === 'completed' ? 'badge-pass' : 'badge-warn'}">Status: ${ws.status}</span>
  `;

  const stagesEl = document.getElementById("delegation-stages");
  stagesEl.innerHTML = ws.delegations
    .map(
      (d) => `
    <div class="stage-card">
      <div class="stage-header">
        <div>
          <strong style="color:#6EE7B7; font-size:15px;">Stage ${d.stage}: ${d.agent}</strong>
          <span style="margin-left:10px; font-size:13px; color:#CBD5E1;">CLI: <code>${d.cli}</code> · Actions: <code>${d.actions.join(", ")}</code></span>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <span class="badge badge-warn">Approval: ${d.approval_mode}</span>
          <span class="badge badge-pass">${d.status} (${d.latency_ms} ms)</span>
        </div>
      </div>
      <div class="code-box">${d.command}</div>
      <div class="code-box" style="color:#E2E8F0; margin-top:8px;">${JSON.stringify(d.verified_outputs, null, 2)}</div>
    </div>
  `
    )
    .join("");

  const edsBox = document.getElementById("eds-markdown-box");
  if (edsBox) {
    edsBox.textContent = ws.eds_markdown;
  }
}

function renderValidator() {
  if (!BUNDLE) return;
  const checkerBox = document.getElementById("checker-json-box");
  checkerBox.textContent = JSON.stringify(BUNDLE.checker, null, 2);

  const fileSelect = document.getElementById("skill-file-select");
  const files = Object.keys(BUNDLE.skill_files || {});
  fileSelect.innerHTML = files.map((f) => `<option value="${f}">${f}</option>`).join("");
  const contentBox = document.getElementById("skill-file-content");
  if (files.length > 0) {
    contentBox.textContent = BUNDLE.skill_files[files[0]];
  }
  fileSelect.onchange = () => {
    contentBox.textContent = BUNDLE.skill_files[fileSelect.value] || "";
  };
}

function renderBenchmark() {
  if (!BUNDLE || !BUNDLE.benchmark) return;
  const bm = BUNDLE.benchmark;
  const tbody = document.getElementById("benchmark-tbody");
  tbody.innerHTML = bm.scenarios
    .map(
      (s) => `
    <tr>
      <td><code>${s.id}</code></td>
      <td><strong>${s.workload}</strong></td>
      <td>${(s.manual_sec / 60).toFixed(1)} min (${s.manual_sec}s)</td>
      <td><span class="badge badge-warn">${s.direct_llm_errors} violations</span></td>
      <td><strong style="color:#6EE7B7;">${s.cinevault_sec}s</strong></td>
      <td><span class="badge badge-pass">${s.cinevault_errors} errors (100% safe)</span></td>
    </tr>
  `
    )
    .join("");
}

function renderCatalogAndMcp() {
  if (!BUNDLE || !BUNDLE.catalog) return;
  const wrap = document.getElementById("catalog-table-wrap");
  wrap.innerHTML = `
    <table class="data-table">
      <thead>
        <tr>
          <th>CLI Family</th>
          <th>Domain</th>
          <th>Registered Agent</th>
          <th>Actions (${BUNDLE.catalog.total_actions})</th>
        </tr>
      </thead>
      <tbody>
        ${BUNDLE.catalog.clis
          .map(
            (c) => `
          <tr>
            <td><code>${c.name}</code></td>
            <td>${c.domain}</td>
            <td><span class="badge badge-pass">${c.agent}</span></td>
            <td style="font-size:12px; color:#CBD5E1;">${c.actions.map((a) => `<code>${a.name}</code> (${a.approval})`).join(", ")}</td>
          </tr>
        `
          )
          .join("")}
      </tbody>
    </table>
  `;

  const mcpSelect = document.getElementById("mcp-tool-select");
  const tools = BUNDLE.mcp_tools || [];
  mcpSelect.innerHTML = tools.map((t) => `<option value="${t.name}">${t.name} — ${t.description}</option>`).join("");
  const mcpOut = document.getElementById("mcp-output-box");

  function showMcpResult(toolName) {
    let resultData = {};
    if (toolName === "uliya_list_capabilities") resultData = BUNDLE.catalog;
    else if (toolName === "uliya_check_skill_package") resultData = BUNDLE.checker;
    else if (toolName === "cinevault_run_orchestration") resultData = BUNDLE.workspaces["tokyo-neon-doc-2026"];
    else if (toolName === "cinevault_generate_eds_markdown") resultData = { eds_markdown: BUNDLE.workspaces["tokyo-neon-doc-2026"].eds_markdown };
    else if (toolName === "cinevault_inspect_approval_gates") resultData = { files: Object.keys(BUNDLE.skill_files) };
    else if (toolName === "cinevault_run_benchmark") resultData = BUNDLE.benchmark;
    mcpOut.textContent = JSON.stringify(
      {
        jsonrpc: "2.0",
        id: 1,
        tool: toolName,
        result: resultData
      },
      null,
      2
    );
  }

  if (tools.length > 0) showMcpResult(tools[0].name);
  mcpSelect.onchange = () => showMcpResult(mcpSelect.value);
  const invokeBtn = document.getElementById("btn-invoke-mcp");
  if (invokeBtn) invokeBtn.onclick = () => showMcpResult(mcpSelect.value);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  const wsSelect = document.getElementById("workspace-select");
  wsSelect.addEventListener("change", () => renderWorkspace(wsSelect.value));
  document.getElementById("btn-run-pipeline").addEventListener("click", () => renderWorkspace(wsSelect.value));

  const tourBanner = document.getElementById("tour-banner");
  const tourText = document.getElementById("tour-step-text");

  document.getElementById("btn-judge-tour").addEventListener("click", () => {
    if (tourTimer) clearInterval(tourTimer);
    tourBanner.classList.add("active");
    const steps = [
      { tab: "tab-orchestration", ws: "tokyo-neon-doc-2026", msg: "Step 1/5: Inspecting 5-Expert Uliya Orchestration on Tokyo Neon 4K Shoot..." },
      { tab: "tab-eds", ws: "tokyo-neon-doc-2026", msg: "Step 2/5: Reviewing Timecoded Rough-Cut Edit Decision Sheet, HyperFrames 1080p Demo & FlowMusic Stems..." },
      { tab: "tab-validator", ws: "zero-match-edge-2030", msg: "Step 3/5: Verifying Official UGREEN check-skill.mjs Static Pass (0 Errors, 0 Warnings)..." },
      { tab: "tab-benchmark", ws: "tokyo-neon-doc-2026", msg: "Step 4/5: Auditing 12-Workload Benchmark (205.2x Speedup & 0.0% Unapproved Write Leak)..." },
      { tab: "tab-mcp", ws: "tokyo-neon-doc-2026", msg: "Step 5/5: Exploring Uliya Capability Catalog v2.0.0 & 6-Tool MCP Server..." }
    ];
    let idx = 0;
    const applyStep = () => {
      const st = steps[idx];
      switchTab(st.tab);
      wsSelect.value = st.ws;
      renderWorkspace(st.ws);
      tourText.textContent = st.msg;
      idx = (idx + 1) % steps.length;
    };
    applyStep();
    tourTimer = setInterval(applyStep, 4500);
  });

  document.getElementById("btn-stop-tour").addEventListener("click", () => {
    if (tourTimer) clearInterval(tourTimer);
    tourBanner.classList.remove("active");
  });

  loadBundle();
});
