"""Merge raw fetch + category draft + summaries into stars.json / stars.csv."""
import json,csv,glob,datetime,os
B=os.path.dirname(os.path.abspath(__file__))+'/..'
raw=json.load(open(f'{B}/raw/starred_raw.json'))
draft=json.load(open(f'{B}/categories_draft.json'))
cat_by_name={r['full_name']:r['category'] for r in draft['repos']}
S={}
for f in sorted(glob.glob(f'{B}/raw/sum/*.txt')):
    for line in open(f,encoding='utf-8'):
        line=line.rstrip('\n')
        if not line: continue
        i,s,t=line.split('|',2); S[int(i)]=(s.strip(),[x.strip() for x in t.split(',') if x.strip()])
README_USED={18,27,80,106,115,116,117,120,147,187,195,212,217,304,317,330,337,432,454,517,534,541,554,571,688,722,735}
NAME_ONLY={261,400,561,617,709}  # empty description and no README
today=datetime.datetime(2026,11,13,tzinfo=datetime.timezone.utc)
cut=today.replace(year=2025)
repos=[]
for i,s in enumerate(raw,1):
    r=s['repo']; summ,tags=S[i]
    pushed=datetime.datetime.fromisoformat(r['pushed_at'].replace('Z','+00:00')) if r.get('pushed_at') else None
    repos.append(dict(
      full_name=r['full_name'],name=r['name'],owner=r['owner']['login'],html_url=r['html_url'],
      description=r.get('description') or '',summary_zh=summ,category=cat_by_name[r['full_name']],tags=tags,
      language=r.get('language'),stargazers_count=r['stargazers_count'],forks_count=r['forks_count'],
      topics=r.get('topics',[]),homepage=r.get('homepage') or '',license=(r.get('license') or {}).get('spdx_id'),
      archived=r['archived'],stale=bool(pushed and pushed<cut),fork=r['fork'],
      pushed_at=r.get('pushed_at'),created_at=r.get('created_at'),updated_at=r.get('updated_at'),starred_at=s['starred_at'],
      owner_avatar_url=r['owner']['avatar_url'],
      summary_source='readme' if i in README_USED else ('name_only' if i in NAME_ONLY else 'description')))
cats=[{k:c[k] for k in ('id','name_zh','description_zh')}|{'count':sum(1 for r in repos if r['category']==c['id'])} for c in draft['categories']]
out=dict(generated_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),user='laoshuterry',total=len(repos),
  stats=dict(archived=sum(r['archived'] for r in repos),stale=sum(r['stale'] for r in repos),
             summary_from_readme=len(README_USED),summary_name_only=len(NAME_ONLY),stale_cutoff=cut.date().isoformat()),
  categories=cats,repos=repos)
# validation
assert len(repos)==len(raw)==736
ids={c['id'] for c in cats}
for r in repos:
    assert r['category'] in ids and r['summary_zh'] and len(r['summary_zh'])<=60, r['full_name']
    assert 2<=len(r['tags'])<=5, r['full_name']
assert sum(c['count'] for c in cats)==len(repos)
json.dump(out,open(f'{B}/stars.json','w'),ensure_ascii=False,indent=1)
with open(f'{B}/stars.csv','w',newline='',encoding='utf-8-sig') as f:
    cols=['full_name','html_url','category','category_name_zh','summary_zh','tags','description','language','stargazers_count','forks_count','topics','homepage','license','archived','stale','fork','pushed_at','created_at','starred_at','owner_avatar_url','summary_source']
    w=csv.writer(f); w.writerow(cols); cn={c['id']:c['name_zh'] for c in cats}
    for r in repos:
        w.writerow([r['full_name'],r['html_url'],r['category'],cn[r['category']],r['summary_zh'],'|'.join(r['tags']),r['description'],r['language'] or '',r['stargazers_count'],r['forks_count'],'|'.join(r['topics']),r['homepage'],r['license'] or '',r['archived'],r['stale'],r['fork'],r['pushed_at'],r['created_at'],r['starred_at'],r['owner_avatar_url'],r['summary_source']])
print(json.dumps(out['stats'],ensure_ascii=False)); 
for c in cats: print(c['count'],c['name_zh'])
