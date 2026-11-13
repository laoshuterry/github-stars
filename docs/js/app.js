import { $ } from './util.js';
import { ICON_SUN, ICON_MOON } from './constants.js';
import { fetchData } from './data.js';
import { render, renderMetadata } from './render.js';

const state = { cat: 'all', q: '', sort: 'starred', hideStale: false, limit: 60 };
const params = new URLSearchParams(location.hash.slice(1));
let data = null;
let searchTimer;

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  $('#theme').innerHTML = theme === 'dark' ? ICON_SUN : ICON_MOON;
  $('#theme').setAttribute('aria-label', theme === 'dark' ? '切换浅色模式' : '切换深色模式');
  try {
    localStorage.setItem('gs-theme', theme);
  } catch {}
}

function setDrawer(open) {
  document.body.classList.toggle('drawer', open);
  $('#menu').setAttribute('aria-expanded', String(open));
}

function update() {
  if (data) render(data, state);
}

function reset() {
  state.limit = 60;
  update();
  window.scrollTo(0, 0);
}

async function load() {
  $('#more').hidden = true;
  $('#grid').innerHTML = '<div class="empty-st">正在加载数据…</div>';
  try {
    data = await fetchData();
    const category = params.get('cat');
    if (category === 'all' || data.categoryMap.has(category)) state.cat = category;
    renderMetadata(data);
    update();
  } catch {
    const message = location.protocol === 'file:'
      ? '浏览器无法在 file:// 页面读取数据。请通过 HTTP 访问，例如在站点目录运行 python3 -m http.server。'
      : '暂时无法加载数据，请检查网络连接及 stars.json 文件后重试。';
    $('#grid').innerHTML = `<div class="empty-st">
      <b>数据加载失败</b>
      <p>${message}</p>
      <button class="more" id="retry">重试</button>
    </div>`;
  }
}

$('#cats').addEventListener('click', event => {
  const button = event.target.closest('.cat');
  if (!button) return;
  state.cat = button.dataset.id;
  setDrawer(false);
  reset();
});
$('#q').addEventListener('input', event => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.q = event.target.value.trim();
    reset();
  }, 120);
});
$('#sort').addEventListener('click', event => {
  const button = event.target.closest('button[data-k]');
  if (!button) return;
  state.sort = button.dataset.k;
  reset();
});
$('#hideStale').addEventListener('change', event => {
  state.hideStale = event.target.checked;
  reset();
});
$('#grid').addEventListener('click', event => {
  if (event.target.closest('#retry')) {
    load();
    return;
  }
  const tag = event.target.closest('.tag');
  if (!tag) return;
  event.preventDefault();
  clearTimeout(searchTimer);
  state.q = tag.dataset.tag;
  $('#q').value = state.q;
  reset();
});
$('#more').addEventListener('click', () => {
  state.limit += 90;
  update();
});
$('#theme').addEventListener('click', () => {
  setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});
$('#menu').addEventListener('click', () => setDrawer(true));
$('#scrim').addEventListener('click', () => setDrawer(false));
document.addEventListener('keydown', event => {
  if (event.key === '/' && document.activeElement !== $('#q')) {
    event.preventDefault();
    $('#q').focus();
  }
  if (event.key === 'Escape') setDrawer(false);
});
new IntersectionObserver(entries => {
  if (entries[0].isIntersecting && !$('#more').hidden && data) {
    state.limit += 90;
    update();
  }
}, { rootMargin: '600px' }).observe($('#more'));

let savedTheme;
try {
  savedTheme = localStorage.getItem('gs-theme');
} catch {}
const validTheme = theme => ['light', 'dark'].includes(theme);
const hashTheme = params.get('theme');
const preferredTheme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
setTheme(validTheme(hashTheme) ? hashTheme : validTheme(savedTheme) ? savedTheme : preferredTheme);
state.q = params.get('q') || '';
$('#q').value = state.q;
if (['stars', 'pushed', 'starred'].includes(params.get('sort'))) state.sort = params.get('sort');
setDrawer(params.get('drawer') === '1');
load();
