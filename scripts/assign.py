import json,re,datetime
CATS=[
("A","ai-agent-skills","AI Agent 与编程 Skills","Claude Code / Codex 等编程 Agent、Agent 框架、通用工程类 Skills 与 Agent 学习资料"),
("D","design-slides","设计、PPT 与图表","设计工具、设计规范、AI 设计/前端审美 Skills、PPT 与图表生成"),
("C","content-creation","自媒体与内容创作","小红书/公众号/X 等内容生产、排版、发布与运营工具和 Skills"),
("V","aigc-video","AI 图像、视频与多媒体创作","AI 生图/生视频模型、ComfyUI、提示词库、视频剪辑与动画生成"),
("L","llm-ml","大模型与机器学习","大模型训练推理、机器学习框架、模型与 AI/深度学习教程书籍"),
("K","cs-learning","计算机学习与面试","CS 课程、编程教程、算法刷题、面试题、技术书籍与速查手册"),
("G","life-growth","生活指南、成长与阅读","生活建议、健康、理财入门、人际、移民、一人公司与阅读资源"),
("Q","finance-blockchain","金融、量化与区块链","个人财务、量化投资、行情工具、比特币/以太坊"),
("P","proxy","网络代理与科学上网","代理协议、客户端、面板、规则与相关教程"),
("N","network-telecom","网络与通信协议","网络仿真、协议编解码、LTE/5G/3GPP、高性能网络"),
("S","self-hosted","自托管服务与网盘","可自建的相册、影音、密码、通讯、文件与 WebDAV 服务"),
("M","media","影音播放、下载与 BT","视频/音乐播放器、下载器、直播录制、IPTV、BT 工具"),
("U","audio-music","音频与音乐制作","合成器、音频插件、DAW、音频框架与 DSP 资源"),
("T","devtools","开发工具、编辑器与终端","IDE/编辑器配置、终端、字体、调试分析、构建与自动化工具"),
("F","lang-lib","编程语言、框架与库","编程语言实现、通用框架、各语言库与 SDK"),
("W","web-frontend","Web 前端、可视化与建站","前端框架/组件、图表可视化、图标字体、静态站点生成"),
("H","os-hardware","操作系统、固件与硬件","内核、BIOS/UEFI、路由器固件、RISC-V/FPGA、开发板、飞控"),
("X","security","安全与逆向工程","渗透测试、逆向/反编译、调试器、安全书籍与工具"),
("J","games-graphics","游戏、图形与仿真","游戏源码/引擎、模拟器、渲染与图形学、物理/航天/机器人仿真、棋类 AI"),
("Y","utilities","桌面与效率工具","Windows/macOS 实用工具、文件传输清理、笔记与日常效率软件"),
("R","awesome-lists","Awesome 资源合集","各类 awesome 列表与资源导航"),
("Z","misc","其他","个人博客、杂项或难以归类的仓库"),
]
M="""
A 1 2 5 13 14 16 17 20 21 22 23 24 25 27 29 30 31 32 33 48 56 64 74 79 80 94 96 102 103 105 109 114 115 120 123 125 128 133 137 138 140 146 160 161 170 171
D 4 26 38 39 44 47 49 55 69 76 84 104 106 111 129 131 139 141 142 144 157 158 296
C 28 57 58 61 62 63 71 73 75 77 87 88 95 108 113 143 507
V 15 34 35 36 37 40 41 42 43 46 65 70 83 89 91 92 99 101 110 112 116 117 118 121 135 149 150 151 152 153 154 180 202
L 6 67 82 85 86 127 136 145 148 159 162 166 169 175 178 184 187 192 196 200 201 221 272 274 275 294 317 327 360 396 403 411 430 435 446 459 464 472 510 540 541 542 546 547 549 550 551 553
K 59 60 78 168 193 197 204 205 206 207 212 216 219 224 229 232 233 244 265 284 289 321 335 338 376 381 386 387 399 408 415 420 431 432 462 470 473 474 480 481 494 516 536 545 563 587 588 607 614 615 618 629 640 658 682 702 703 714 729
G 7 8 9 10 11 12 93 98 124 155 182 234 242 308 355 418 559 593
Q 50 68 156 174 183 255 323 465 560 612 650
P 90 97 100 126 185 186 230 231 235 236 257 282 378 379 400 401 402 407 409 501 504 505 506 509 514 515 518 519 520 521 522 524 579 580 581 669 672 673 674 675 684 686 688 691 696 707 708 709 710 711
N 190 198 199 263 333 444 454 455 456 457 466 513 523 531 532 570
S 51 52 54 122 164 173 189 266 267 277 278 283 285 326 331 353 433 488 573
M 72 107 147 203 256 264 273 290 293 309 318 322 329 352 356 384 388 389 390 391 425 426 437 438 439 482 508 567 572 577 578 627 683
U 188 227 228 239 240 243 247 251 254 271 305 306 311 312 315 339 342 345 346 347 348 351 354 357 358 359 397 398 404 405 406 566 568
T 19 130 181 452 217 218 302 313 316 328 334 362 383 413 422 440 458 467 468 477 490 499 512 527 529 530 543 544 554 555 558 562 565 584 594 595 596 599 603 606 616 621 622 628 648 659 660 670 687 692 698 705 706 713 715 716 717 718 722 723 724 725 726 727 728 731 732 733 734 735
F 191 214 223 241 319 337 343 368 416 421 442 445 449 463 492 495 496 552 564 582 583 597 598 600 602 604 611 613 619 624 630 638 651 653 655 665 679 680 681 685 689 700
W 258 259 260 261 262 303 341 349 469 485 486 487 489 503 574 635 656 667 694 712 720 721 730
H 3 45 208 245 286 287 288 310 361 371 372 373 377 380 395 417 427 428 429 450 461 475 476 478 479 483 500 525 528 539 569 590 591 592 610 631 657 678 690 704 719
X 81 119 194 210 220 253 363 365 367 375 410 453 498 548 693
J 134 163 165 209 211 222 225 237 248 250 252 269 270 276 279 281 295 297 298 300 301 324 325 332 344 350 364 366 369 370 374 382 392 393 394 414 423 451 471 534 535 537 538 556 557 561 589 601 609 620 634 654 661 662 676 677 695 699
Y 18 53 66 132 176 177 226 246 249 280 291 292 299 307 314 336 385 412 434 436 441 447 493 497 502 511 533 626 637
R 167 179 238 448 491 526 575 576 585 586 605 608 623 625 633 636 639 641 642 643 644 645 646 647 649 652 668 671 697 701 736
Z 172 195 213 215 268 304 320 330 340 419 424 443 460 484 517 571 617 632 663 664 666
"""
raw=json.load(open('/workspace/github-stars/raw/starred_raw.json'))
n=len(raw); idx={}
for line in M.strip().splitlines():
    c,*nums=line.split()
    for x in nums:
        x=int(x); assert x not in idx, ("dup",x,idx.get(x),c); idx[x]=c
missing=[i for i in range(1,n+1) if i not in idx]; extra=[i for i in idx if i>n]
assert not missing and not extra,(missing,extra)
code={c[0]:c for c in CATS}
cats=[]; repos=[]
for i,s in enumerate(raw,1):
    r=s['repo']; c=code[idx[i]]
    repos.append(dict(idx=i,full_name=r['full_name'],html_url=r['html_url'],description=r.get('description') or '',
      language=r.get('language'),stargazers_count=r['stargazers_count'],topics=r.get('topics',[]),archived=r['archived'],
      pushed_at=r['pushed_at'],starred_at=s['starred_at'],category=c[1]))
for c in CATS:
    cats.append(dict(id=c[1],name_zh=c[2],description_zh=c[3],count=sum(1 for r in repos if r['category']==c[1])))
json.dump(dict(generated_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),user='laoshuterry',total=n,
  status='draft - pending user review',categories=cats,repos=repos),open('/workspace/github-stars/categories_draft.json','w'),ensure_ascii=False,indent=1)
L=[f"# laoshuterry 的 GitHub Star 分类草案\n\n共 {n} 个仓库，{len(cats)} 个分类。生成时间：{datetime.datetime.now():%Y-%m-%d %H:%M}（PKT, UTC+5）。仅为分类草案，待确认后再写中文简介。\n\n## 分类总览\n\n| # | 分类 | id | 数量 | 说明 |\n|---|---|---|---|---|"]
for k,c in enumerate(cats,1): L.append(f"| {k} | {c['name_zh']} | `{c['id']}` | {c['count']} | {c['description_zh']} |")
for c in cats:
    L.append(f"\n## {c['name_zh']}（{c['count']}）\n\n{c['description_zh']}\n")
    for r in sorted([r for r in repos if r['category']==c['id']],key=lambda r:-r['stargazers_count']):
        d=re.sub(r'\s+',' ',r['description'])[:90]
        L.append(f"- [{r['full_name']}]({r['html_url']}) ★{r['stargazers_count']:,} — {d or '（无描述）'}")
open('/workspace/github-stars/categories_draft.md','w').write("\n".join(L)+"\n")
for c in cats: print(c['count'],c['name_zh'])
print("total",n,sum(c['count'] for c in cats))
