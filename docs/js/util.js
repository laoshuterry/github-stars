export const DAY = 86400000;
export const NOW = Date.now();
export const $ = selector => document.querySelector(selector);

export function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
}

export function highlight(value, query) {
  const text = String(value ?? '');
  if (!query) return escapeHtml(text);
  const pattern = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = text.matchAll(new RegExp(pattern, 'ig'));
  let result = '';
  let position = 0;
  for (const match of matches) {
    result += escapeHtml(text.slice(position, match.index));
    result += `<mark>${escapeHtml(match[0])}</mark>`;
    position = match.index + match[0].length;
  }
  return result + escapeHtml(text.slice(position));
}

export function formatNumber(number) {
  if (number >= 1e6) return (number / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
  if (number >= 1e4) return (number / 1e3).toFixed(number >= 1e5 ? 0 : 1).replace(/\.0$/, '') + 'k';
  if (number >= 1e3) return (number / 1e3).toFixed(1).replace(/\.0$/, '') + 'k';
  return String(number);
}

export function timestamp(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  const time = Date.parse(value);
  return Number.isFinite(time) ? time : null;
}

export function relativeTime(time) {
  if (time === null) return '—';
  const days = (NOW - time) / DAY;
  if (days < 1) return Math.max(1, Math.round(days * 24)) + ' 小时前';
  if (days < 30) return Math.round(days) + ' 天前';
  if (days < 365) return Math.round(days / 30) + ' 个月前';
  return (days / 365).toFixed(1).replace(/\.0$/, '') + ' 年前';
}

export function localDate(time, includeTime = false) {
  if (time === null) return '—';
  const date = new Date(time);
  const pad = value => String(value).padStart(2, '0');
  const day = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
  return includeTime ? `${day} ${pad(date.getHours())}:${pad(date.getMinutes())}` : day;
}

export function repositoryUrl(url, name) {
  try {
    const parsed = new URL(url);
    if (['http:', 'https:'].includes(parsed.protocol)) return parsed.href;
  } catch {}
  return 'https://github.com/' + name.split('/').map(encodeURIComponent).join('/');
}
