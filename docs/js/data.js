import { CAT_COLORS } from './constants.js';
import { DAY, NOW, timestamp, repositoryUrl } from './util.js';

export async function fetchData() {
  const response = await fetch('./stars.json', { cache: 'no-cache' });
  if (!response.ok) throw new Error('数据请求失败');
  return normalize(await response.json());
}

export function normalize(data) {
  if (!data || !Array.isArray(data.repos) || !Array.isArray(data.categories)) {
    throw new Error('数据格式无效');
  }
  const categories = [];
  const categoryMap = new Map();
  for (const item of data.categories) {
    if (
      !item || typeof item.id !== 'string' || !item.id ||
      ['all', 'uncategorized'].includes(item.id) || categoryMap.has(item.id)
    ) continue;
    const category = {
      id: item.id,
      name: String(item.name_zh ?? item.id),
      description: String(item.description_zh ?? ''),
      color: CAT_COLORS[categories.length % CAT_COLORS.length]
    };
    categories.push(category);
    categoryMap.set(category.id, category);
  }
  const repos = data.repos.filter(item => item && typeof item === 'object').map(item => {
    const name = String(item.full_name ?? '');
    const summaryZh = typeof item.summary_zh === 'string' ? item.summary_zh.trim() : '';
    const description = typeof item.description === 'string' ? item.description : '';
    const summary = summaryZh || description || '（暂无简介）';
    const tags = Array.isArray(item.tags) ? item.tags.filter(tag => typeof tag === 'string' && tag.trim()) : [];
    const pushed = timestamp(item.pushed_at);
    const stars = Number(item.stargazers_count);
    return {
      name, summary, tags, pushed,
      missingSummary: !summaryZh && !description,
      starred: timestamp(item.starred_at),
      url: repositoryUrl(item.html_url, name),
      category: categoryMap.has(item.category) ? item.category : 'uncategorized',
      language: typeof item.language === 'string' ? item.language : '',
      stars: Number.isFinite(stars) && stars > 0 ? stars : 0,
      archived: Boolean(item.archived),
      isStale: item.stale == null ? NOW - (pushed ?? 0) > 365 * DAY : Boolean(item.stale),
      haystack: `${name} ${summary} ${description} ${tags.join(' ')}`.toLowerCase()
    };
  });
  if (repos.some(repo => repo.category === 'uncategorized')) {
    const category = { id: 'uncategorized', name: '待整理', description: '', color: '#94A3B8' };
    categories.push(category);
    categoryMap.set(category.id, category);
  }
  return {
    categories, categoryMap, repos,
    user: typeof data.user === 'string' && data.user.trim() ? data.user.trim() : 'laoshuterry',
    generated: timestamp(data.generated_at)
  };
}
