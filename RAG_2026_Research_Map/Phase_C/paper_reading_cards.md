# Phase C 代表论文首轮阅读卡

日期：2026-10-14；仅分析 `selected_papers.csv` 中来自既有核心池的 27 篇。页码是本地 PDF 的顺序页码，不一定等于正式论文集连续页码。PMLR 部分全文采用标题一致的 arXiv 版本；CoRM-RAG 和 FlowRAG 使用作者版，版本差异风险见分类审计。

阅读范围：摘要、引言、方法及框架图的图注与相邻解释、实验总表、结论、可定位的作者局限。`UNKNOWN` 表示本轮无法由已读正文可靠核实，不能解释为事实不存在。表中“相比变化”是对作者自述与其引用前人的比较，不构成创新性评价。

## A 类

### HiChunk: Evaluating and Enhancing Retrieval Augmented Generation with Hierarchical Chunking（ACL 2026，A）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.1372/)；[本地 PDF](source_pdfs/2026.acl-long.1372.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：稀疏证据问答难以显出分块优劣；平面分块难兼顾层级信息。
- **核心方法与框架图**：HiCBench 标注多级分块和密集证据；HiChunk 用微调模型预测层级边界，Auto-Merge 查询时调整块粒度。 技术路线：层级分块＋层级检索＋专门评测。
- **相对既有工作的变化**：同时测分块、检索和回答，不只用最终 QA 分数评估分块。
- **实际数据集／指标**：QASPER；LongBench；GutenQA；OHRBench；HiCBench；分块准确率；Evidence Recall；F1；ROUGE；Fact Coverage。
- **主要对比基线**：固定长度分块 FC200；其他分块方法（Table 2/3）
- **主实验结论**：HiCBench T1 上 HC200+AM 的证据召回 81.03，高于 FC200 的 74.06（同一示例设置）；稀疏证据数据上的差距较小。
- **作者承认的局限**：更深层级训练数据稀缺且逐层预测误差累积。
- **可追溯依据**：摘要 PDF p.1；方法图 Figure 2, p.5；实验 Table 2/3, p.6–7；Limitations p.10；[全文链接](https://aclanthology.org/2026.acl-long.1372.pdf)。

### SmartChunk Retrieval: Query-Aware Chunk Compression with Planning for Efficient Document RAG（ICLR 2026，A）

正式来源：[论文页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c1ff00b27ba052039bb41531236baac-Abstract-Conference.html)；[本地 PDF](source_pdfs/iclr2026-5c1ff00b27ba052039bb41531236baac.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：静态块大小和扁平检索难同时匹配不同查询的证据粒度与成本。
- **核心方法与框架图**：SmartChunk 让规划器按查询选块抽象层级；STITCH 强化学习/模仿训练规划器；轻量压缩器生成高层块嵌入。 技术路线：查询自适应分块＋压缩嵌入。
- **相对既有工作的变化**：在查询时动态选粒度，避免反复 LLM 摘要建索引。
- **实际数据集／指标**：NarrativeQA；QASPER；QuALITY；NaturalQuestions；NewsQA（域外）；Recall@5；QA 正确性（文中 LLM judge）；F1/ROUGE；货币成本；延迟。
- **主要对比基线**：静态块策略；GraphRAG/GRAG 等结构化检索（Table 2）
- **主实验结论**：Table 2 报告在 QA 正确性和检索召回有竞争力的同时降低成本/延迟；NewsQA 有域外评测。
- **作者承认的局限**：作者说明在 QuALITY 等直接事实检索数据上 GRAG 等方法可能优于其平均表现。
- **可追溯依据**：摘要 PDF p.1；方法 Figure 2, p.4；数据/主表 Table 1/2, p.7；域外 Table 3, p.9；LIMITATION p.26；[全文链接](https://proceedings.iclr.cc/paper_files/paper/2026/file/5c1ff00b27ba052039bb41531236baac-Paper-Conference.pdf)。

### Hierarchical Abstract Tree for Cross-Document Retrieval Augmented Generation（ICML 2026，A）

正式来源：[论文页](https://proceedings.mlr.press/v306/zhao26bk.html)；[本地 PDF](source_pdfs/zhao26bk.pdf)。正式发表由官方页确认；全文采用 arXiv/作者版阅读并核对首页标题。

- **研究问题**：单文档树索引面对跨文档多跳问答时分布适应差、跨文档连接弱、抽象过粗。
- **核心方法与框架图**：Ψ-RAG 用 merge-and-collapse 构建层级抽象树，配多粒度检索 Agent 和查询重组/混合检索。 技术路线：语料级树索引＋跨文档多粒度检索。
- **相对既有工作的变化**：将树索引从单文档摘要扩到语料级跨文档证据。
- **实际数据集／指标**：NQ；PopQA；HotpotQA；2WikiMultiHopQA；MuSiQue（正文另有摘要任务）；EM；F1；Recall@2/5；ROUGE-L；索引/检索耗时。
- **主要对比基线**：RAPTOR；HippoRAG2；BM25；DPR；GraphRAG（正文设置）
- **主实验结论**：论文报告跨文档多跳 QA 优于 RAPTOR 与 HippoRAG2；表 2/3 同时报告 QA 和检索召回。
- **作者承认的局限**：UNKNOWN（本轮未定位作者独立 Limitations 声明）；不得将本文对前人不足误记为作者局限。
- **可追溯依据**：PMLR 正式条目；arXiv PDF 摘要 p.1；方法 §3；结果 Table 2/3 p.7、Table 4/5 p.8；[全文链接](https://arxiv.org/pdf/2605.00529)。

## B 类

### R^3AG: Retriever Routing for Retrieval-Augmented Generation（ACL 2026，B）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.939/)；[本地 PDF](source_pdfs/2026.acl-long.939.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：检索器路由只看文本相关性，忽略检索证据对生成器的实际帮助。
- **核心方法与框架图**：R3AG 将检索器能力分成检索质量与生成效用两种表示，用对比学习和查询自适应注意力路由。 技术路线：多检索器效用感知路由。
- **相对既有工作的变化**：路由目标从单一相关性扩到下游生成效用。
- **实际数据集／指标**：TriviaQA；Natural Questions；HotpotQA；Exact Match；F1；路由延迟。
- **主要对比基线**：E5-large；Adaptive RAG；AAR；RouterRetriever；LTRR
- **主实验结论**：平均 EM/F1 为 43.06/53.86，高于最优单检索器 E5-large 的 41.31/51.81。
- **作者承认的局限**：未联合多个检索器；仅在问答任务验证，能力表示尚较简单。
- **可追溯依据**：摘要 PDF p.1；方法 Figure 2 p.4；实验 §5/Table 2 p.6–7；Limitations p.9；[全文链接](https://aclanthology.org/2026.acl-long.939.pdf)。

### Retrieval as Generation: A Unified Framework with Self-Triggered Information Planning（ACL 2026，B）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.196/)；[本地 PDF](source_pdfs/2026.acl-long.196.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：外部控制器与生成器分离使多步检索时机和查询重写难以协同。
- **核心方法与框架图**：GRIP 把 [RETRIEVE]/[INTERMEDIARY]/[ANSWER]/[SOLVED] 控制 token 纳入自回归解码，用结构化样本监督和强化学习训练。 技术路线：生成式检索控制/自触发规划。
- **相对既有工作的变化**：由模型生成控制 token 决定检索与停止，而非外置固定策略。
- **实际数据集／指标**：HotpotQA；PopQA；Natural Questions；WebQuestions；TriviaQA；EM；F1；ROUGE；平均检索次数。
- **主要对比基线**：Single RAG；FLARE；DRAGIN；Self-RAG；GainRAG
- **主实验结论**：Table 1 报告总体分数领先所比开源基线；Table 4 显示按任务调整检索次数。
- **作者承认的局限**：对最大检索预算和证据打包方式敏感，论文将其固定。
- **可追溯依据**：摘要 PDF p.1；方法 Figure 1 p.3；Table 1 p.6、Table 4 p.7；Limitations p.10；[全文链接](https://aclanthology.org/2026.acl-long.196.pdf)。

### DeepRAG: Thinking to Retrieve Step by Step for Large Language Models（ICLR 2026，B）

正式来源：[论文页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/bdff657cb9351656c025da8e1dc538a4-Abstract-Conference.html)；[本地 PDF](source_pdfs/iclr2026-bdff657cb9351656c025da8e1dc538a4.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：复杂查询分解不准且无必要地检索会增加噪声和成本。
- **核心方法与框架图**：DeepRAG 将推理/检索建模为 MDP，经二叉树搜索合成轨迹、模仿学习及校准链，逐原子子问题选择检索或参数知识。 技术路线：多步按需检索决策。
- **相对既有工作的变化**：让每一步的知识边界决定是否查外部证据。
- **实际数据集／指标**：HotpotQA；2WikiMultiHopQA；PopQA；WebQuestions；MuSiQue；回答正确率/EM/F1；检索次数；时间。
- **主要对比基线**：Adaptive-RAG；FLARE；DRAGIN（正文比较组）
- **主实验结论**：摘要及结论报告回答准确率提升 25.41% 并提高检索效率；具体比较口径见 Table 1。
- **作者承认的局限**：UNKNOWN（正文未找到作者独立 Limitations 段）；不把相关工作缺点代替作者声明。
- **可追溯依据**：摘要 PDF p.1；方法 Figure 2 p.3；实验 Table 1 p.7；Conclusion p.10；[全文链接](https://proceedings.iclr.cc/paper_files/paper/2026/file/bdff657cb9351656c025da8e1dc538a4-Paper-Conference.pdf)。

### Masking or Mitigating? Deconstructing the Impact of Query Rewriting on Retriever Biases in RAG（Findings of ACL 2026，B）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.414/)；[本地 PDF](source_pdfs/2026.findings-acl.414.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：查询改写已常用，但对稠密检索器长度、位置、字面匹配、重复偏差的作用不清。
- **核心方法与框架图**：在 ColDeR 成对文档上比较五种查询增强和六种检索器；用成对统计量区分简单改写与伪文档扩展机制。 技术路线：查询改写偏差诊断（实证）。
- **相对既有工作的变化**：不只报 QA 分数，而拆解检索偏差及其查询侧可修正范围。
- **实际数据集／指标**：ColDeR（源自 Re-DocRED）；四类偏差配对样本；平均 |t|；显著偏差数；偏差降幅。
- **主要对比基线**：原始查询；简单 LLM 改写；HyDE；Query2Doc 等增强策略
- **主实验结论**：简单改写平均偏差下降 54%，但多个偏差共同出现时仍失效；方法效应因检索器而异。
- **作者承认的局限**：受控成对样本难完全代表真实混合偏差；未覆盖稀疏/混合检索器。
- **可追溯依据**：摘要 PDF p.1；数据 Table 1 p.4；结果 Table 2 p.5；Limitations p.9；[全文链接](https://aclanthology.org/2026.findings-acl.414.pdf)。

## C 类

### Optimizing RAG Rerankers with LLM Feedback via Reinforcement Learning（ACL 2026，C）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.1406/)；[本地 PDF](source_pdfs/2026.acl-long.1406.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：传统重排器用人工相关性标签，未直接优化生成答案质量。
- **核心方法与框架图**：RRPO 将重排视为序列决策，用生成器反馈奖励训练，并以参考锚定确定性基线稳定更新。 技术路线：生成效用驱动的强化学习重排。
- **相对既有工作的变化**：从文档相关性学习转为下游回答效用优化。
- **实际数据集／指标**：HotpotQA；AmbigNQ；2WikiMultiHopQA；EM；F1；Hit/奖励。
- **主要对比基线**：Naive RAG；RankZephyr；预训练重排器
- **主实验结论**：Table 1/2 报告优于 RankZephyr 等强重排器，并在 2Wiki 上验证迁移。
- **作者承认的局限**：候选池召回若过低，重排无法补回未检索到的证据。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.2；Table 1 p.6、Table 2 p.7；Limitations p.9；[全文链接](https://aclanthology.org/2026.acl-long.1406.pdf)。

### Rethinking the Reranker: Boundary-Aware Evidence Selection for Robust Retrieval-Augmented Generation（ICML 2026，C）

正式来源：[论文页](https://proceedings.mlr.press/v306/sun26p.html)；[本地 PDF](source_pdfs/sun26p.pdf)。正式发表由官方页确认；全文采用 arXiv/作者版阅读并核对首页标题。

- **研究问题**：高相关证据可能过易或根本不足，不能给生成器稳定的学习信号。
- **核心方法与框架图**：BAR-RAG 用生成器反馈训练边界感知证据选择器，再在该证据分布下训练生成器，选择困难但可解的组合。 技术路线：证据难度边界选择＋两阶段强化学习。
- **相对既有工作的变化**：不再以相关性最高为唯一准则，同时处理选择器—生成器分布偏移。
- **实际数据集／指标**：Natural Questions；TriviaQA；PopQA；HotpotQA；Top-K QA accuracy；检索召回；不同 K 的鲁棒性。
- **主要对比基线**：标准 RAG；相关性重排器（详细列表见实验节）
- **主实验结论**：Figure 4 显示在四个 QA 集、两个生成器上低 K 准确率更高且 K 增大时更稳。
- **作者承认的局限**：UNKNOWN（本轮未定位作者明确局限性段落）。
- **可追溯依据**：PMLR 正式条目；arXiv PDF 摘要 p.1；方法 Figure 3 p.3；结果 Figure 4 p.7；[全文链接](https://arxiv.org/pdf/2602.03689)。

### NEST: Nested Evidence Survival for Retrieval（ACL 2026，C）

正式来源：[论文页](https://aclanthology.org/2026.acl-industry.35/)；[本地 PDF](source_pdfs/2026.acl-industry.35.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：极高噪声下固定 top-k 提前剪掉稀少有效证据，迭代控制器又增加代价。
- **核心方法与框架图**：NEST 先在嵌套检索范围内保留候选，再用跨范围稳定的倒数排名选择去冗余。 技术路线：无训练的召回扩展＋生存一致性筛选。
- **相对既有工作的变化**：将“先保召回”和“后控精度”明确分开。
- **实际数据集／指标**：WebQuestions；HotpotQA distractor；InternalQA＋50M Common Crawl 干扰项；EM；F1；Recall@50；冗余度；延迟。
- **主要对比基线**：Vanilla RAG；AutoRAG；DeepRAG
- **主实验结论**：Table 2：Recall@50 为 84.9，对 DeepRAG 的 78.1；额外延迟约 12–18 ms；消融移除 NES 后 WebQuestions EM 62.8→54.1。
- **作者承认的局限**：若基础检索器在较粗范围完全未取到相关候选，NEST 无法恢复；极低延迟场景仍有开销。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.3；Table 1/2/3 p.6；Limitations p.6；[全文链接](https://aclanthology.org/2026.acl-industry.35.pdf)。

### Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation（SIGIR 2026，C）

正式来源：[论文页](https://doi.org/10.1145/3805712.3809631)；[本地 PDF](source_pdfs/sigir26-3809631.pdf)。DOI 与机构记录确认；全文为作者版；出版社正文未取得。

- **研究问题**：语义相关文档未必能抵抗带认知偏差的查询，错误证据可能诱导生成错误。
- **核心方法与框架图**：CoRM-RAG 对查询施加认知扰动、由教师模型给证据稳健分数，训练 Evidence Critic；推理时风险感知重排并可弃答。 技术路线：反事实风险训练＋证据审查/选择性回答。
- **相对既有工作的变化**：排序对象从主题相关性变为偏差扰动下仍支持正确结论的证据。
- **实际数据集／指标**：Biased-NQ；TruthfulQA；回答准确率；选择性准确率/覆盖率；Recall@k；推理延迟。
- **主要对比基线**：BM25；Contriever；Cross-Encoder；LLM-Rerank
- **主实验结论**：作者版 Figure 4 报告 Biased-NQ 中 Recall@k 对基线有优势；正文还比较覆盖率—风险曲线。数值与口径以作者版 Table 1 为准。
- **作者承认的局限**：UNKNOWN（作者版未定位独立 Limitations）；正式 ACM 全文未取得，存在版本差异可能。
- **可追溯依据**：[DOI 正式条目](https://doi.org/10.1145/3805712.3809631)；作者版 PDF Figure 2 p.4、Table 1 p.7、Figure 3/4 p.8–9；[全文链接](https://arxiv.org/pdf/2605.01302)。

## D 类

### SARA: Selective and Adaptive Retrieval-augmented Generation with Context Compression（ACL 2026，D）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.661/)；[本地 PDF](source_pdfs/2026.acl-long.661.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：激进文本压缩会丢失实体和数字，而全量证据又超过有效上下文预算。
- **核心方法与框架图**：SARA 保留少量自然语言片段，把其余证据编码为可学习压缩向量，并据此迭代重排。 技术路线：文本片段＋软压缩向量混合上下文。
- **相对既有工作的变化**：兼顾局部细节与更广证据覆盖，而非只做纯文本摘要或纯向量压缩。
- **实际数据集／指标**：QASPER；NarrativeQA；TriviaQA；QuALITY；HotpotQA 等共 9 集；F1；答案相关性；正确性；语义相似度；token 预算。
- **主要对比基线**：Vanilla RAG；ICAE；LLMLingua；LongLLMLingua；CompAct
- **主实验结论**：摘要报告相关性 +17.71、正确性 +13.72、语义相似度 +15.53；Table 1 比较多个 QA 集。
- **作者承认的局限**：压缩向量对数字与实体等细节的保真度随上下文变化。
- **可追溯依据**：摘要 PDF p.1；Figure 1/2 p.2–3；Table 1 p.6；Limitations p.9；[全文链接](https://aclanthology.org/2026.acl-long.661.pdf)。

### AED-RAG: Continuous Multi-Granular Context Fusion for Retrieval-Augmented Generation via Adaptive Ensemble Decoding（Findings of ACL 2026，D）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.1148/)；[本地 PDF](source_pdfs/2026.findings-acl.1148.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：粗粒度段落混入噪声，离散重排也难在生成时融合段落、三元组和模型内部知识。
- **核心方法与框架图**：AED-RAG 用对比困惑度训练效用预测器，推理时给不同信息源赋权，逐 token 融合输出分布。 技术路线：多粒度证据的自适应集成解码。
- **相对既有工作的变化**：从一次性选择单段落转为按 token 软融合三种来源。
- **实际数据集／指标**：HotpotQA；Natural Questions；TriviaQA；WebQuestions；EM；F1；平均分。
- **主要对比基线**：硬选择重排方法；标准 RAG；其他集成解码方法（Table 1）
- **主实验结论**：Table 1 在四个开放域 QA 集上报告领先多数所比方法。
- **作者承认的局限**：只研究单段落信息源；检索条数固定；尚缺大规模语料验证。
- **可追溯依据**：摘要 PDF p.1；Figure 2 p.3；Table 1 p.6；Limitations p.9；[全文链接](https://aclanthology.org/2026.findings-acl.1148.pdf)。

### Less Is More: Elevating RAG via Performance-Driven Context Compression（ICML 2026，D）

正式来源：[论文页](https://proceedings.mlr.press/v306/cui26i.html)；[本地 PDF](source_pdfs/cui26i.pdf)。正式发表由官方页确认；全文采用 arXiv/作者版阅读并核对首页标题。

- **研究问题**：按预设启发式压缩上下文易伤害下游回答，且难同时控制 token 成本。
- **核心方法与框架图**：CORE-RAG 先知识蒸馏初始化压缩器，再用最终问答任务表现反馈迭代优化压缩策略。 技术路线：性能驱动上下文压缩。
- **相对既有工作的变化**：以生成任务效果而非代理压缩指标指导压缩。
- **实际数据集／指标**：Natural Questions；TriviaQA；HotpotQA；2WikiMultiHopQA；EM/F1；压缩比/输入 token；问答效能。
- **主要对比基线**：全上下文 RAG；BM25；现有压缩方法（Table 1）
- **主实验结论**：作者在主表报告压缩后仍可超过若干未压缩或现有压缩基线；精确差值在本轮提取版中未可靠核对，记 UNKNOWN。
- **作者承认的局限**：UNKNOWN（本轮未定位作者明确局限性声明）。
- **可追溯依据**：[PMLR 正式条目](https://proceedings.mlr.press/v306/cui26i.html)；arXiv PDF 摘要 p.1、Figure 2 p.4、实验 §4/Table 1 p.6；[全文链接](https://arxiv.org/pdf/2508.19282)。

## E 类

### Think Parallax: Solving Multi-Hop Problems via Multi-View Knowledge-Graph-Based Retrieval-Augmented Generation（ACL 2026，E）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.1226/)；[本地 PDF](source_pdfs/2026.acl-long.1226.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：KG-RAG 把多跳语义折叠进一个嵌入空间，导致路径搜索噪声和偏移。
- **核心方法与框架图**：ParallaxRAG 将查询/知识图谱三元组投到对齐的多头语义空间，利用头间差异约束和聚合选择子图。 技术路线：多视角知识图谱检索。
- **相对既有工作的变化**：显式利用不同 attention head 的多跳关系分工，而非平面单视角匹配。
- **实际数据集／指标**：WebQSP；CWQ；BioASQ；路径三元组召回；答案实体召回；QA 分数；幻觉率。
- **主要对比基线**：RoG；G-Retriever；GNN-RAG；StructGPT；ToG
- **主实验结论**：Table 1/2 在 WebQSP 和 CWQ 上报告检索与 QA 改进；Table 4 在 BioASQ 测跨域迁移。
- **作者承认的局限**：UNKNOWN（未定位作者独立 Limitations 段）。
- **可追溯依据**：摘要 PDF p.1；Figure 2 p.3；Table 1 p.5、Table 2 p.6、Table 4 p.8；[全文链接](https://aclanthology.org/2026.acl-long.1226.pdf)。

### Beyond Chunks and Graphs: Retrieval-Augmented Generation through Triplet-Driven Thinking（Findings of ACL 2026，E）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.1310/)；[本地 PDF](source_pdfs/2026.findings-acl.1310.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：多轮检索 LLM 调用昂贵，图式 RAG 的图构建冗余且易错。
- **核心方法与框架图**：T2RAG 建无图的原子三元组库；把问题拆成带占位符的查询三元组，逐轮检索填槽并作答。 技术路线：三元组驱动的无图多跳检索。
- **相对既有工作的变化**：用结构化原子事实和迭代填槽替代显式图遍历。
- **实际数据集／指标**：PopQA；2WikiMultiHopQA；MuSiQue；HotpotQA；Story；Medical；EM；F1；检索成本/时间；token 成本。
- **主要对比基线**：HippoRAG2；IRCoT；BM25；其他多轮/Graph RAG
- **主实验结论**：摘要报告六集平均性能最多提高约 11%、检索成本最多降低约 45%；Table 1 为主要结果。
- **作者承认的局限**：作者局限指出三元组抽取错误（如过度切分）及多跳实验覆盖等问题；具体实验限制见 Appendix D.1。
- **可追溯依据**：摘要 PDF p.1；在线流程 Figure 2 p.5；Table 1 p.8；Limitations/Appendix D.1 p.21；[全文链接](https://aclanthology.org/2026.findings-acl.1310.pdf)。

### Reasoning with Memory: Adaptive Information Management for Retrieval-Augmented Generation（Findings of ACL 2026，E）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.1834/)；[本地 PDF](source_pdfs/2026.findings-acl.1834.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：多跳检索链增长时中间推理状态不连贯，相关信息难跨轮保留。
- **核心方法与框架图**：State-Aware RAG 在 MCTS 检索/生成循环里维护工作记忆；轻量 extractor 以路径—结果双奖励学习过滤、整合、更新状态。 技术路线：显式工作记忆＋搜索式多跳推理。
- **相对既有工作的变化**：把记忆更新作为独立可训练组件，检索器与生成器冻结。
- **实际数据集／指标**：2WikiMultiHopQA；HotpotQA；MuSiQue；Bamboogle 等共 8 集；substring EM；LLM judge Accuracy；多跳 QA 分数。
- **主要对比基线**：记忆增强 RAG；RL 增强 RAG；SimpleDeepSearcher 等（Table 1）
- **主实验结论**：摘要报告相对最强记忆增强基线平均 +8.6%、相对最强 RL 增强基线 +9.3%。
- **作者承认的局限**：双奖励的 LLM judge 带来较高训练推理成本；基础检索质量限制整体上限。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.2、Figure 2 p.3；Table 1 p.6；Limitations p.9；[全文链接](https://aclanthology.org/2026.findings-acl.1834.pdf)。

## F 类

### Guaranteeing Knowledge Integration with Joint Decoding for Retrieval-Augmented Generation（ACL 2026，F）

正式来源：[论文页](https://aclanthology.org/2026.acl-long.192/)；[本地 PDF](source_pdfs/2026.acl-long.192.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：检索到正确证据后，生成器仍可能被自身参数知识带偏。
- **核心方法与框架图**：GUARANTRAG 分开生成内部知识答案和基于证据答案；对后者做对比 DPO，最后以联合解码融合逻辑与事实。 技术路线：参数知识—外部证据冲突的双流解码。
- **相对既有工作的变化**：把证据抽取与原有推理流分离后再融合，而非一次生成内隐处理。
- **实际数据集／指标**：Natural Questions；TruthfulQA；Wizard of Wikipedia；HotpotQA；ELI5；QA 准确性；幻觉率；证据使用/一致性指标。
- **主要对比基线**：Standard RAG；Self-RAG；RQ-RAG；SOLAR；DA-RAG
- **主实验结论**：摘要报告准确率最多 +12.1%、幻觉率下降 16.3%；Table 1 为五集主结果。
- **作者承认的局限**：双答案和联合解码增加时延；跨专业领域可能不稳；DPO 超参需调节。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.3；§4/Table 1 p.4–6；Limitations p.9；[全文链接](https://aclanthology.org/2026.acl-long.192.pdf)。

### Rational Synthesizers or Heuristic Followers? Analyzing LLMs in RAG-based Question-Answering（Findings of ACL 2026，F）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.2003/)；[本地 PDF](source_pdfs/2026.findings-acl.2003.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：多篇互相冲突的检索文档如何共同影响答案，不能由单对文档冲突试验解释。
- **核心方法与框架图**：GroupQA 收集争议问题与立场标注证据，在数量、改写冗余、顺序、冲突程度上做受控干预。 技术路线：证据群组整合的诊断基准。
- **相对既有工作的变化**：由单条证据转向文档组内重复、顺序和冲突的因果式对照。
- **实际数据集／指标**：GroupQA：1,635 个问题、15,058 篇/段证据文档；回答立场/概率变化；先验稳定性；顺序和冗余敏感性。
- **主要对比基线**：不提供算法性能强基线；主要比较受控证据排列和数量条件
- **主实验结论**：改写重复证据可能比独立证据更能影响答案；先呈证据更有影响，模型说明并不总忠实。
- **作者承认的局限**：UNKNOWN（本轮未定位独立 Limitations 段）。
- **可追溯依据**：摘要 PDF p.1；数据 Table 1 p.3；受控实验 Figure 1 p.1、Figure 3 p.5；Conclusion p.9；[全文链接](https://aclanthology.org/2026.findings-acl.2003.pdf)。

### Resisting Contextual Interference in RAG via Parametric-Knowledge Reinforcement（ICLR 2026，F）

正式来源：[论文页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4dbcd4ba82866fdefc7ea0d15e9a72f2-Abstract-Conference.html)；[本地 PDF](source_pdfs/iclr2026-4dbcd4ba82866fdefc7ea0d15e9a72f2.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：错误、无关或冲突检索文本会使模型过度信任外部证据。
- **核心方法与框架图**：Knowledgeable-R1 用有/无检索配对采样和局部/全局优势估计强化训练，学习什么时候依赖参数知识、什么时候吸收上下文。 技术路线：抗证据干扰的策略优化。
- **相对既有工作的变化**：显式训练在不同证据可靠性状态间切换。
- **实际数据集／指标**：HotpotQA；2WikiMultiHopQA；MuSiQue；ConFiQA；ExplainPE；五类上下文场景；QA 准确率；冲突/反事实场景准确率。
- **主要对比基线**：RAG prompting；GRPO w/ RAG；其他上下文冲突方法（Table 2）
- **主实验结论**：摘要报告反事实场景相对强基线提高 22.89%，完整正确证据时未见退化。
- **作者承认的局限**：作者指出尚未细分混合上下文中错误证据比例变化的影响。
- **可追溯依据**：摘要 PDF p.1；方法 §3；Table 2 p.8；Limitations p.11；[全文链接](https://proceedings.iclr.cc/paper_files/paper/2026/file/4dbcd4ba82866fdefc7ea0d15e9a72f2-Paper-Conference.pdf)。

### Toward Faithful Retrieval-Augmented Generation with Sparse Autoencoders（ICLR 2026，F）

正式来源：[论文页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b6f6bfbd260fbf2f5acb0a1d6439ca0e-Abstract-Conference.html)；[本地 PDF](source_pdfs/iclr2026-b6f6bfbd260fbf2f5acb0a1d6439ca0e.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：RAG 幻觉检测若依赖外部大模型评审昂贵，纯内部表征探针又不够准。
- **核心方法与框架图**：RAGLens 从稀疏自编码器特征中选出幻觉相关信号，组合轻量检测器，并用特征解释做事后缓解。 技术路线：模型内部稀疏特征的忠实性检测。
- **相对既有工作的变化**：检测依据由输出文本/外部 judge 转为内部可解释激活。
- **实际数据集／指标**：RAGTruth；Dolly；AUROC；幻觉率；跨数据集迁移。
- **主要对比基线**：已有幻觉检测器；LLM 评审方法（Table 1）
- **主实验结论**：Table 1/2 报告检测性能与跨集泛化；Table 4 报告加入反馈后幻觉率变化。
- **作者承认的局限**：UNKNOWN（本轮未定位作者独立 Limitations 声明）；方法要求获得内部激活。
- **可追溯依据**：摘要 PDF p.1；方法 §3；Table 1 p.6、Table 2 p.7、Table 4 p.9；Conclusion p.10；[全文链接](https://proceedings.iclr.cc/paper_files/paper/2026/file/b6f6bfbd260fbf2f5acb0a1d6439ca0e-Paper-Conference.pdf)。

## G 类

### RAG without Forgetting: Continual Query-Infused Key Memory（ICML 2026，G）

正式来源：[论文页](https://proceedings.mlr.press/v306/hu26ac.html)；[本地 PDF](source_pdfs/hu26ac.pdf)。正式发表由官方页确认；全文采用 arXiv/作者版阅读并核对首页标题。

- **研究问题**：查询时扩展可改善检索但每次重做且不积累；静态索引扩展可能漂移。
- **核心方法与框架图**：Evolving Retrieval Memory/ERM 以答案正确性反馈门控，把有效查询扩展的原子信号归因到文档检索 key，逐批更新索引。 技术路线：训练自由的持续检索键记忆。
- **相对既有工作的变化**：把瞬时查询改写收益持久化为可验证的索引更新。
- **实际数据集／指标**：BEIR/BRIGHT 等 13 个数据集；nDCG@1/5/10；Recall@5/10；MRR；延迟。
- **主要对比基线**：原始检索；HyDE；查询改写；静态 key expansion
- **主实验结论**：Figure 3 报告 ERM 在接近原生检索时延下达到或超过部分查询扩展效果；分集结果见正文和附录。
- **作者承认的局限**：UNKNOWN（本轮未定位作者明确局限性段）。
- **可追溯依据**：[PMLR 正式条目](https://proceedings.mlr.press/v306/hu26ac.html)；arXiv PDF 摘要 p.1；方法 §3；Figure 3 p.7；附录 Table 3 p.16；[全文链接](https://arxiv.org/pdf/2602.05152)。

### FlowRAG: Continual Learning for Dynamic Retriever in Retrieval-Augmented Generation（WWW 2026，G）

正式来源：[论文页](https://doi.org/10.1145/3774904.3792361)；[本地 PDF](source_pdfs/www26-3792361.pdf)。ACM 正式页确认；全文采用作者版阅读。

- **研究问题**：持续到来的新语料会使经生成器监督的检索器遗忘旧域，整网重训代价高。
- **核心方法与框架图**：FlowRAG 在编码器各层插入可训练 prompt 嵌入，以跨层融合加生成器引导的损失持续调整检索器。 技术路线：参数高效持续学习检索器。
- **相对既有工作的变化**：在跨域序列更新中保持旧域检索质量，同时把生成效用纳入检索损失。
- **实际数据集／指标**：ConvQA；CovidQA；NewsQA；Natural Questions；ACC@5；F1；Forgetting Score；可训练参数比例。
- **主要对比基线**：Contriever；L2R；REPLUG；End2EndRAG；Atlas
- **主实验结论**：正文报告平均 ACC@5 35.96%、F1 32.00%，优于 L2R 约 6.95/4.7 个百分点；仅更新约 0.64% 参数。
- **作者承认的局限**：UNKNOWN（作者 PDF 未定位独立 Limitations 段）。
- **可追溯依据**：[ACM 正式条目](https://doi.org/10.1145/3774904.3792361)；作者版 PDF 摘要 p.1；方法 §4；Table 1 p.6、Table 2 p.6；Conclusion p.8；[全文链接](https://me.sage.org.ai/contents/research_papers/2026/2026_flowrag_www_2026.pdf)。

## H 类

### RAG in the Wild: On the (In)effectiveness of LLMs with Mixture-of-Knowledge Retrieval Augmentation（Findings of ACL 2026，H）

正式来源：[论文页](https://aclanthology.org/2026.findings-acl.849/)；[本地 PDF](source_pdfs/2026.findings-acl.849.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：Wikipedia 式基准难反映多源异质语料下真实 RAG 的收益和路由难度。
- **核心方法与框架图**：用 MASSIVE DS 混合知识源评估检索、重排与提示式语料路由的贡献。 技术路线：真实异质知识源的 RAG 实证评测。
- **相对既有工作的变化**：从单语料问答转向多源知识环境与模型规模差异。
- **实际数据集／指标**：MMLU；MMLU-Pro；ARC-Challenge 等六个数据集；MASSIVE DS；QA accuracy；检索带来的相对增益；来源路由表现。
- **主要对比基线**：无检索；单语料检索；全部语料检索；重排器
- **主实验结论**：Table 1 显示检索对较小模型收益更明显；大模型部分领域边际收益小或为负。
- **作者承认的局限**：侧重短答案 QA；未评估运行时延；大规模模型覆盖有限。
- **可追溯依据**：摘要 PDF p.1；实验 §2/Table 1 p.2；Figure 1 p.3；Limitations p.5；[全文链接](https://aclanthology.org/2026.findings-acl.849.pdf)。

### Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems（EACL 2026，H）

正式来源：[论文页](https://aclanthology.org/2026.eacl-long.147/)；[本地 PDF](source_pdfs/2026.eacl-long.147.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：真实 RAG 误答可来自分块、检索、重排或生成，缺少可操作的错误归因分类。
- **核心方法与框架图**：提出分阶段错误类型、人工标注错误数据和自动分类器 RAGEC，并根据诊断作针对性系统调整。 技术路线：流水线级错误分类与自动评测。
- **相对既有工作的变化**：从总体正确率转向具体故障阶段及类型。
- **实际数据集／指标**：DragonBall-EN；CLAPnq（正文评测）；与人工阶段标注的一致性；错误类型分布。
- **主要对比基线**：人工标注作为参照；无明确算法性强基线
- **主实验结论**：Table 1 给出自动阶段分类与人工标注的混淆矩阵，作者结论认为一致性有用但远非完美。
- **作者承认的局限**：分类表不穷尽所有流水线；展示用 RAG 管线未针对测试集精调。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.2；Table 1 p.7；Conclusion p.9；Limitations p.10；[全文链接](https://aclanthology.org/2026.eacl-long.147.pdf)。

### T^{2}-RAGBench: Text-and-Table Benchmark for Evaluating Retrieval-Augmented Generation（EACL 2026，H）

正式来源：[论文页](https://aclanthology.org/2026.eacl-long.8/)；[本地 PDF](source_pdfs/2026.eacl-long.8.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：文本＋表格数值问答的现有数据常给 oracle context，不能检验真正检索后推理。
- **核心方法与框架图**：T2-RAGBench 将既有表格问答重写为上下文独立问题，形成需要先检索再计算的 23,088 个三元组，并做人类复核。 技术路线：文本表格混合检索评测基准。
- **相对既有工作的变化**：从给定正确上下文转向未知上下文的端到端检索—数值推理。
- **实际数据集／指标**：FinQA；ConvFinQA；TAT-DQA 来源；T2-RAGBench 23,088 样本；检索命中/排序质量；最终答案准确率；人工问题独立性。
- **主要对比基线**：BM25；稠密检索；Hybrid BM25；多种 RAG 组合
- **主实验结论**：专家抽查 91.3% 问题具上下文独立性；Hybrid BM25 在其检索比较中最佳，但整个任务仍困难。
- **作者承认的局限**：问题合成可能不代表真实用户提问；人工抽查不能保证所有重写问题同义。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.1；Table 1/2 p.3–4；实验 §5；Limitations p.9；[全文链接](https://aclanthology.org/2026.eacl-long.8.pdf)。

### Redefining Retrieval Evaluation in the Era of LLMs（EACL 2026，H）

正式来源：[论文页](https://aclanthology.org/2026.eacl-long.391/)；[本地 PDF](source_pdfs/2026.eacl-long.391.pdf)。官方论文集 PDF 正文已读。

- **研究问题**：nDCG/MAP/MRR 的人类位置折扣和相关性假设不能准确预测 LLM 消费证据后的回答质量。
- **核心方法与框架图**：定义证据正效用与干扰负效用标签，构造 UDCG 及 LLM 导向位置折扣，以相关性至端到端正确率的对应程度评估。 技术路线：面向生成器的检索效用指标。
- **相对既有工作的变化**：将干扰文档的伤害和非单调位置效应纳入检索指标。
- **实际数据集／指标**：Natural Questions；TriviaQA；PopQA；BioASQ；NoMIR；Spearman 相关；QA accuracy；弃答/错误比例。
- **主要对比基线**：nDCG；MAP；MRR；eRAG；二值相关指标
- **主实验结论**：摘要报告对端到端准确率的相关性最多比传统指标高 36%；Figure 1 展示位置效应错配。
- **作者承认的局限**：仅验证可核答案 QA；效用标注需访问输出概率，对黑箱 API 不适用。
- **可追溯依据**：摘要 PDF p.1；Figure 1 p.4；实验 §7/Table 3 p.7–8；Limitations p.9；[全文链接](https://aclanthology.org/2026.eacl-long.391.pdf)。
