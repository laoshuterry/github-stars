import { LANG, ICON_STAR } from './constants.js';
import { $, escapeHtml as esc, highlight, formatNumber as fmt, relativeTime, localDate } from './util.js';

function matches(repo, state) {
  return (!state.q.trim() || repo.haystack.includes(state.q.toLowerCase().trim())) &&
    (!state.hideStale || !(repo.isStale || repo.archived));
}

function badges(repo) {
  if (repo.archived) return '<span class="badge b-arch" title="仓库已归档">已归档</span>';
  if (repo.isStale) return '<span class="badge b-stale" title="超过一年没有更新">一年未更新</span>';
  return '';
}

function categoryButton(category, counts, state) {
  const count = counts.get(category.id) || 0;
  const classes = `cat${state.cat === category.id ? ' on' : ''}${count ? '' : ' empty'}`;
  return `<button class="${classes}" data-id="${esc(category.id)}">
    <i class="dot" style="background:${category.color}"></i>
    <span class="nm">${esc(category.name)}</span>
    <span class="ct">${count}</span>
  </button>`;
}

function stats(scope) {
  const totalStars = scope.reduce((sum, repo) => sum + repo.stars, 0);
  const inactive = scope.filter(repo => repo.archived || repo.isStale).length;
  return `<span class="stat"><b>${scope.length}</b>仓库</span>
    <span class="stat"><b>${fmt(totalStars)}</b>总 Star</span>
    <span class="stat"><b>${inactive}</b>不活跃</span>`;
}

function card(repo, data, state) {
  const hl = text => highlight(text, state.q);
  const slash = repo.name.indexOf('/');
  const name = slash < 0
    ? hl(repo.name)
    : `<span class="own">${hl(repo.name.slice(0, slash))}/</span>${hl(repo.name.slice(slash + 1))}`;
  const color = Object.hasOwn(LANG, repo.language) ? LANG[repo.language] : '#8B949E';
  const category = data.categoryMap.get(repo.category);
  const tags = repo.tags.map(tag =>
    `<button class="tag" data-tag="${esc(tag)}">#${hl(tag)}</button>`
  ).join('');
  const language = repo.language
    ? `<span class="lang"><i class="ld" style="background:${color}"></i>${esc(repo.language)}</span>`
    : '';
  const categoryChip = state.cat === 'all' && category
    ? `<span class="cat-chip">${esc(category.name)}</span>`
    : '';
  const updated = relativeTime(repo.pushed) + (repo.pushed === null ? '' : '更新');
  return `<article class="card">
    <div class="c-top">
      <h3 class="c-name"><a href="${esc(repo.url)}" target="_blank" rel="noopener">${name}</a></h3>
      <div class="badges">${badges(repo)}</div>
    </div>
    <p class="c-desc${repo.missingSummary ? ' muted' : ''}" title="${esc(repo.summary)}">${hl(repo.summary)}</p>
    ${repo.tags.length ? `<div class="tags">${tags}</div>` : ''}
    <div class="meta">
      <span class="st">${ICON_STAR}${fmt(repo.stars)}</span>
      ${language}
      ${categoryChip}
      <span class="tm" title="最近更新 ${localDate(repo.pushed)} · Star 于 ${localDate(repo.starred)}">${updated}</span>
    </div>
  </article>`;
}

export function render(data, state) {
  const matching = data.repos.filter(repo => matches(repo, state));
  const counts = new Map([['all', matching.length]]);
  for (const repo of matching) counts.set(repo.category, (counts.get(repo.category) || 0) + 1);
  const allCategory = { id: 'all', name: '全部', color: 'linear-gradient(135deg,#8B5CF6,#06B6D4)' };
  $('#cats').innerHTML = [allCategory, ...data.categories]
    .map(category => categoryButton(category, counts, state)).join('');
  const category = data.categoryMap.get(state.cat);
  const scope = category ? data.repos.filter(repo => repo.category === category.id) : data.repos;
  const list = matching.filter(repo => state.cat === 'all' || repo.category === state.cat);
  const key = { starred: 'starred', stars: 'stars', pushed: 'pushed' }[state.sort];
  list.sort((a, b) => {
    if (a[key] === null) return b[key] === null ? 0 : 1;
    if (b[key] === null) return -1;
    return b[key] - a[key];
  });
  $('#title').textContent = category ? category.name : '全部收藏';
  $('#sub').textContent = category
    ? category.description
    : `FatMouse 在 GitHub 上 Star 的全部仓库，按 ${data.categories.length} 个主题分类整理。`;
  $('#stats').innerHTML = stats(scope);
  const result = `共 <b>${list.length}</b> 个${state.q ? `，匹配“${esc(state.q)}”` : ''}`;
  $('#result').innerHTML = result;
  $('#mresult').innerHTML = result;
  $('#grid').innerHTML = list.length
    ? list.slice(0, state.limit).map(repo => card(repo, data, state)).join('')
    : `<div class="empty-st">
        <b>没有找到相关仓库</b>换个关键词，或切换到“全部”分类试试
      </div>`;
  $('#more').hidden = list.length <= state.limit;
  $('#more').textContent = `加载更多（还有 ${Math.max(0, list.length - state.limit)} 个）`;
  document.querySelectorAll('#sort button').forEach(button => {
    button.classList.toggle('on', button.dataset.k === state.sort);
  });
}

export function renderMetadata(data) {
  document.title = `Star 收藏夹 · ${data.user}`;
  $('#user').textContent = '@' + data.user;
  $('.gh').href = `https://github.com/${encodeURIComponent(data.user)}?tab=stars`;
  $('#categoryCount').textContent = `${data.categories.length} 个分类`;
  $('#upd').textContent = data.generated === null ? '数据更新时间未知' : '数据 ' + localDate(data.generated);
  $('#dataFooter').textContent = data.generated === null
    ? '数据更新时间未知'
    : '数据更新于 ' + localDate(data.generated, true);
}
