import csv
from pathlib import Path

ROOT = Path(r"E:\AgentBackdoorAttack\RAG_2026_Research_Map")
OUT = ROOT / "Phase_C"
OUT.mkdir(exist_ok=True)
selection = [
("A","2026.acl-long.1372","分块质量与层次检索同时评测；含专门基准"),
("A","iclr2026-5c1ff00b27ba052039bb41531236baac","按查询规划块抽象层级；与静态分块形成对照"),
("A","zhao26bk","跨文档抽象树与多粒度检索；检验层次索引的跨文档能力"),
("B","2026.acl-long.939","路由不同检索器；覆盖检索器选择"),
("B","2026.acl-long.196","生成过程中自触发检索；覆盖检索时机控制"),
("B","iclr2026-bdff657cb9351656c025da8e1dc538a4","任务分解与逐步检索；覆盖多步决策"),
("B","2026.findings-acl.414","检验查询改写对检索器偏差的影响；覆盖查询处理诊断"),
("C","2026.acl-long.1406","用生成反馈优化重排器；覆盖生成效用目标"),
("C","sun26p","边界感知证据选择；覆盖检索噪声和证据充分性"),
("C","2026.acl-industry.35","极端噪声下证据保留；覆盖工业噪声场景"),
("C","sigir26-3809631","反事实风险最小化证据选择；覆盖风险感知"),
("D","2026.acl-long.661","选择性压缩与细节保留；覆盖输入上下文预算"),
("D","2026.findings-acl.1148","多粒度上下文融合与自适应解码；覆盖证据融合"),
("D","cui26i","按下游性能训练压缩器；覆盖任务效用型压缩"),
("E","2026.acl-long.1226","多视角知识图谱检索；覆盖关系/路径推理"),
("E","2026.findings-acl.1310","三元组驱动推理；与图索引及分块检索对照"),
("E","2026.findings-acl.1834","中间记忆状态管理；覆盖长链条推理"),
("F","2026.acl-long.192","联合解码促进检索知识整合；覆盖生成阶段机制"),
("F","2026.findings-acl.2003","冲突证据使用机制分析；覆盖诊断型研究"),
("F","iclr2026-4dbcd4ba82866fdefc7ea0d15e9a72f2","参数知识与错误上下文的冲突控制；覆盖训练型方案"),
("F","iclr2026-b6f6bfbd260fbf2f5acb0a1d6439ca0e","SAE 表征检测不忠实输出；覆盖可解释检测"),
("G","hu26ac","持续更新检索键；覆盖索引侧反馈积累"),
("G","www26-3792361","动态语料下持续适配检索器；覆盖参数侧增量更新"),
("H","2026.findings-acl.849","混合知识检索场景中评估 RAG；覆盖真实分布"),
("H","2026.eacl-long.147","错误类型与阶段归因；覆盖失败诊断"),
("H","2026.eacl-long.8","文本与表格联合 RAG 基准；覆盖复杂文档"),
("H","2026.eacl-long.391","面向生成消费方式重定义检索评测；覆盖指标设计"),
]
override = {"sigir26-3809631":"https://arxiv.org/pdf/2605.01302"}
with (ROOT/"rag_core_papers.csv").open(encoding="utf-8-sig",newline="") as f:
    pool={r["论文ID"]:r for r in csv.DictReader(f)}
assert len(selection)==27 and len({i for _,i,_ in selection})==27
counts={x:sum(d==x for d,_,_ in selection) for x in "ABCDEFGH"}
assert counts==dict(zip("ABCDEFGH",[3,4,4,3,3,4,2,4])),counts
rows=[]
for direction,pid,reason in selection:
    r=pool[pid]
    assert r["主要方向代码"]==direction,(pid,direction,r["主要方向代码"])
    rows.append({
        "序号":len(rows)+1,"方向代码":direction,"论文ID":pid,"标题":r["标题"],"发表渠道":r["发表渠道"],
        "发表类型":r["发表类型"],"DOI或arXiv":r["DOI或arXiv"],"官方论文地址":r["官方论文地址"],
        "PDF地址":override.get(pid,r["PDF地址"]),"选择理由":reason,"正式发表核验":"待逐篇复核",
        "PDF取得状态":"待获取","阅读状态":"待阅读","保留/替换说明":"首轮入选"
    })
columns=list(rows[0])
with (OUT/"selected_papers.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
print(f"selected={len(rows)} counts={counts}")
