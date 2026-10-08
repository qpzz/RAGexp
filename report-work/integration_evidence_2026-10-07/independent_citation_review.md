# 整合稿独立引文核验记录

核验日期：2026-10-07。核验对象：`Agent后门攻击_七大方向十二子方向_文献脉络与攻防问题整合稿_2026-10-07.md`。本记录仅核验26篇引用的身份与已有研究事实，不评判拟研究机制是否已经实验证实，不扩展选题，也未修改主稿。

## 核验方式与结论边界

独立读取26份本地 PDF 首页面题名、作者、版本标识与出版页脚，并读取相关方法、限制和附录；全文提取仅用于定位，没有采用已有 evidence_map 的判定作为证据。对本地预印本无法证明的正式出版身份、MemMorph 的 under review 状态和 GhostSplice 的公开披露名称，进行了限定在这些文献的官方来源核验。没有重新开展全面查新。

主稿正文与文末参考文献均含26个不同编号，集合完全一致：8、12、13、16、19、20、21、22、23、24、25、26、27、28、32、33、34、35、36、37、38、41、45、48、54、56。没有孤立正文引用，也没有未使用的文末条目。继承原报告的不连续编号符合本次材料对照用途，未作为正式 IEEE 排序错误处理。

26篇论文身份均能对应；未发现虚构论文或错配 arXiv 标识。主要研究描述有原文支持。核验期间发现并反馈了 MCPTox 本地版本备注错误，以及 OEP 批量经验覆盖、MemoRepair 参数修复分支和 TMA-NM 保证范围的澄清需要。父任务已完成这些修订，并补入GhostSplice作者官方披露/仓库链接。最终核验当前主稿通过，未发现其他必改的论文身份或已有研究事实错误。下表中的“支持”表示稿件的概括符合所核查原文，不表示该论文的全部结论可无条件推广。

最终核验所读主稿文件 SHA-256：`d1067624a6849bd8f953ece21355efd322c3e0e5487f4726c64d4a3ad9794447`。本记录不对之后的改动作自动追认。

## 逐条身份与支撑核验

| 编号 | 独立确认的论文身份/本地版本 | 主稿已有研究描述的证据与结论 |
|---|---|---|
| [8] | Rathbun、Amato、Oprea；*SleeperNets: Universal Backdoor Poisoning Attacks Against Reinforcement Learning Agents*。本地 arXiv:2405.20539v2，2024-10-21；正式 NeurIPS 2024 身份由出版方页面确认。 | PDF p1 摘要明确 training-time RL backdoor poisoning、奖励投毒、推理时触发目标动作。8.1将其限定为训练型历史背景正确；不能据此证明推理时记忆污染效果。 |
| [12] | Yao等，*ReAct: Synergizing Reasoning and Acting in Language Models*；arXiv:2210.03629v3，首页面明确 ICLR 2023 conference paper。 | PDF p1摘要描述交替生成 reasoning traces 与 actions，通过外部知识库/环境补充观察。7.1概括有支持；该文不直接研究持久记忆后门，稿件已正确区分。 |
| [13] | Shinn等，*Reflexion: Language Agents with Verbal Reinforcement Learning*；正式 PDF 首页面 NeurIPS 2023 页脚。 | PDF p1摘要明确不更新权重，而是语言反馈、反思文本和 episodic memory buffer，改善 subsequent trials。7.1有支持；不能从语言强化名称误认成需要参数训练。 |
| [16] | Chen等，*AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases*；NeurIPS 2024正式 PDF。 | PDF p1摘要及威胁模型支持长期记忆/RAG库投毒、优化检索触发器、触发查询检索恶意示范，且无需额外训练或微调。5.1将其与系统自行总结经验的攻击权限区别开，正确。 |
| [19] | Srivastava、He，*MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval*；arXiv:2512.16962v1，2025-12-18。 | PDF pp1–2及§3支持通过 README 等读取材料诱导保存伪造成功经验，后续语义/词法检索与模仿产生跨会话持续漂移；5.1有支持。其原文不是必须由攻击者直接编辑最终数据库的模型。 |
| [20] | Zhang等，*MemMorph: Tool Hijacking in LLM Agents via Memory Poisoning*；arXiv:2605.26154v1，2026-05-24。官方 arXiv Comments 明确 Preprint. Under review。 | PDF pp1–3支持以技术事实、事件报告、操作政策伪装记忆记录，间接改变情境判断与工具选择。5.1有支持。攻击本身是记忆投毒；附录训练型检测器对比不应被误认为攻击需要训练目标模型。 |
| [21] | Wang、Lou、Zhou、Li，*OEP: Poisoning Self-Evolving LLM Agents via Locally Correct but Non-Transferable Experiences*；arXiv:2605.18930v1，2026-05-18。 | PDF pp1–3及§4支持局部正确、不可迁移经验加严重但合理的假设后果，诱导反思形成过度泛化规则；§4.3已有精心安排的案例序列，§6已有混合反思批次，附录OpenClaw设置每域注入10例。5.1最新版本已补批次覆盖，正确；“多条一起反思”本身不能成为S7增量。 |
| [22] | Zhao等，*MEMOREPAIR: Barrier-First Cascade Repair in Agentic Memory*；arXiv:2605.07242v1，2026-05-08。 | PDF pp1–4支持先撤回影响级联，再用仍有效支持与修复前驱构造后继，只发布验证且前驱闭合的结果。pp8–9限制及来源边删除实验明确完整 influence provenance 是保证条件。删除、更正、工具/API迁移均有覆盖。3.1、5.1、6.1、S10主要概括有支持；最新稿已说明本项目仅借鉴存储级部分。 |
| [23] | Louck，*Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees*；arXiv:2606.24322v1，2026-06-23；TMA-NM是文中构造名。 | PDF §II–III支持可信监控按到达通道绑定真正来源，不依正文自述；不可随改写或可信工具回显洗白；重要动作通过至少2个独立可信 principal 或新的动作绑定用户授权提升/许可。最终4.1已补主要保证 consequential action integrity、非所有回答的事实正确、跨Agent共享记忆 out of scope，现有描述受支持。 |
| [24] | Li等，*MemTX: Transactional Belief Commit for Stateful Agent Memory*；arXiv:2607.23929v2，2026-07-28。 | PDF §3支持暂存、验证提交、权限/有效性/来源与类型化级联修复；§3.4明确未记录来源不受修复覆盖，补偿是决策级审计义务而非环境重放。§4.3 temporal-scope报告旧写入被拒后在新事务重试，竞争记录已在新快照中导致退回权威裁决。3.1和S3分界有支持；不能把该具体例子改写为已经实证“撤销后任意新ID都绕过”。 |
| [25] | Chen等，*MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair*；arXiv:2607.27080v1，2026-07-29。 | PDF p1及方法部分明确 Write–Execute–Forget链，跟踪写入、后续行为与选择性修复。Figure 1临时付款规则丢失有效日期后成为长期规则。5.1的适用信息丢失、8.1生命周期概括有支持。临时规则示例不能外推为所有条件迁移机制都已实证。 |
| [26] | Shen、Toyoda、Leung，*Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems*；arXiv:2609.08258v1，2026-09-08。 | PDF §§3–5研究5系统、9情景、9模型，并区分撤销未记录、对应用不可见、读取不执行。附录C确实扩展写回、多角色共享库与工具动作。最新3.1、S3/S4分界均有支持；扩展结果主要在Graphiti流程中，不得外推所有系统。详见下文。 |
| [27] | Yao等，*Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents*；arXiv:2609.04875v1，2026-09-04。 | PDF pp2–5支持运行时来源图定位首次注入、恢复干净检查点/裁剪KV、清洗后重放后缀及shadow execution/dedup。p4 Theorem 1有确定性或固定随机性、反事实一致观察、无不可恢复已提交外部副作用等条件；p7限制排除模型参数和已提交副作用。3.1概括正确；选择性是复用干净前缀并重建受污染后缀，不是任意跳过污染后缀内的状态。PDF的2027版权样式不构成可独立确认的AAAI录用，稿件仅称2026预印本是稳妥的。 |
| [28] | Lee、Tiwari，*Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*；arXiv:2410.07283v1，2024-10-09。 | PDF pp1–2及实验支持恶意提示在协作消息中自复制、扩散到未直接接触初始外部材料的Agent。3.1、S4分界正确；该论文不能单独作为“接收方已修复后再次感染”实验已经完成的证据。 |
| [32] | Zhan等，*InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*；本地arXiv:2403.02691v3；官方ACL条目确认 Findings ACL 2024。 | PDF摘要和评测方法支持工具返回中的间接注入测试、用户目标与攻击者目标评分。2.1有支持；不提供植入后跨会话持久触发的替代证明。 |
| [33] | Debenedetti等，*AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*；正式NeurIPS 2024 Datasets and Benchmarks PDF。 | PDF pp1–3支持可扩展动态任务、工具环境、安全任务与攻击/防御评测，能追踪多步任务及后续调用。2.1有支持。“实际工具交互”应理解为可执行评测环境，不能据此称真实生产部署实验。 |
| [34] | Wang等，*MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers*（出版页面题名）；本地PDF题名多一个Attack，首页面明确AAAI-26及35811页。正式卷40(42)、35811–35819，由AAAI官方确认；2025年预印本arXiv:2508.14925。 | PDF p1摘要支持注册工具元数据内投毒，可不执行恶意工具；2.1有支持。初稿[34]“本地保存预印本”错误，已反馈并由父任务改为“本地正式PDF”。正式页面与PDF的轻微题名差异已说明，论文身份一致。 |
| [35] | Li等，*MCP-ITP: An Automated Framework for Implicit Tool Poisoning in MCP*；arXiv:2601.07395v1，2026-01-12。 | PDF p1、§3支持恶意工具本身不调用、其元数据诱导调用合法高权限工具，并以检测/评测反馈黑盒优化。2.1准确。不能将“不调用恶意工具也影响合法工具”重新命名为新机制。 |
| [36] | Ediga、Chattopadhyay，*Measuring and Exploiting Implicit Trust in LLM Tool-Calling Pipelines*；arXiv:2609.18217v1，2026-09-16。GhostSplice不是PDF题名/正文中的方法名；作者官方披露和仓库确认相关攻击名称。 | PDF摘要、§III–IV支持五种输入通道信任测量及多通道碎片拼接、sampling/TOCTOU等扩展。2.1相关研究概括有支持。将GhostSplice作为相关披露简称可以保留，宜附作者披露链接，避免误认成正式论文标题。 |
| [37] | Feng等，*BackdoorAgent: A Unified Framework for Backdoor Attacks on LLM-based Agents*；本地arXiv:2601.04566v2；官方ACL条目确认Findings ACL 2026。 | PDF摘要及§4、官方正式摘要支持planning/memory/tool-use三个阶段、触发器传播和统一任务评测。8.1有支持，但工作流内跨步骤保持不自动等于独立会话重置后的持久性，稿件已另设边界。 |
| [38] | *Securing the Tool Layer: A Threat Taxonomy and Runtime Defense Framework for Model Context Protocol Deployments*；本地正式ACL Industry 2026 PDF，pp865–871；SHIELD MCP为正文防御构造名。 | PDF摘要、§3支持描述、参数、响应三阶段运行时代理检查与跨调用依赖相关检查。2.1有支持。“ShieldMCP”只是在正文中正常化大小写/空格的简称，非另一篇论文。 |
| [41] | Li等，*A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory*；arXiv:2609.30813v1，2026-09-25；Correlated Promotion Benchmark（CPB）为基准名。 | PDF摘要及方法支持重复/转述被当作独立支持、CPB-Static与Live、不同接纳政策的错拒与假信念采纳权衡。4.1有支持。场景定义的来源真值与部署时实际可见元数据不能混同；稿件对可信来源的独立说明正确。 |
| [45] | Mansoor、Phadke、Rana，*Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures*；arXiv:2608.02645v1，页脚2026-07-31，文面日期August 5 2026；均为2026预印本。 | PDF摘要及方法明确time-out after dispatch、延迟可见、部分状态更新，postcondition verification、verify-before-retry、idempotency keys。7.1有支持；研究在受控模拟环境完成，不是已证明经验总结安全。 |
| [48] | Hubinger等，*Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training*；arXiv:2401.05566v3，2024-01-17。 | PDF摘要、方法支持经训练生成条件性不安全行为，部分在SFT/RL/对抗安全训练后保留。8.1训练背景定位正确；与运行时存储修复不是相同作用层。 |
| [54] | Lyu、Ren、Lai、Liu，*From Version Conflicts to Decision Conflicts: Selective Revalidation for Long-Running AI Agents*；arXiv:2609.08015v1，2026-09-07；ATR为原文方法名。 | PDF pp1–3支持记录待执行动作的明确、可执行前提，状态变更后只重检受影响前提，再由目标侧事务/CAS绑定提交。p5限制是开发者编写前提与真值的确定性受控实验，未验证自然语言前提自动抽取。4.1“依据变化后选择性复核”合理，但不应暗示其原生解决接纳后来源身份和独立性图更新。 |
| [56] | Pulipaka等，*Hidden in Memory: Sleeper Memory Poisoning in LLM Agents*；arXiv:2605.15338v2，2026-05-18；PDF明确Preprint. Under Review。 | PDF摘要、威胁模型与评测支持低信任文档/网页/代码库诱导保存伪造用户记忆，未来多次会话检索并引发攻击者目标，跟踪write–retrieve–use。8.1有支持；分阶段及条件成功率应区分，稿件共同实验边界已说明。 |

## 重点事实核验与需保留的边界

### MemTX的跨事务重试

§4.3（PDF p6）已有明确例子：旧写入被判过时并拒绝；Agent在新事务重试；新快照已有竞争写入，因而原“晚到写入”条件不再成立，裁决退回来源权威。论文还报告部分模型未声明父来源的问题。当前稿件说“它也讨论跨事务重试等边界”有支持；S3的新研究机制依旧是待测假设，原文不直接证明“任何被撤销内容换ID即可重新接纳”。§3.4（p4）也明确未记录来源不能修复、补偿不等于环境重放。应保留现稿的二者区分。

### MemoRepair的完整来源图条件与参数分支

§2.1（p2）区分 influence edges 与 semantic retrieval edges，只有前者决定修复范围。§3.4和§5显示缺1%影响边会产生17.7% Leak，完整影响来源是保证条件，而非一般检索相似边。该稿已准确提示来源缺失边界。论文还包含 neural-skill param 模式、LoRA参数持留和参数遗忘操作对照（pp3、5、7–8）；父任务在3.1补入“本项目仅借鉴存储级撤回、重建与验证”后，推理时边界已清楚。

### Forgetting的重放对象

Theorem 1（p4）与算法（p5）操作的是可重建运行时：首次注入前的干净前缀可复用；注入后受污染KV/模型派生状态需按序重建。反事实固定内容可经prefill重放，模型派生内容重新解码。工具使用shadow execution与dedup；已提交外部动作不能因重放而自动撤销。当前稿件3.1没有把它误述为“删记忆后重试生成所有记忆”，有支持。PDF p7还限制反事实观察一致性、人类输入可能改变、分布实验非显著性不等于理论等价。不要从这里推出所有商业API都能直接实现精确运行时撤销。

### Revoked的范围与附录C

主研究比较Graphiti、Zep、mem0、langmem、cognee的指定配置；其中Graphiti/Zep共享引擎，mem0的默认expired过滤与关闭过滤的配置表现不同（附录B.3）。因此稿件限定“所评测系统和设置”正确，不能复述成“所有默认系统均必然不执行任何撤销”。

附录C（pp17–20）的3类扩展均主要在Graphiti指定流程上完成：C.1把受污染决策journal写回当前新记录，原记录过滤可能不足以消除新派生影响；natural ingestion和direct write两种模式分别报告，前者会自行丢弃/取代很多journal，不能只用direct模式效果描述自然流程。C.2是三个角色各自从同一个共享库检索，研究原失效记录与写回journal传播；它不是“接收方已完成本地修复后，从独立伙伴存储收到重新表达消息”的相同实验。C.3还有原失效记录不再返回时，第二Agent仍通过journal复发的情况。最新稿3.1及S3、S4补充正好说明这些近邻与区别，有原文支持。

### OEP的已有组合覆盖

局部正确但不可迁移经验、严重假设后果、反思自生高优先级规则均是已有核心机制。§4.3已有案例序列；§6比较正常/攻击案例混合比例；附录OpenClaw实验每个域有10个案例。最新5.1已补序列和批次反思覆盖。S7只能把明确的条件交互、组合特异性及其区别作为待检验对象，“两条以上”或“多例一起反思”不是单独增量。本记录没有扩写研究方案。

### GhostSplice与ShieldMCP名称

GhostSplice名称无法从[36]本地PDF或arXiv摘要页面直接确认，但作者所属ASSET官方披露明确以该名指代跨通道碎片拼接攻击，其官方代码仓库也使用该名。这里存在“相关攻击披露简称”和“正式论文题名”两种身份。建议参考文献继续用正式论文题名，并附相关作者披露作为别名依据：[ASSET作者披露](https://asset-group.github.io/disclosures/ghostsplice/)、[官方PoC仓库](https://github.com/asset-group/ghostsplice)。ShieldMCP/SHIELD MCP明确在[38]正文使用，无需另造同名论文条目。

### 训练型文献与推理时范围

[8]、[48]的后门植入发生于训练阶段，现稿正确仅作历史背景。[13]的语言强化不更新权重；[16]无需训练目标模型。[22]同时包含存储级和参数级修复，现稿新增限定正确。[20]附录A.3有检测器训练对比（AdamW、10 epochs），不表示其记忆投毒攻击需要训练目标大模型；已有论文含训练型基线也不意味着本项目必须训练。拟方案和实验均应继续保留“尚待验证”状态。

## 已反馈修改与剩余精度建议

| 状态 | 主稿位置 | 原问题 | 处理或建议 |
|---|---|---|---|
| 已由父任务修订 | [34]参考文献备注 | 把本地AAAI正式PDF称为预印本 | 改成“本地正式PDF与出版页面题名略有差异”；官方题名继续采用页面题名。 |
| 已由父任务修订 | 3.1 MemoRepair、推理时范围 | 原概括未提示该论文包含参数修复分支 | 已注明仅借鉴存储级撤回、重建与验证。 |
| 已由父任务修订 | 5.1 OEP及S7近邻 | 需要更清楚承认已有序列/批次反思 | 已补案例序列与批次，不把“多条一起反思”单独当新机制。 |
| 已由父任务修订 | [36]及2.1 | GhostSplice不是论文题名/正文方法名 | 已写成相关公开攻击披露简称，并附作者披露/仓库链接。 |
| 已由父任务修订 | 4.1 TMA-NM、S4近邻 | 来源权威保证与认知事实资格、跨Agent协议容易混淆 | 已说明重要动作来源权威门控、动作绑定新用户授权替代路径、非所有回答事实正确、跨Agent共享记忆明确不在原保证范围；与原文一致。 |
| 可选精度建议 | 4.1 Selective Revalidation | “证据版本/决策依据变化”较泛 | 若再压实表述，可写成“待执行动作所依赖的可执行前提变化后，选择性复核”；不宣称其已实现来源身份/独立性图更新。 |

## 有针对性的官方来源核验

下列链接仅用于解决本地原文不能确认的出版或别名问题，并非新增文献搜索。

- SleeperNets正式NeurIPS 2024身份：[出版方页面](https://proceedings.neurips.cc/paper_files/paper/2024/hash/cb03b5108f1c3a38c990ef0b45bc8b31-Abstract-Conference.html)。
- InjecAgent正式Findings ACL 2024身份：[ACL Anthology](https://aclanthology.org/2024.findings-acl.624/)。
- BackdoorAgent正式Findings ACL 2026身份：[ACL Anthology](https://aclanthology.org/2026.findings-acl.791/)。
- MCPTox正式题名、卷期及日期：[AAAI出版页面](https://ojs.aaai.org/index.php/AAAI/article/view/40895)；2025预印本身份：[arXiv:2508.14925](https://arxiv.org/abs/2508.14925)。
- MemMorph under review备注：[arXiv:2605.26154](https://arxiv.org/abs/2605.26154)。
- [36]正式论文身份：[arXiv:2609.18217](https://arxiv.org/abs/2609.18217)；相关GhostSplice名称见上列作者披露与仓库。

本核验未进行撤稿数据库筛查，未独立验证论文作者实验代码或复现其数值，也未证明26篇在2026-10-07时均为各题最新版本。结论限于所读本地版本、主稿具体已有研究描述和列明的官方身份核验。
