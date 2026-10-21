# Phase C 分类与发表信息审计

审计日期：2026-10-14。输入为上级目录的 `all_candidates.csv`（83 行）、`rag_core_papers.csv`（61 行）和 `rag_classification.csv`（61 行）。本阶段不改变 Phase A/B 原始清单；下述判断属于对现有记录及入选论文正文的复核。

## 行数、唯一性和 54＋7 的含义

三份表按论文 ID 连接：61 条核心记录与 61 条分类记录一一对应，主分类代码均非空，且每条仅有一个主分类。83 条候选、61 条核心及 61 条分类均无重复论文 ID；核心表也无重复标题或重复的非空 DOI/arXiv 字段。核心表与分类表的 ID 集合和主分类代码完全一致。这里的“唯一主分类”不排斥 A—H 的多标签辅助列及一个次要分类。

|主分类|A|B|C|D|E|F|G|H|小计|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|篇数|4|9|8|4|5|8|2|14|54|

其余 **7 篇仍在 61 篇 RAG 核心池内**，但主分类不属于 A—H：M「多模态 RAG」4 篇、I「检索表示与索引」1 篇、L「多语言 RAG」1 篇、X「RAG 系统效率」1 篇。因此 54 与 61 的差额不是缺失分类。辅助列中的 A—H 匹配可与这 7 篇重叠，不能当作主分类求和。

## 错分、边界与去重

在本轮入选全文中未发现能够确定的主分类错误，也未发现同一论文在三表中重复。以下边界值得在深入精读时复核：NEST（`2026.acl-industry.35`）同时涉及高噪声检索和上下文选择，暂保留 C；RAGLens（ICLR 2026）属于生成忠实性检测，暂保留 F；《Classifying Errors in RAG》（`2026.eacl-long.147`）属于评测/归因，保留 H。这些是主分类取舍，**不是**把论文计入两个主类。两篇不同的 FlowRAG 尤其不能合并：本轮 G 类 `www26-3792361` 是 WWW 2026 的持续学习检索器；另有同名的图式推理检索论文，标题、副标题和作者均不同。

按 ID、标题、DOI 的去重只覆盖已收录记录；它不证明此前检索无漏收，也不等于逐篇全文的相似性判断。Phase A/B 的摘要级判断仍需以后续阅读更新。

## 2026 正式发表核验

核心表原记录中，42 篇标为 `official venue page`，18 篇标为 `official venue or publisher page`，1 篇（`sigir26-3808571`）标为 `DOI and author PDF; publisher page inaccessible`。前 60 篇有正式会议/出版社记录。最后 1 篇虽无法直接打开出版社正文页，但其 [作者发表清单](https://mrdrozdov.github.io/publications/) 给出 SIGIR 2026、页码 2813–2823 和 DOI 10.1145/3805712.3808571，[dblp 记录](https://dblp.org/rec/conf/sigir/ArabzadehDBZ26) 也一致，因此**2026 正式发表的书目信息已得到交叉核实**；“出版社页面内容直接核对”仍为**待核**，不能把作者版等同于正式版。入选的另一篇 SIGIR 论文 CoRM-RAG（`sigir26-3809631`）也以 DOI、机构记录和作者版交叉确认；正式出版社全文未取得，表格及方法以作者版核对，版本差异保留风险。

本轮选出的 27 篇均在原池记录为 2026 年正式渠道论文；ACL/EACL、ICLR、ICML、WWW 可由官方论文集或出版社条目核验。对未能完整取得 PDF 的论文，正式发表与**正文可读性**分开记录，不能因前者成立就推断实验细节。每篇具体状态见 `selected_papers.csv` 和阅读卡。

## 审计复核方式

逐项比对 `论文ID`、`标题`、`DOI或arXiv` 和 `主要方向代码`；对入选论文查官方论文页/DOI，以及 PDF 首页的标题与会议行。ACL Anthology、[ICLR Proceedings](https://proceedings.iclr.cc/)、[PMLR ICML 2026 v306](https://proceedings.mlr.press/v306/) 和 [ACM FlowRAG 条目](https://doi.org/10.1145/3774904.3792361) 是本轮主要正式来源。作者版或 arXiv 仅用于在正式站点 PDF 不可达时阅读正文，需与正式标题核对。

## 61 篇逐条书目审计索引

下表列出全部核心记录的 2026 年份、主类和可复核论文页。`原核验记录` 是 Phase A/B 原表字段；除本轮入选 27 篇及另行查证的 SIGIR QPP 外，本轮没有重新精读其余论文全文。`官方/出版社页` 指原阶段已记录相应链接，不能代替重新打开出版社全文。

|ID|主类|2026 渠道|原核验记录|来源|
|---|---|---|---|---|
|2026.acl-long.1620|M|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.1620/)|
|2026.acl-long.939|B|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.939/)|
|2026.acl-long.1372|A|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.1372/)|
|2026.acl-industry.35|C|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-industry.35/)|
|2026.acl-long.818|M|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.818/)|
|2026.findings-acl.849|H|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.849/)|
|2026.findings-acl.414|B|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.414/)|
|2026.acl-long.1406|C|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.1406/)|
|2026.eacl-long.391|H|EACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.eacl-long.391/)|
|2026.acl-industry.60|H|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-industry.60/)|
|2026.findings-acl.1499|F|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1499/)|
|2026.eacl-long.8|H|EACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.eacl-long.8/)|
|2026.acl-long.1226|E|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.1226/)|
|2026.acl-long.192|F|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.192/)|
|2026.findings-eacl.62|E|Findings of EACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-eacl.62/)|
|2026.eacl-long.147|H|EACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.eacl-long.147/)|
|2026.acl-long.661|D|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.661/)|
|2026.eacl-srw.17|H|EACL 2026 SRW|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.eacl-srw.17/)|
|2026.findings-acl.2157|C|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.2157/)|
|2026.acl-short.14|H|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-short.14/)|
|2026.semeval-1.447|H|SemEval 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.semeval-1.447/)|
|2026.acl-long.612|F|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.612/)|
|2026.findings-acl.1571|A|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1571/)|
|2026.lrec-1.9|H|LREC 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.lrec-1.9/)|
|2026.findings-acl.1310|E|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1310/)|
|2026.findings-acl.1148|D|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1148/)|
|2026.findings-acl.2003|F|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.2003/)|
|2026.findings-acl.1834|E|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1834/)|
|2026.findings-acl.1932|B|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1932/)|
|2026.findings-acl.480|D|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.480/)|
|2026.acl-long.2218|M|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.2218/)|
|2026.findings-acl.1399|B|Findings of ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.findings-acl.1399/)|
|2026.acl-long.196|B|ACL 2026|官方/出版社页（Phase A/B）|[记录](https://aclanthology.org/2026.acl-long.196/)|
|hu26ac|G|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/hu26ac.html)|
|madhu26a|I|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/madhu26a.html)|
|sun26p|C|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/sun26p.html)|
|cui26i|D|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/cui26i.html)|
|zhao26g|M|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/zhao26g.html)|
|ki26a|L|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/ki26a.html)|
|zhao26bk|A|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/zhao26bk.html)|
|choudhary26b|H|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/choudhary26b.html)|
|taghavi26a|H|ICML 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.mlr.press/v306/taghavi26a.html)|
|iclr2026-b6f6bfbd260fbf2f5acb0a1d6439ca0e|F|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b6f6bfbd260fbf2f5acb0a1d6439ca0e-Abstract-Conference.html)|
|iclr2026-f5846131aa6a72d1df3bd6d43a4a960b|F|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f5846131aa6a72d1df3bd6d43a4a960b-Abstract-Conference.html)|
|iclr2026-5c1ff00b27ba052039bb41531236baac|A|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c1ff00b27ba052039bb41531236baac-Abstract-Conference.html)|
|iclr2026-bdff657cb9351656c025da8e1dc538a4|B|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/bdff657cb9351656c025da8e1dc538a4-Abstract-Conference.html)|
|iclr2026-c7201deff8d507a8fe2e86d34094e154|C|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c7201deff8d507a8fe2e86d34094e154-Abstract-Conference.html)|
|iclr2026-4dbcd4ba82866fdefc7ea0d15e9a72f2|F|ICLR 2026|官方/出版社页（Phase A/B）|[记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4dbcd4ba82866fdefc7ea0d15e9a72f2-Abstract-Conference.html)|
|www26-3792085|C|WWW 2026|官方/出版社页（Phase A/B）|[记录](https://dl.acm.org/doi/10.1145/3774904.3792085)|
|www26-3792093|C|WWW 2026|官方/出版社页（Phase A/B）|[记录](https://dl.acm.org/doi/10.1145/3774904.3792093)|
|www26-3792389|E|WWW 2026|官方/出版社页（Phase A/B）|[记录](https://doi.org/10.1145/3774904.3792389)|
|www26-3792361|G|WWW 2026|官方/出版社页（Phase A/B）|[记录](https://doi.org/10.1145/3774904.3792361)|
|sigir26-3808571|B|SIGIR 2026|DOI＋作者版；出版社正文不可达|[记录](https://doi.org/10.1145/3805712.3808571)|
|sigir26-3809631|C|SIGIR 2026|官方/出版社页（Phase A/B）|[记录](https://doi.org/10.1145/3805712.3809631)|
|icde26-11629265|H|ICDE 2026|官方/出版社页（Phase A/B）|[记录](https://ieeexplore.ieee.org/document/11629265/)|
|sigmod26-3786655|X|SIGMOD 2026|官方/出版社页（Phase A/B）|[记录](https://doi.org/10.1145/3786655)|
|ipm26-104369|F|Information Processing & Management 2026|官方/出版社页（Phase A/B）|[记录](https://www.sciencedirect.com/science/article/pii/S0306457325003103)|
|ipm26-104449|B|Information Processing & Management 2026|官方/出版社页（Phase A/B）|[记录](https://www.sciencedirect.com/science/article/pii/S0306457325003905)|
|ipm26-104534|B|Information Processing & Management 2026|官方/出版社页（Phase A/B）|[记录](https://www.sciencedirect.com/science/article/pii/S0306457325004753)|
|ipm26-104368|H|Information Processing & Management 2026|官方/出版社页（Phase A/B）|[记录](https://www.sciencedirect.com/science/article/pii/S0306457325003097)|
|tois26-3800948|H|ACM TOIS 2026|官方/出版社页（Phase A/B）|[记录](https://doi.org/10.1145/3800948)|
