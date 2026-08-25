import argparse
import io
import os
import sys
import traceback
import webbrowser
import zipfile

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel

from Agent.graph import agent
from Agent.states import Plan
from Agent.tools import get_project_root, read_file

# ── FastAPI app — this is what the frontend talks to ──────────────────────────

app = FastAPI(title="Forge — AI App Builder API")

# Dev-friendly CORS. Tighten allow_origins to your actual frontend origin
# before deploying this anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Embedded frontend — served directly at http://localhost:8000/ ─────────────
# Kept as one string here so this file has zero dependency on folder layout.
_FRONTEND_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Forge — AI App Builder</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<style>
  :root{
    --bg-void:#0D0F14;
    --bg-panel:#151822;
    --bg-panel-raised:#1C2029;
    --border:#262B37;
    --accent-build:#E8A33D;
    --accent-build-dim:#5A4324;
    --accent-live:#4FD1C5;
    --accent-live-dim:#1F4744;
    --accent-error:#E8615C;
    --text-primary:#ECEEF3;
    --text-muted:#8890A0;
    --text-dim:#4A5061;
    --radius:10px;
  }
  *{box-sizing:border-box;}
  html,body{height:100%;}
  body{
    margin:0;
    background:var(--bg-void);
    color:var(--text-primary);
    font-family:'Inter',sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  .shell{
    display:flex;
    flex-direction:column;
    min-height:100vh;
  }

  /* ---------- header ---------- */
  .topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:16px 24px;
    border-bottom:1px solid var(--border);
    background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent);
  }
  .brand{
    display:flex;
    align-items:baseline;
    gap:10px;
  }
  .brand .mark{
    font-family:'Space Grotesk',sans-serif;
    font-weight:700;
    font-size:19px;
    letter-spacing:0.01em;
  }
  .brand .mark span{color:var(--accent-build);}
  .brand .tagline{
    font-size:12px;
    color:var(--text-dim);
    font-family:'JetBrains Mono',monospace;
  }
  .status-pill{
    display:flex;
    align-items:center;
    gap:8px;
    font-family:'JetBrains Mono',monospace;
    font-size:12px;
    padding:6px 12px;
    border-radius:999px;
    border:1px solid var(--border);
    color:var(--text-muted);
    background:var(--bg-panel);
  }
  .status-dot{
    width:7px;height:7px;border-radius:50%;
    background:var(--text-dim);
    transition:background .3s;
  }
  .status-pill.building .status-dot{background:var(--accent-build);animation:pulse 1.1s ease-in-out infinite;}
  .status-pill.building{color:var(--accent-build);border-color:var(--accent-build-dim);}
  .status-pill.live .status-dot{background:var(--accent-live);}
  .status-pill.live{color:var(--accent-live);border-color:var(--accent-live-dim);}
  .status-pill.error .status-dot{background:var(--accent-error);}
  .status-pill.error{color:var(--accent-error);}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.4;transform:scale(1.3);}}

  /* ---------- layout ---------- */
  .workspace{
    flex:1;
    display:grid;
    grid-template-columns:360px 1fr;
    gap:1px;
    background:var(--border);
    min-height:0;
  }
  @media(max-width:860px){
    .workspace{grid-template-columns:1fr;}
  }

  .rail{
    background:var(--bg-void);
    display:flex;
    flex-direction:column;
    min-height:0;
  }

  .prompt-block{
    padding:20px;
    border-bottom:1px solid var(--border);
  }
  .prompt-block label{
    display:block;
    font-family:'JetBrains Mono',monospace;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.08em;
    color:var(--text-dim);
    margin-bottom:10px;
  }
  textarea{
    width:100%;
    resize:vertical;
    min-height:88px;
    background:var(--bg-panel);
    border:1px solid var(--border);
    border-radius:var(--radius);
    color:var(--text-primary);
    font-family:'Inter',sans-serif;
    font-size:14px;
    padding:12px 14px;
    line-height:1.5;
  }
  textarea:focus{outline:none;border-color:var(--accent-build);}
  textarea::placeholder{color:var(--text-dim);}

  .build-btn{
    margin-top:12px;
    width:100%;
    padding:12px 16px;
    border-radius:var(--radius);
    border:none;
    background:var(--accent-build);
    color:#1A1204;
    font-family:'Space Grotesk',sans-serif;
    font-weight:600;
    font-size:14px;
    cursor:pointer;
    transition:filter .15s, transform .1s;
  }
  .build-btn:hover:not(:disabled){filter:brightness(1.08);}
  .build-btn:active:not(:disabled){transform:scale(.99);}
  .build-btn:disabled{background:var(--bg-panel-raised);color:var(--text-dim);cursor:not-allowed;}
  .hint{
    margin-top:8px;
    font-size:11px;
    color:var(--text-dim);
    font-family:'JetBrains Mono',monospace;
  }
  .backend-row{
    display:flex;
    align-items:center;
    gap:8px;
    margin-bottom:14px;
  }
  .backend-row label{
    font-family:'JetBrains Mono',monospace;
    font-size:10.5px;
    text-transform:uppercase;
    letter-spacing:0.06em;
    color:var(--text-dim);
    flex-shrink:0;
  }
  .backend-row input{
    flex:1;
    background:var(--bg-panel);
    border:1px solid var(--border);
    border-radius:7px;
    color:var(--text-muted);
    font-family:'JetBrains Mono',monospace;
    font-size:12px;
    padding:7px 10px;
  }
  .backend-row input:focus{outline:none;border-color:var(--accent-live);color:var(--text-primary);}

  .console{
    flex:1;
    overflow-y:auto;
    padding:16px 20px 24px;
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px;
    line-height:1.9;
  }
  .console .console-title{
    text-transform:uppercase;
    letter-spacing:0.08em;
    font-size:11px;
    color:var(--text-dim);
    margin-bottom:10px;
  }
  .log-line{
    display:flex;
    gap:8px;
    color:var(--text-muted);
    white-space:pre-wrap;
    word-break:break-word;
  }
  .log-line .tag{color:var(--accent-build);flex-shrink:0;}
  .log-line.ok .tag{color:var(--accent-live);}
  .log-line.err{color:var(--accent-error);}
  .log-line.err .tag{color:var(--accent-error);}
  .log-line.empty{color:var(--text-dim);}

  /* ---------- main panel ---------- */
  .panel{
    background:var(--bg-void);
    display:flex;
    flex-direction:column;
    min-height:0;
  }
  .tabbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    border-bottom:1px solid var(--border);
    padding:0 16px;
  }
  .tabs{display:flex;gap:2px;}
  .tab{
    padding:13px 14px;
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px;
    color:var(--text-dim);
    background:none;
    border:none;
    border-bottom:2px solid transparent;
    cursor:pointer;
  }
  .tab.active{color:var(--text-primary);border-bottom-color:var(--accent-build);}
  .tab:disabled{cursor:not-allowed;opacity:.4;}
  .download-btn{
    display:flex;
    align-items:center;
    gap:6px;
    padding:7px 13px;
    border-radius:7px;
    border:1px solid var(--border);
    background:var(--bg-panel);
    color:var(--text-muted);
    font-family:'Inter',sans-serif;
    font-size:12.5px;
    font-weight:500;
    cursor:pointer;
  }
  .download-btn:hover:not(:disabled){border-color:var(--accent-live);color:var(--accent-live);}
  .download-btn:disabled{opacity:.35;cursor:not-allowed;}

  .view{
    flex:1;
    min-height:0;
    position:relative;
    background:#0A0B0E;
  }
  iframe{
    width:100%;height:100%;border:none;background:#fff;
  }
  .code-view{
    display:none;
    height:100%;
    overflow:auto;
    padding:20px 24px;
  }
  .code-view.active{display:block;}
  .code-view pre{
    margin:0;
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px;
    line-height:1.7;
    color:var(--text-primary);
    white-space:pre-wrap;
    word-break:break-word;
  }

  .empty-state{
    height:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:8px;
    color:var(--text-dim);
    font-family:'JetBrains Mono',monospace;
    font-size:13px;
    text-align:center;
    padding:24px;
  }
  .empty-state .big{
    font-family:'Space Grotesk',sans-serif;
    font-size:15px;
    color:var(--text-muted);
    font-weight:600;
  }
</style>
</head>
<body>

<div class="shell">

  <div class="topbar">
    <div class="brand">
      <div class="mark">FORGE<span>.</span></div>
      <div class="tagline">prompt → plan → code → preview</div>
    </div>
    <div class="status-pill" id="statusPill">
      <div class="status-dot"></div>
      <span id="statusText">idle</span>
    </div>
  </div>

  <div class="workspace">

    <div class="rail">
      <div class="prompt-block">
        <div class="backend-row">
          <label for="backendUrl">backend</label>
          <input type="text" id="backendUrl" value="http://localhost:8000" spellcheck="false">
        </div>
        <label for="promptInput">describe the app you want built</label>
        <textarea id="promptInput" placeholder="e.g. Personal Finance Dashboard with income/expense tracking, categories (Food, Travel, Bills), monthly filters, LocalStorage, dark/light theme, CSV export, and budget warnings"></textarea>
        <button class="build-btn" id="buildBtn">Build app</button>
        <div class="hint">⌘/Ctrl + Enter to build</div>
      </div>
      <div class="console" id="console">
        <div class="console-title">build console</div>
        <div class="log-line empty" id="consoleEmpty">waiting for a prompt…</div>
      </div>
    </div>

    <div class="panel">
      <div class="tabbar">
        <div class="tabs">
          <button class="tab active" data-tab="preview">Preview</button>
          <button class="tab" data-tab="index.html" disabled>index.html</button>
          <button class="tab" data-tab="style.css" disabled>style.css</button>
          <button class="tab" data-tab="script.js" disabled>script.js</button>
        </div>
        <button class="download-btn" id="downloadBtn" disabled>⭳ Download code</button>
      </div>

      <div class="view" id="previewView">
        <div class="empty-state" id="emptyState">
          <div class="big">nothing built yet</div>
          <div>write a prompt on the left and hit "Build app"</div>
        </div>
        <iframe id="previewFrame" style="display:none;"></iframe>
      </div>
      <div class="code-view" id="code-index.html"><pre id="pre-index.html"></pre></div>
      <div class="code-view" id="code-style.css"><pre id="pre-style.css"></pre></div>
      <div class="code-view" id="code-script.js"><pre id="pre-script.js"></pre></div>
    </div>

  </div>
</div>

<script>
const els = {
  backendUrl: document.getElementById('backendUrl'),
  prompt: document.getElementById('promptInput'),
  buildBtn: document.getElementById('buildBtn'),
  consoleEl: document.getElementById('console'),
  consoleEmpty: document.getElementById('consoleEmpty'),
  statusPill: document.getElementById('statusPill'),
  statusText: document.getElementById('statusText'),
  tabs: document.querySelectorAll('.tab'),
  downloadBtn: document.getElementById('downloadBtn'),
  previewFrame: document.getElementById('previewFrame'),
  emptyState: document.getElementById('emptyState'),
};

let files = { 'index.html': '', 'style.css': '', 'script.js': '' };
let planName = 'my_app';

if(window.location.protocol.startsWith('http')){
  els.backendUrl.value = window.location.origin;
}

function setStatus(state, label){
  els.statusPill.className = 'status-pill ' + state;
  els.statusText.textContent = label;
}

function log(tag, text, cls){
  if(els.consoleEmpty) { els.consoleEmpty.remove(); els.consoleEmpty = null; }
  const line = document.createElement('div');
  line.className = 'log-line' + (cls ? ' ' + cls : '');
  line.innerHTML = `<span class="tag">[${tag}]</span><span>${text}</span>`;
  els.consoleEl.appendChild(line);
  els.consoleEl.scrollTop = els.consoleEl.scrollHeight;
  return line;
}

async function callBackend(prompt){
  const base = els.backendUrl.value.trim().replace(/\/$/, '') || 'http://localhost:8000';
  let res;
  try{
    res = await fetch(`${base}/api/build`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
  } catch(e){
    throw new Error(`can't reach backend at ${base} — is main.py running?`);
  }
  if(!res.ok){
    let detail = '';
    try{ detail = (await res.json()).detail || ''; } catch(e){}
    throw new Error(`backend error ${res.status}${detail ? ' — ' + detail : ''}`);
  }
  return res.json();
}

function assemblePreview(html, css, js){
  let out = html;
  if(/<link[^>]+style\.css[^>]*>/i.test(out)){
    out = out.replace(/<link[^>]+style\.css[^>]*>/i, `<style>\n${css}\n</style>`);
  } else if(/<\/head>/i.test(out)){
    out = out.replace(/<\/head>/i, `<style>\n${css}\n</style>\n</head>`);
  } else {
    out = `<style>${css}</style>` + out;
  }
  if(/<script[^>]+script\.js[^>]*><\/script>/i.test(out)){
    out = out.replace(/<script[^>]+script\.js[^>]*><\/script>/i, `<script>\n${js}\n<\/script>`);
  } else if(/<\/body>/i.test(out)){
    out = out.replace(/<\/body>/i, `<script>\n${js}\n<\/script>\n</body>`);
  } else {
    out += `<script>${js}<\/script>`;
  }
  return out;
}

function switchTab(name){
  els.tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  document.getElementById('previewView').style.display = name === 'preview' ? 'block' : 'none';
  ['index.html','style.css','script.js'].forEach(f => {
    document.getElementById('code-' + f).classList.toggle('active', name === f);
  });
}

els.tabs.forEach(t => t.addEventListener('click', () => {
  if(t.disabled) return;
  switchTab(t.dataset.tab);
}));

els.downloadBtn.addEventListener('click', async () => {
  const zip = new JSZip();
  const folder = zip.folder(planName);
  folder.file('index.html', files['index.html']);
  folder.file('style.css', files['style.css']);
  folder.file('script.js', files['script.js']);
  const blob = await zip.generateAsync({ type: 'blob' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${planName}.zip`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

els.prompt.addEventListener('keydown', (e) => {
  if((e.metaKey || e.ctrlKey) && e.key === 'Enter') runBuild();
});
els.buildBtn.addEventListener('click', runBuild);

async function runBuild(){
  const userPrompt = els.prompt.value.trim();
  if(!userPrompt) { els.prompt.focus(); return; }

  els.buildBtn.disabled = true;
  els.tabs.forEach(t => { if(t.dataset.tab !== 'preview') t.disabled = true; });
  els.downloadBtn.disabled = true;
  els.consoleEl.innerHTML = '<div class="console-title">build console</div>';
  els.consoleEmpty = null;
  setStatus('building', 'building');
  switchTab('preview');
  els.emptyState.style.display = 'none';
  els.previewFrame.style.display = 'none';

  try{
    log('planner', 'analyzing user request and planning full architecture...');
    log('pipeline', 'multi-agent pipeline running: Planner -> HTML Architect -> CSS Stylist -> JS Engineer -> Verifier...');

    const data = await callBackend(userPrompt);

    planName = (data.name || 'my_app').toString().trim().replace(/\s+/g,'_').replace(/[^a-z0-9_]/gi,'').toLowerCase() || 'my_app';
    log('planner', `plan ready -> <strong>${planName}</strong> -- ${data.description || ''}`);
    if(data.complexity){
      log('planner', `complexity: <strong>${data.complexity}</strong>`);
    }
    if(data.features && data.features.length){
      log('planner', `${data.features.length} features planned:`);
      data.features.forEach((f, i) => log('planner', `  ${i+1}. ${f}`));
    }

    const html = data.files['index.html'] || '';
    const css  = data.files['style.css'] || '';
    const js   = data.files['script.js'] || '';

    files['index.html'] = html;
    files['style.css']  = css;
    files['script.js']  = js;

    document.getElementById('pre-index.html').textContent = html;
    document.getElementById('pre-style.css').textContent  = css;
    document.getElementById('pre-script.js').textContent  = js;

    log('html', `index.html generated (${html.length} bytes)`);
    document.querySelector('.tab[data-tab="index.html"]').disabled = !html;
    log('css', `style.css generated (${css.length} bytes)`);
    document.querySelector('.tab[data-tab="style.css"]').disabled = !css;
    log('js', `script.js generated (${js.length} bytes)`);
    document.querySelector('.tab[data-tab="script.js"]').disabled = !js;

    log('verifier', `pipeline status: ${data.status}`, data.status === 'DONE' ? 'ok' : 'err');

    log('runtime', 'assembling preview…');
    const assembled = assemblePreview(html, css, js);
    els.previewFrame.srcdoc = assembled;
    els.previewFrame.style.display = 'block';
    els.downloadBtn.disabled = false;

    if(data.status === 'DONE'){
      log('runtime', 'build complete — preview is live', 'ok');
      setStatus('live', 'live');
    } else {
      log('runtime', 'build finished with issues — check the files tabs', 'err');
      setStatus('error', 'partial build');
    }

  } catch(err){
    log('error', err.message || String(err), 'err');
    setStatus('error', 'build failed');
    els.emptyState.style.display = 'flex';
  } finally {
    els.buildBtn.disabled = false;
  }
}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def frontend():
    return _FRONTEND_HTML



class BuildRequest(BaseModel):
    prompt: str
    recursion_limit: int = 50


class BuildResponse(BaseModel):
    name: str
    description: str
    complexity: str = "simple"
    features: list[str] = []
    files: dict[str, str]
    status: str


@app.post("/api/build", response_model=BuildResponse)
def build_app(req: BuildRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(400, "prompt is required")

    try:
        result = agent.invoke(
            {"user_prompt": prompt},
            {"recursion_limit": req.recursion_limit},
        )
    except Exception:
        traceback.print_exc()
        raise HTTPException(500, "agent pipeline failed — see server logs")

    plan: Plan | None = result.get("plan")
    status = result.get("status", "UNKNOWN")

    if plan is None:
        raise HTTPException(500, f"no plan produced — status: {status}")

    files: dict[str, str] = {}
    for f in plan.files:
        # matches the .run(...) call style used in graph.py's coder/verifier nodes
        files[f.path] = read_file.run(f.path)

    # Make sure the three files the frontend expects are always present.
    for required in ("index.html", "style.css", "script.js"):
        files.setdefault(required, "")

    return BuildResponse(
        name=plan.name,
        description=plan.description,
        complexity=plan.complexity,
        features=plan.features,
        files=files,
        status=status,
    )


@app.get("/api/download/{project_name}")
def download_project(project_name: str):
    try:
        root = get_project_root()
    except RuntimeError:
        raise HTTPException(404, "no project has been built yet")

    if root.name != project_name:
        raise HTTPException(404, f"'{project_name}' is not the currently loaded project")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in root.rglob("*"):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(root))
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{project_name}.zip"'},
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}





# ── Original CLI flow — still available with `python main.py --cli` ───────────

def run_cli(recursion_limit: int) -> None:
    try:
        user_prompt = input("Enter your project prompt: ").strip()
        if not user_prompt:
            print("No prompt provided.")
            sys.exit(1)

        print("\n=== Starting App Builder ===\n")
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": recursion_limit},
        )

        plan: Plan | None = result.get("plan")
        status = result.get("status", "unknown")
        print(f"\n=== Pipeline finished -- status: {status} ===\n")

        if plan:
            project_folder = os.path.join(os.getcwd(), plan.name)
            index_html = os.path.join(project_folder, "index.html")
            if os.path.exists(index_html):
                print(f"Opening {index_html} ...")
                webbrowser.open(f"file:///{os.path.abspath(index_html)}")
            else:
                print(f"index.html not found in {project_folder}")
                print("Files present:")
                for f in os.listdir(project_folder):
                    print(f"  {f}")

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="App Builder — generate web apps with AI")
    parser.add_argument(
        "--recursion-limit", "-r",
        type=int, default=50,
        help="LangGraph recursion limit (default: 50).",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the original one-shot terminal flow instead of starting the API server.",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port for the API server (default: 8000).",
    )
    args = parser.parse_args()

    if args.cli:
        run_cli(args.recursion_limit)
        return

    import uvicorn
    port = int(os.environ.get("PORT", args.port))
    print(f"\n=== Forge API server -> http://localhost:{port} ===")
    print("Open your browser at http://localhost:{} and start building!\n".format(port))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()