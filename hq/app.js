// Kaizen XP HQ: the 3D office and the live progress panel.
// Live mode reads /api/events (what hook.py logs) and /api/progress (what
// server.py works out from the project files). Add ?demo to the address to
// watch made-up activity instead.
import * as THREE from 'three';
import { OrbitControls } from './vendor/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from './vendor/CSS2DRenderer.js';

const GOLD = 0xc9a84c, BLACK = 0x0d0d0d, CREAM = 0xf3efe4;
const STATE_COLOUR = { idle: 0x3a3a3a, working: GOLD, waiting: 0xe8a33d, done: 0x5fbf77 };
const DONE_FOR_MS = 90_000;      // a finished agent shows green this long
const STALE_MS = 10 * 60_000;    // no news for this long means it stopped

// Desk positions follow the plan's three waves: wave 1 in the middle,
// wave 2 on the left, wave 3 on the right. The main session sits in front.
const TEAM = [
  { name: 'coordinator', title: 'Coordinator', wave: 1, pos: [0, -1.5], tint: 0xc9a84c },
  { name: 'shop-analyst', title: 'Shop Analyst', wave: 1, pos: [-5.5, 0], tint: 0x6f9fd8 },
  { name: 'product-qa', title: 'Product QA', wave: 1, pos: [5.5, 0], tint: 0x5fbf77 },
  { name: 'ci-challenger', title: 'CI Challenger', wave: 1, pos: [-3.5, -5.5], tint: 0xe0654f },
  { name: 'usability-checker', title: 'Usability Checker', wave: 1, pos: [3.5, -5.5], tint: 0xb07fd6 },
  { name: 'listing-optimiser', title: 'Listing Optimiser', wave: 2, pos: [-12, -3.5], tint: 0xe8a33d },
  { name: 'customer-care', title: 'Customer Care', wave: 2, pos: [-12, 2.5], tint: 0xe58fb0 },
  { name: 'market-scout', title: 'Market Scout', wave: 3, pos: [12, -5], tint: 0x4fc1c1 },
  { name: 'product-builder', title: 'Product Builder', wave: 3, pos: [12, 0], tint: 0xd8c27a },
  { name: 'traffic-planner', title: 'Traffic Planner', wave: 3, pos: [12, 5], tint: 0x8fc85a },
];
const MAIN = { name: 'main', title: 'Main session (Josh)', wave: 0, pos: [0, 5.5], tint: CREAM };
const BY_NAME = Object.fromEntries([...TEAM, MAIN].map(a => [a.name, a]));

const params = new URLSearchParams(location.search);
const DEMO = params.has('demo');

// ---------- state ----------
for (const a of [...TEAM, MAIN]) {
  Object.assign(a, { state: 'idle', activity: 'Idle', since: 0, lastSeen: 0, steps: 0, runs: 0,
    expected: loadExpected(a.name), outputs: 0, lastOutput: null, ids: new Set() });
}
const counters = { tools: 0, files: 0 };
let selected = null;

function loadExpected(name) {
  try { return Number(localStorage.getItem('hq-steps-' + name)) || 15; } catch { return 15; }
}
function saveExpected(a) {
  try { localStorage.setItem('hq-steps-' + a.name, String(Math.round(a.expected))); } catch { /* private mode */ }
}

// ---------- scene ----------
const stage = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.prepend(renderer.domElement);

const labels = new CSS2DRenderer({ element: document.getElementById('labels') });

const scene = new THREE.Scene();
scene.background = new THREE.Color(BLACK);
scene.fog = new THREE.Fog(BLACK, 60, 120);

const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200);
camera.position.set(0, 17, 25);
const controls = new OrbitControls(camera, renderer.domElement);
let userMoved = false;
controls.addEventListener('start', () => { userMoved = true; });
controls.target.set(0, 0, -0.5);
controls.enableDamping = true;
controls.maxPolarAngle = Math.PI * 0.47;
controls.minDistance = 6;
controls.maxDistance = 90;
controls.autoRotate = false;

scene.add(new THREE.HemisphereLight(0xfff4dc, 0x101010, 0.55));
const sun = new THREE.DirectionalLight(0xffffff, 1.1);
sun.position.set(8, 20, 12);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -22, right: 22, top: 16, bottom: -16 });
scene.add(sun);

// Floor, zones and the back wall.
const floor = new THREE.Mesh(new THREE.PlaneGeometry(38, 24),
  new THREE.MeshStandardMaterial({ color: 0x141414, roughness: 0.9 }));
floor.rotation.x = -Math.PI / 2;
floor.position.z = 0.5;
floor.receiveShadow = true;
scene.add(floor);
const grid = new THREE.GridHelper(38, 38, 0x2b2615, 0x1d1b14);
grid.position.set(0, 0.002, 0.5);
scene.add(grid);

function zone(x, w, text) {
  const strip = new THREE.Mesh(new THREE.PlaneGeometry(w - 0.6, 0.08),
    new THREE.MeshBasicMaterial({ color: GOLD, transparent: true, opacity: 0.5 }));
  strip.rotation.x = -Math.PI / 2;
  strip.position.set(x, 0.01, 11.6);
  scene.add(strip);
  const el = document.createElement('div');
  el.className = 'zone';
  el.textContent = text;
  const lab = new CSS2DObject(el);
  lab.position.set(x, 0.1, 12.2);
  scene.add(lab);
}
zone(-13, 8, 'WAVE 2  ·  LISTINGS AND CARE');
zone(0, 18, 'WAVE 1  ·  MEASURE AND CHECK');
zone(13, 8, 'WAVE 3  ·  GROW');

function textCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

const wallCanvas = textCanvas(1024, 256);
const wallTex = new THREE.CanvasTexture(wallCanvas);
wallTex.colorSpace = THREE.SRGBColorSpace;
const wall = new THREE.Mesh(new THREE.BoxGeometry(38, 6, 0.3),
  new THREE.MeshStandardMaterial({ color: 0x101010, roughness: 1 }));
wall.position.set(0, 3, -11.5);
wall.receiveShadow = true;
scene.add(wall);
const board = new THREE.Mesh(new THREE.PlaneGeometry(16, 4),
  new THREE.MeshBasicMaterial({ map: wallTex }));
board.position.set(0, 3.4, -11.3);
scene.add(board);

function drawWall(p) {
  const g = wallCanvas.getContext('2d');
  g.fillStyle = '#0d0d0d'; g.fillRect(0, 0, 1024, 256);
  g.strokeStyle = '#c9a84c'; g.lineWidth = 4; g.strokeRect(6, 6, 1012, 244);
  g.fillStyle = '#c9a84c'; g.font = 'bold 54px Helvetica, Arial'; g.textAlign = 'left';
  g.fillText('KAIZEN XP', 40, 84);
  g.fillStyle = '#8d8a82'; g.font = '22px Helvetica, Arial';
  g.fillText('Measure. Change one thing. Check. Standardise.', 40, 122);
  const working = TEAM.filter(a => a.state === 'working').length;
  const stats = [
    [String(working), 'working now'],
    [p ? String(openIssues(p)) : '-', 'open issues'],
    [p ? String(p.decisions.logged) : '-', 'decisions logged'],
    [p ? String(reportsCount(p)) : '-', 'agent outputs'],
  ];
  stats.forEach(([v, l], i) => {
    const x = 40 + i * 245;
    g.fillStyle = '#f3efe4'; g.font = 'bold 56px Helvetica, Arial'; g.fillText(v, x, 200);
    g.fillStyle = '#8d8a82'; g.font = '20px Helvetica, Arial'; g.fillText(l, x, 232);
  });
  wallTex.needsUpdate = true;
}

// ---------- desks and agents ----------
const pickables = [];
const deskMat = new THREE.MeshStandardMaterial({ color: 0x1c1c1c, roughness: 0.6, metalness: 0.2 });
const trimMat = new THREE.MeshStandardMaterial({ color: GOLD, roughness: 0.35, metalness: 0.8 });

function buildDesk(a) {
  const g = new THREE.Group();
  g.position.set(a.pos[0], 0, a.pos[1]);
  scene.add(g);

  const top = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.1, 1.3), deskMat);
  top.position.y = 0.78; top.castShadow = true; top.receiveShadow = true;
  g.add(top);
  const edge = new THREE.Mesh(new THREE.BoxGeometry(2.62, 0.03, 0.03), trimMat);
  edge.position.set(0, 0.8, 0.66);
  g.add(edge);
  for (const [x, z] of [[-1.2, -0.55], [1.2, -0.55], [-1.2, 0.55], [1.2, 0.55]]) {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.78, 0.07), deskMat);
    leg.position.set(x, 0.39, z); leg.castShadow = true;
    g.add(leg);
  }

  // Monitor with a live screen texture.
  const canvas = textCanvas(256, 144);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  const frame = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.8, 0.06), deskMat);
  frame.position.set(0, 1.35, -0.4); frame.castShadow = true;
  g.add(frame);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.68),
    new THREE.MeshBasicMaterial({ map: tex }));
  screen.position.set(0, 1.35, -0.365);
  g.add(screen);
  const stand = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.2, 0.08), deskMat);
  stand.position.set(0, 0.92, -0.4);
  g.add(stand);

  // The agent: a small figure on the camera side of the desk, facing its screen.
  const body = new THREE.Group();
  body.position.set(0, 0, 1.05);
  g.add(body);
  const suit = new THREE.MeshStandardMaterial({ color: a.tint, roughness: 0.5, metalness: 0.1 });
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.28, 0.42, 6, 16), suit);
  torso.position.y = 0.98; torso.castShadow = true;
  body.add(torso);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.24, 20, 16),
    new THREE.MeshStandardMaterial({ color: 0x1a1a1a, roughness: 0.3, metalness: 0.5 }));
  head.position.y = 1.62; head.castShadow = true;
  body.add(head);
  const lampMat = new THREE.MeshBasicMaterial({ color: STATE_COLOUR.idle });
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 10), lampMat);
  lamp.position.y = 1.92;
  body.add(lamp);
  const arms = [];
  for (const side of [-1, 1]) {
    const arm = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.38, 4, 8), suit);
    arm.position.set(side * 0.34, 1.0, -0.22);
    arm.rotation.x = -1.1;
    arm.castShadow = true;
    body.add(arm);
    arms.push(arm);
  }
  const seat = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.08, 20), deskMat);
  seat.position.set(0, 0.55, 0.05);
  body.add(seat);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.55, 8), deskMat);
  post.position.set(0, 0.27, 0.05);
  body.add(post);

  // A ring that spins over the agent while it works.
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.025, 8, 40),
    new THREE.MeshBasicMaterial({ color: GOLD, transparent: true, opacity: 0.9 }));
  ring.rotation.x = Math.PI / 2;
  ring.position.y = 2.2;
  ring.visible = false;
  body.add(ring);

  const glow = new THREE.PointLight(GOLD, 0, 4.5);
  glow.position.set(0, 1.5, 0.2);
  g.add(glow);

  const el = document.createElement('div');
  el.className = 'tag idle';
  el.innerHTML = `<b></b><span></span>`;
  el.querySelector('b').textContent = a.title;
  el.addEventListener('click', () => select(a.name));
  const tag = new CSS2DObject(el);
  tag.position.set(0, 2.75, 0.6);
  g.add(tag);

  for (const m of [torso, head, top, frame]) { m.userData.agent = a.name; pickables.push(m); }
  a.view = { g, body, torso, arms, lamp, ring, glow, canvas, tex, el };
  drawScreen(a);
}

function buildMain(a) {
  const g = new THREE.Group();
  g.position.set(a.pos[0], 0, a.pos[1]);
  scene.add(g);
  const table = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.6, 0.8, 40), deskMat);
  table.position.y = 0.4; table.castShadow = true; table.receiveShadow = true;
  g.add(table);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.04, 8, 60), trimMat);
  rim.rotation.x = Math.PI / 2; rim.position.y = 0.8;
  g.add(rim);
  const holo = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 1),
    new THREE.MeshBasicMaterial({ color: GOLD, wireframe: true, transparent: true, opacity: 0.8 }));
  holo.position.y = 1.7;
  g.add(holo);
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 10),
    new THREE.MeshBasicMaterial({ color: STATE_COLOUR.idle }));
  lamp.position.y = 1.7;
  g.add(lamp);
  const glow = new THREE.PointLight(GOLD, 0, 6);
  glow.position.set(0, 1.8, 0);
  g.add(glow);
  const el = document.createElement('div');
  el.className = 'tag idle';
  el.innerHTML = `<b></b><span></span>`;
  el.querySelector('b').textContent = a.title;
  el.addEventListener('click', () => select(a.name));
  const tag = new CSS2DObject(el);
  tag.position.set(0, 2.8, 0);
  g.add(tag);
  table.userData.agent = a.name; pickables.push(table);
  a.view = { g, holo, lamp, glow, el, main: true };
}

TEAM.forEach(buildDesk);
buildMain(MAIN);

function drawScreen(a) {
  const { canvas, tex } = a.view;
  if (!canvas) return;
  const g = canvas.getContext('2d');
  const s = a.state;
  g.fillStyle = s === 'working' ? '#1d1708' : '#0a0a0a';
  g.fillRect(0, 0, 256, 144);
  g.fillStyle = '#' + STATE_COLOUR[s].toString(16).padStart(6, '0');
  g.fillRect(0, 0, 256, 6);
  g.font = 'bold 22px Helvetica, Arial';
  g.fillText({ idle: 'IDLE', working: 'WORKING', waiting: 'NEEDS JOSH', done: 'DONE' }[s], 14, 40);
  g.fillStyle = '#f3efe4';
  g.font = '16px Helvetica, Arial';
  wrap(g, a.activity, 14, 70, 228, 20, 3);
  if (s === 'working') {
    g.fillStyle = '#c9a84c';
    g.fillRect(14, 128, Math.min(228, 228 * progressOf(a)), 6);
  }
  tex.needsUpdate = true;
}

function wrap(g, text, x, y, w, lh, max) {
  const words = String(text).split(' ');
  let line = '', n = 0;
  for (const word of words) {
    const test = line ? line + ' ' + word : word;
    if (g.measureText(test).width > w && line) {
      g.fillText(line, x, y + n * lh);
      line = word;
      if (++n >= max) return;
    } else line = test;
  }
  if (line) g.fillText(line, x, y + n * lh);
}

// ---------- hand-off packets ----------
const packets = [];
function sendPacket(from, to) {
  const a = BY_NAME[from], b = BY_NAME[to];
  if (!a || !b || a === b) return;
  const start = new THREE.Vector3(a.pos[0], 1.8, a.pos[1]);
  const end = new THREE.Vector3(b.pos[0], 1.8, b.pos[1] + 1);
  const mid = start.clone().lerp(end, 0.5);
  mid.y += 3 + start.distanceTo(end) * 0.15;
  const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
  const orb = new THREE.Mesh(new THREE.SphereGeometry(0.16, 14, 12), new THREE.MeshBasicMaterial({ color: GOLD }));
  const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(curve.getPoints(40)),
    new THREE.LineBasicMaterial({ color: GOLD, transparent: true, opacity: 0.35 }));
  scene.add(orb, line);
  packets.push({ curve, orb, line, t: 0 });
}

// ---------- state changes ----------
function setState(a, state, activity, now) {
  if (!a) return;
  if (state === 'working' && a.state !== 'working') { a.steps = 0; a.since = now; }
  if (state === 'done' && a.state === 'working' && a.steps > 2) {
    a.runs += 1;
    a.expected = a.expected * 0.6 + a.steps * 0.4;   // learns how long a run usually takes
    saveExpected(a);
  }
  a.state = state;
  if (activity) a.activity = activity;
  a.lastSeen = now;
  refreshAgent(a);
}

function progressOf(a) {
  if (a.state === 'done') return 1;
  if (a.state !== 'working') return 0;
  return Math.min(0.95, a.steps / Math.max(4, a.expected));
}

function refreshAgent(a) {
  const v = a.view;
  if (!v) return;
  const c = STATE_COLOUR[a.state];
  v.lamp.material.color.setHex(c);
  v.glow.color.setHex(c);
  v.glow.intensity = a.state === 'idle' ? 0 : 6;
  if (v.ring) v.ring.visible = a.state === 'working';
  v.el.className = 'tag ' + a.state;
  v.el.querySelector('span').textContent = a.activity;
  drawScreen(a);
  renderRow(a);
}

// Which agent did this? Newer Claude Code versions say so in the hook data.
// If not, a tool call made while a specialist is running is that specialist's.
function whoDid(ev) {
  if (ev.agent && BY_NAME[ev.agent]) return BY_NAME[ev.agent];
  if (ev.agent_id) {
    const a = TEAM.find(t => t.ids.has(ev.agent_id));
    if (a) return a;
  }
  const busy = TEAM.filter(t => t.state === 'working').sort((x, y) => y.since - x.since);
  return busy[0] || MAIN;
}

const VERB = { Read: 'Reading', Write: 'Writing', Edit: 'Editing', MultiEdit: 'Editing', Glob: 'Finding files',
  Grep: 'Searching', Bash: '', WebSearch: 'Searching the web', WebFetch: 'Reading a web page',
  TodoWrite: 'Planning steps', NotebookEdit: 'Editing' };

function handle(ev) {
  const now = ev.ts * 1000;
  const live = !ev.replay;
  const isHandOff = ev.tool === 'Task' || ev.tool === 'Agent';
  switch (ev.event) {
    case 'SessionStart':
      if (live) feed(now, MAIN, 'Session started');
      setState(MAIN, 'idle', 'Ready', now);
      break;
    case 'UserPromptSubmit':
      setState(MAIN, 'working', 'Working on your request', now);
      if (live) feed(now, MAIN, 'Josh gave the team a job');
      break;
    case 'SubagentStart': {
      const a = BY_NAME[ev.agent];
      if (a && a !== MAIN) {
        if (ev.agent_id) a.ids.add(ev.agent_id);
        if (a.state !== 'working') setState(a, 'working', 'Starting up', now);
      }
      break;
    }
    case 'PreToolUse': {
      const who = whoDid(ev);
      if (isHandOff && BY_NAME[ev.target]) {
        const to = BY_NAME[ev.target];
        if (live) sendPacket(who.name, to.name);
        setState(to, 'working', ev.label || 'Starting up', now);
        if (live) feed(now, who, `handed work to <b>${esc(to.title)}</b>${ev.label ? ': ' + esc(ev.label) : ''}`);
        break;
      }
      counters.tools += 1;
      who.steps += 1;
      const verb = VERB[ev.tool] ?? ev.tool;
      const text = [verb, ev.label].filter(Boolean).join(' ') || ev.tool;
      setState(who, 'working', text, now);
      if (live && who !== MAIN) feed(now, who, esc(text));
      break;
    }
    case 'PostToolUse': {
      if (isHandOff && BY_NAME[ev.target]) {
        const a = BY_NAME[ev.target];
        if (a.state === 'working') setState(a, 'done', 'Finished: ' + (ev.label || 'job done'), now);
        break;
      }
      if (ev.path) {
        counters.files += 1;
        const who = whoDid(ev);
        if (live) {
          feed(now, who, `wrote <b>${esc(ev.path)}</b>`);
          scheduleProgress();
        }
      }
      break;
    }
    case 'SubagentStop': {
      const a = BY_NAME[ev.agent] || TEAM.find(t => t.ids.has(ev.agent_id));
      if (a && a !== MAIN) {
        setState(a, 'done', 'Finished', now);
        if (ev.agent_id) a.ids.delete(ev.agent_id);
        if (live) feed(now, a, 'finished its job');
      }
      break;
    }
    case 'Notification':
      setState(MAIN, 'waiting', ev.label || 'Needs you', now);
      if (live) { feed(now, MAIN, esc(ev.label || 'Claude needs you')); banner(ev.label || 'Claude needs you'); }
      break;
    case 'Stop':
      for (const a of TEAM) if (a.state === 'working' && now - a.lastSeen > 30_000) setState(a, 'idle', 'Idle', now);
      setState(MAIN, 'done', 'Over to you', now);
      banner(null);
      if (live) feed(now, MAIN, 'Claude finished. Over to you.');
      break;
  }
  updateCounters();
}

// ---------- panel ----------
const agentsEl = document.getElementById('agents');
for (const a of [MAIN, ...TEAM]) {
  const row = document.createElement('div');
  row.className = 'agent';
  row.innerHTML = `<div class="dot"></div><div class="n"></div><div class="w"></div><div class="a"></div><div class="bar"><i></i></div>`;
  row.querySelector('.n').textContent = a.title;
  row.querySelector('.w').textContent = a.wave ? 'Wave ' + a.wave : 'You';
  row.addEventListener('click', () => select(a.name));
  agentsEl.appendChild(row);
  a.row = row;
  renderRow(a);
}

function renderRow(a) {
  if (!a.row) return;
  a.row.querySelector('.dot').className = 'dot ' + a.state;
  const out = a.outputs ? ` · ${a.outputs} output${a.outputs > 1 ? 's' : ''}, last ${ago(a.lastOutput)}` : '';
  a.row.querySelector('.a').innerHTML = `<em>${esc(a.activity)}</em>${esc(out)}`;
  a.row.querySelector('.bar i').style.width = (progressOf(a) * 100).toFixed(0) + '%';
  a.row.classList.toggle('sel', selected === a.name);
}

function updateCounters() {
  document.getElementById('k-working').textContent = TEAM.filter(a => a.state === 'working').length;
  document.getElementById('k-tools').textContent = counters.tools;
  document.getElementById('k-files').textContent = counters.files;
}

const feedEl = document.getElementById('feed');
function feed(ms, a, html) {
  if (feedEl.firstElementChild?.classList.contains('empty')) feedEl.innerHTML = '';
  const li = document.createElement('li');
  const t = new Date(ms).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  li.innerHTML = `<time>${t.slice(0, 8)}</time><div><span style="color:#f3efe4">${esc(a.title)}</span> ${html}</div>`;
  feedEl.prepend(li);
  while (feedEl.children.length > 80) feedEl.lastChild.remove();
}

const bannerEl = document.getElementById('banner');
function banner(text) {
  bannerEl.style.display = text ? 'block' : 'none';
  if (text) bannerEl.textContent = text;
}

function openIssues(p) {
  return Object.entries(p.issues).filter(([s]) => !/^(fixed|checked|closed)$/i.test(s)).reduce((n, [, c]) => n + c, 0);
}
function reportsCount(p) { return p.agents.reduce((n, a) => n + a.outputs, 0); }

const MARK = {
  PASS: '<span class="ok">PASS</span>', FAIL: '<span class="bad">FAIL</span>',
  Ready: '<span class="ok">Ready</span>', 'Ready with fixes': '<span class="warn">Fixes</span>',
  'Not ready': '<span class="bad">Not ready</span>', 'See report': '<span class="warn">See</span>',
};
const yes = '<span class="ok">✓</span>', no = '<span class="none">·</span>';

function renderProgress(p) {
  for (const row of p.agents) {
    const a = BY_NAME[row.name];
    if (!a) continue;
    a.outputs = row.outputs;
    a.lastOutput = row.last_output_at ? row.last_output_at * 1000 : null;
    renderRow(a);
  }
  document.getElementById('products').innerHTML = p.products.map(x => `<tr>
    <td>${esc(x.slug.replace(/-/g, ' '))}</td>
    <td class="c">${x.qa ? MARK[x.qa] : no}</td>
    <td class="c">${x.ux ? MARK[x.ux] : no}</td>
    <td class="c">${x.listing ? yes : no}</td>
    <td class="c">${x.draft ? yes : no}</td></tr>`).join('');
  const iss = Object.entries(p.issues);
  document.getElementById('issues').innerHTML = iss.length
    ? iss.map(([s, c]) => `<div><b style="color:#f3efe4">${c}</b> ${esc(s)}</div>`).join('') : 'None logged yet';
  document.getElementById('issues').className = iss.length ? '' : 'empty';
  const d = p.decisions;
  document.getElementById('decisions').className = '';
  document.getElementById('decisions').innerHTML = `<div><b style="color:#f3efe4">${d.logged}</b> logged</div>` +
    `<div class="${d.awaiting_result ? 'warn' : ''}"><b>${d.awaiting_result}</b> need a result</div>`;
  const s = p.shop, shopEl = document.getElementById('shop');
  if (s) {
    const conv = s.views ? (s.orders / s.views * 100).toFixed(1) : '0.0';
    shopEl.className = 'kpis';
    shopEl.innerHTML = [[s.views, 'views'], [s.orders, 'orders'], ['£' + s.revenue.toFixed(2), 'revenue'],
      [s.favourites, 'favourites'], [conv, 'orders per 100 views'], [s.week, 'week']]
      .map(([v, l]) => `<div class="kpi"><div class="v" style="font-size:16px">${esc(String(v))}</div><div class="l">${l}</div></div>`).join('');
  }
  drawWall(p);
}

let lastProgress = null, progressTimer = null;
async function loadProgress() {
  if (DEMO) { lastProgress = demoProgress(); renderProgress(lastProgress); return; }
  try {
    const r = await fetch('api/progress', { cache: 'no-store' });
    lastProgress = await r.json();
    renderProgress(lastProgress);
  } catch { /* server stopped; the connection pill shows it */ }
}
function scheduleProgress() {
  clearTimeout(progressTimer);
  progressTimer = setTimeout(loadProgress, 800);
}

function select(name) {
  selected = selected === name ? null : name;
  for (const a of [MAIN, ...TEAM]) renderRow(a);
}

// ---------- helpers ----------
function esc(s) { return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function ago(ms) {
  if (!ms) return 'never';
  const s = (Date.now() - ms) / 1000;
  if (s < 90) return 'just now';
  if (s < 5400) return Math.round(s / 60) + ' min ago';
  if (s < 129600) return Math.round(s / 3600) + ' h ago';
  return Math.round(s / 86400) + ' days ago';
}

// ---------- connection ----------
const conn = document.getElementById('conn');
function setConn(cls, text) { conn.className = 'pill ' + cls; conn.textContent = text; }

function connect() {
  const es = new EventSource('api/events');
  es.onmessage = e => { try { handle(JSON.parse(e.data)); } catch (err) { console.warn(err); } };
  es.addEventListener('ready', () => {
    setConn('live', 'LIVE');
    // Anything still marked busy from old history has long stopped.
    const now = Date.now();
    for (const a of [MAIN, ...TEAM]) {
      if (a.state !== 'idle' && now - a.lastSeen > STALE_MS) setState(a, 'idle', 'Idle', now);
    }
  });
  es.onerror = () => setConn('off', 'OFFLINE');
}

// ---------- demo: a made-up weekly cycle ----------
function demoProgress() {
  const t = Date.now() / 1000;
  return {
    agents: TEAM.map((a, i) => ({ name: a.name, outputs: a.wave === 1 ? 2 + (i % 3) : 0,
      last_output_at: a.wave === 1 ? t - 3600 * (i + 1) : null })),
    products: ['breakdown-dashboard', 'ci-starter-kit', 'kpi-calculator', 'mtba-tracker', 'rcfa-template', 'visibility-kit']
      .map((slug, i) => ({ slug, qa: ['PASS', 'PASS', 'FAIL', 'PASS', null, 'PASS'][i],
        ux: ['Ready with fixes', 'Ready', 'Not ready', null, null, 'Ready'][i], listing: true, draft: i % 2 === 1 })),
    issues: { Open: 3, 'Fix in progress': 1, Fixed: 2 },
    decisions: { logged: 4, awaiting_result: 1 },
    shop: { week: 'demo', views: 182, favourites: 11, orders: 4, revenue: 37.96 },
  };
}

function runDemo() {
  setConn('demo', 'DEMO');
  const P = ['visibility-kit', 'ci-starter-kit', 'rcfa-template', 'mtba-tracker', 'kpi-calculator'];
  const pick = arr => arr[Math.floor(Math.random() * arr.length)];
  const script = () => {
    const prod = pick(P), day = new Date().toISOString().slice(0, 10);
    const job = (agent, task, steps, out) => [
      { event: 'PreToolUse', tool: 'Agent', target: agent, label: task, agent: 'coordinator' },
      ...steps.flatMap(([tool, label]) => [{ event: 'PreToolUse', tool, label, agent }, { wait: 900 }]),
      ...(out ? [{ event: 'PostToolUse', tool: 'Write', label: out.split('/').pop(), path: out, agent }] : []),
      { event: 'SubagentStop', agent },
    ];
    return [
      { event: 'UserPromptSubmit' },
      { event: 'PreToolUse', tool: 'Agent', target: 'coordinator', label: 'Run the weekly cycle' },
      { event: 'PreToolUse', tool: 'Read', label: 'CLAUDE.md', agent: 'coordinator' }, { wait: 700 },
      { event: 'PreToolUse', tool: 'Glob', label: 'data/exports/*', agent: 'coordinator' }, { wait: 700 },
      ...job('shop-analyst', 'Weekly numbers report', [['Read', 'stats.csv'], ['Read', 'decisions.md'], ['Bash', 'Work out conversion per listing'],
        ['Bash', 'Compare with last week'], ['Write', day + '.md']], `reports/weekly/${day}.md`),
      ...job('ci-challenger', 'Weekly CI review', [['Read', 'issues.md'], ['Read', 'listing.md'], ['Bash', 'Render every page of ' + prod],
        ['Grep', 'em dash check'], ['Bash', 'Check field names are unique'], ['Write', day + '.md']], `reports/ci/${day}.md`),
      { event: 'PreToolUse', tool: 'Agent', target: 'product-qa', label: 'Check ' + prod, agent: 'coordinator' },
      { event: 'PreToolUse', tool: 'Agent', target: 'usability-checker', label: 'Check ' + prod, agent: 'coordinator' },
      ...[['Bash', 'pdftoppm render pages'], ['Bash', 'Fill every form field'], ['Bash', 'pdftotext typo check'],
        ['Bash', 'Test as a night-shift operator on a phone'], ['Read', 'listing.md']]
        .flatMap(([tool, label], i) => [{ event: 'PreToolUse', tool, label, agent: i % 2 ? 'usability-checker' : 'product-qa' }, { wait: 1000 }]),
      { event: 'PostToolUse', tool: 'Write', path: `reports/qa/${prod}-${day}.md`, agent: 'product-qa' },
      { event: 'SubagentStop', agent: 'product-qa' }, { wait: 600 },
      { event: 'PostToolUse', tool: 'Write', path: `reports/ux/${prod}-${day}.md`, agent: 'usability-checker' },
      { event: 'SubagentStop', agent: 'usability-checker' },
      { event: 'PreToolUse', tool: 'Read', label: 'decisions.md', agent: 'coordinator' }, { wait: 800 },
      { event: 'PreToolUse', tool: 'Write', label: day + '.md', agent: 'coordinator' }, { wait: 900 },
      { event: 'PostToolUse', tool: 'Write', path: `reports/brief/${day}.md`, agent: 'coordinator' },
      { event: 'SubagentStop', agent: 'coordinator' },
      { event: 'PostToolUse', tool: 'Agent', target: 'coordinator', label: 'Monday Brief ready' },
      ...job('customer-care', 'Draft replies to new messages', [['Glob', 'data/inbox/*'], ['Write', 'replies-' + day + '.md']], `data/inbox/replies-${day}.md`),
      ...job('market-scout', 'Check a buyer request', [['WebSearch', 'shift handover template'], ['WebFetch', 'etsy.com/search'], ['Write', 'buyer-requests.md']]),
      { event: 'Notification', label: 'Monday Brief ready: 3 decisions for Josh' }, { wait: 5000 },
      { event: 'Stop' }, { wait: 6000 },
    ];
  };
  let queue = [];
  const step = () => {
    if (!queue.length) queue = script();
    const ev = queue.shift();
    if (ev.wait) return setTimeout(step, ev.wait);
    handle({ ts: Date.now() / 1000, agent: '', ...ev });
    setTimeout(step, 450 + Math.random() * 500);
  };
  step();
}

// ---------- loop ----------
function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h);
  labels.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  // Pull back on narrow screens so all three waves stay in view.
  if (!userMoved) {
    const tall = camera.aspect < 1;
    const d = 25 * Math.max(1, 1.55 / camera.aspect) * (tall ? 1.1 : 1);
    camera.position.set(0, d * (tall ? 0.9 : 0.68), d * (tall ? 0.45 : 0.78));
  }
  // On a phone only the busy agents keep their name tags.
  stage.classList.toggle('compact', w < 640);
}
new ResizeObserver(resize).observe(stage);
resize();

const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
let downAt = null;
renderer.domElement.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 5) return;
  const r = renderer.domElement.getBoundingClientRect();
  mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObjects(pickables)[0];
  if (hit) select(hit.object.userData.agent); else if (selected) select(selected);
});

const clock = new THREE.Clock();
const goal = new THREE.Vector3();
function frame() {
  const dt = Math.min(clock.getDelta(), 0.1), t = clock.elapsedTime, now = Date.now();
  for (const a of TEAM) {
    const v = a.view;
    if (a.state === 'working') {
      v.torso.position.y = 0.98 + Math.sin(t * 3 + a.pos[0]) * 0.02;
      v.arms[0].rotation.x = -1.1 + Math.sin(t * 18) * 0.15;
      v.arms[1].rotation.x = -1.1 + Math.sin(t * 18 + 1.6) * 0.15;
      v.ring.rotation.z += dt * 3;
      v.glow.intensity = 5 + Math.sin(t * 6) * 1.5;
      if (now - a.lastSeen > STALE_MS) setState(a, 'idle', 'Idle', now);
    } else {
      v.torso.position.y = 0.98 + Math.sin(t * 1.2 + a.pos[0]) * 0.008;
      if (a.state === 'done' && now - a.lastSeen > DONE_FOR_MS) setState(a, 'idle', 'Idle', now);
    }
    if (a.state === 'waiting') v.lamp.visible = Math.sin(t * 8) > 0; else v.lamp.visible = true;
  }
  const m = MAIN.view;
  m.holo.rotation.y += dt * (MAIN.state === 'working' ? 1.6 : 0.3);
  m.holo.rotation.x += dt * 0.2;
  m.lamp.visible = MAIN.state !== 'waiting' || Math.sin(t * 8) > 0;
  if (MAIN.state === 'done' && now - MAIN.lastSeen > DONE_FOR_MS) setState(MAIN, 'idle', 'Ready', now);

  for (let i = packets.length - 1; i >= 0; i--) {
    const p = packets[i];
    p.t += dt / 1.3;
    p.orb.position.copy(p.curve.getPoint(Math.min(1, p.t)));
    p.line.material.opacity = 0.35 * (1 - p.t);
    if (p.t >= 1) { scene.remove(p.orb, p.line); p.orb.geometry.dispose(); p.line.geometry.dispose(); packets.splice(i, 1); }
  }

  if (selected) {
    const a = BY_NAME[selected];
    goal.set(a.pos[0], 1, a.pos[1]);
    controls.target.lerp(goal, 0.06);
  }
  controls.update();
  renderer.render(scene, camera);
  labels.render(scene, camera);
  requestAnimationFrame(frame);
}

setInterval(() => {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  if (lastProgress) drawWall(lastProgress);
}, 1000);
setInterval(loadProgress, 15000);

drawWall(null);
loadProgress();
if (DEMO) runDemo(); else connect();
frame();
