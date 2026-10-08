# 硕士学位论文开题报告（文献查重修订版）

论文总题目：Agent 后门攻击研究

拟定研究重点：工具生命周期中的后门残留与多 Agent 记忆的事后再污染

版本日期：2026 年 9 月 27 日

说明：本报告为对上一版《Agent 后门攻击_硕士开题报告》的文献查重和选题修订。文中的“未见直接覆盖”仅表示截至本报告日期，在列明的公开论文及关键词范围内没有找到研究问题、威胁模型和评测终点均相同的工作；它不是对全球文献的绝对新颖性证明。所有课题均为推理时研究，不训练或微调大模型。

# 摘要

本报告重新核对 2024—2026 年 Agent 后门、记忆投毒、MCP 工具安全和多 Agent 安全研究后发现，旧报告中六个候选方向均与近期工作存在程度不同的重叠。尤其是组合记忆与情境触发已由 MemPoison 明确覆盖；跨 MCP 通道拆分注入已由 GhostSplice 研究；同源记忆形成虚假多数已由 CAMA 作为核心问题提出；多 Agent 记忆传播阻断已有 MAPLE-Guard；选择性修复、调用前门控和来源追踪也已有 MemSecBench、MemTX、ShieldMCP、MemLineage 等工作。基于此，本报告不再将上述现象本身作为创新点，而把研究问题收窄为两个可验证的时间边界：第一，恶意 MCP 工具被移除或恢复为正常版本后，其诱导的经验记忆是否仍会迁移到其他合法工具并触发错误动作；第二，污染源被发现并清理后，未同步清理的私有记忆、共享记忆和待处理消息是否会使系统再次污染，尤其在来源谱系不完整时如何定点阻断。两篇子课题分别以工具生命周期和多 Agent 事后修复为主，实验相互独立，可合并为硕士论文主体。

# 一、研究背景与问题界定

Agent 后门攻击不要求改变模型参数。攻击者可在推理时通过文档、查询、工具描述、工具响应或 Agent 消息影响系统状态，使 Agent 在特定后续条件下执行偏离用户任务的行为。长期记忆使一次攻击在原始输入消失后仍可能被使用；工具和多 Agent 协作则增加了受影响状态的种类与传播路径。为避免把普通提示注入误称为后门，本报告要求攻击至少满足三个条件：攻击源在后续测试阶段不再直接出现；攻击效果依赖先前被写入或派生的状态；使用实际环境状态或工具动作日志判定结果。

本文把“已有人做过”分为三档。直接覆盖指已有论文将相同机制作为主要问题，且有明确实验；实质相邻指机制或防御边界相近，但威胁模型、时间阶段或最终指标不同；未见直接覆盖指所检索论文未同时包含本文拟定的具体攻击能力、时间过程和动作终点。近年预印本更新很快，开题后的每次投稿前仍需再次检索。

# 二、检索范围与判断方法

检索日期为 2026 年 9 月 27 日，优先查看论文原文、会议页面、项目官方文档。关键词覆盖 agent memory poisoning、context-triggered memory corruption、memory repair、MCP tool metadata、cross-channel fragmentation、tool retirement、multi-agent shared-memory poisoning、correlated evidence、post-repair reinfection 等组合。重点比对旧报告 C1—C6 的威胁模型、攻击入口、时间跨度、目标动作、所需权限、基准和防御机制。表中“未见直接覆盖”应作为拟研究问题，不能在论文引言中直接写成“首次提出”。

# 三、旧报告六个方向的查重结论

| 旧方向 | 已有直接或高度相邻研究 | 修订结论 |
| --- | --- | --- |
| C1 提示与记忆条件组合的延迟后门 | AgentPoison、Zombie Agents、Sleeper Memory Poisoning 已覆盖持久或休眠后门；MemPoison 明确包含组合多记录污染和情境触发休眠污染；ACL 2026 的 Conjunctive Prompt Attacks 研究组合触发。 | 原表述不再推荐独立投稿；仅可作为新方向的对照攻击。 |
| C2 派生记忆的选择性修复 | MemSecBench 已用 Write—Execute—Forget 评测选择性修复；MemLineage、TMA-NM、MemTX 和 Forgetting Without Restarting 已研究谱系、级联修复或选择性重放。 | “发现后修复派生记忆”过宽；只有在不完整谱系、跨 Agent 异步再污染等更窄条件下才可能有独立空间。 |
| C3 MCP 描述变化与返回值协同触发 | MCPTox、MCP Security Bench、ETDI 已覆盖工具投毒、混合攻击和定义变化；GhostSplice 已直接评测工具描述、结果及 sampling 等跨通道拆分注入。 | 旧版“描述＋返回值组合”为高重叠；不得作为主创新。 |
| C4 面向 MCP 后门的调用前证据校验 | ShieldMCP 已实现运行时校验；MemLineage、TMA-NM、PPMF 与 MemTX 已研究来源、权限、动作门控。 | 泛化的调用前校验不是空白；可作为基线或工程组件。 |
| C5 多 Agent 共享记忆中的虚假独立背书 | Prompt Infection、Mandela Effect、PlanFlip 研究传播和集体错误；CAMA 已把同源记忆被重复计数的“虚假多数”设为核心问题并提出独立来源推断。 | 旧版“同源转述变成多数”与 CAMA 直接重叠，不建议按原题开展。 |
| C6 多 Agent 证据去重与定点隔离 | CAMA 已做相关记忆去重与独立证据恢复；MAPLE-Guard 已在写入、检索、共享提升和跨 Agent 重用处设置防护；MemTX 包含级联修复。 | 泛化去重与隔离不宜独立成篇；需转向事后、跨副本、谱系缺失条件。 |

## 3.1 需要明确承认的近期论文

MemPoison 于 2026 年 7 月提出 L1 直接污染、L2 组合多记录污染、L3 情境触发休眠污染三个层级。因此旧版 C1 不能把“组合条件触发”本身称为新机制。GhostSplice 于 2026 年 9 月研究 MCP 工具描述、工具结果和 sampling 通道中的拆分注入，因此旧版 C3 的“描述与返回值分别放一段攻击信息”已被覆盖。CAMA 于 2026 年 8 月提出 Memory Correlation Bias，并处理同源记忆形成虚假多数；MAPLE-Guard 于同月研究私有与共享记忆之间的污染传播。因此旧版 C5、C6 的核心表述也不再新颖。

MemSecBench 于 2026 年 7 月追踪记忆写入、行为后果和选择性修复；MemTX 同月提出包含撤销后的级联修复的事务式记忆协议；Forgetting Without Restarting 于 2026 年 9 月研究状态级选择性重放。PPMF、TMA-NM、MemLineage 等研究还覆盖来源保留与敏感动作门控。以上工作共同压缩了旧版 C2、C4 的空间。上述 2026 年论文中多篇为 arXiv 预印本，需与已发表的 NeurIPS、AAAI、ACL 工作区分，不应一概称为顶会论文。

# 四、仍值得检验的细分研究空间

在上述文献中，能够作为硕士小论文候选的不是新的“攻击面名称”，而是此前方法的时间边界和假设条件。以下两个方向均处在已有研究的交叉处，但本次检索未找到完全相同的论文。它们具有中等新颖性风险，必须用对照实验验证其独立价值。

| 新编号 | 拟定细分问题 | 与最接近工作的区别 | 新颖性风险 |
| --- | --- | --- | --- |
| N1 | 恶意 MCP 工具退役或恢复正常后，已写入的经验记忆是否迁移到其他合法工具并诱导目标动作？ | GhostSplice 关注暴露时跨通道组合；MemMorph 关注记忆改变工具选择；eTAMP 关注环境观察后的跨站持久性。N1 的关键条件是恶意工具在测试时已不存在，结果发生在另一合法工具上。 | 中等偏高；若已有论文实验含工具撤销与替代工具迁移，必须再次收窄。 |
| N2 | 初始污染源清理后，私有记忆、共享记忆或待处理消息是否让系统再污染；谱系缺失时怎样最小范围阻断？ | MemSecBench 和 MemTX 涉及修复；MAPLE-Guard 重在传播前门控；Forgetting Without Restarting 面向单 Agent 状态。N2 以事后发现、多个副本和异步重放为固定条件。 | 中等偏高；应避免宣称“首次修复多 Agent 记忆”，只研究再污染边界。 |

N1 可继续细分为三个可测子问题：工具描述恢复正常但工具仍在时，经验记忆是否保留旧动作模式；恶意工具彻底移除后，经验能否迁移到替代合法工具；如果先后发生工具更新与记忆摘要，哪一步决定后门残留。N2 可细分为三个可测子问题：只清理共享记忆而留下私有副本是否造成再污染；清理后到达的旧消息是否重新写入；在随机缺失部分来源边时，定点隔离和全量重置的安全与效用差异。

# 五、子课题一：工具退役后的记忆迁移型后门

暂定中文题目：恶意 MCP 工具退役后 Agent 经验记忆的后门残留与跨工具迁移

暂定英文题目：Residual Backdoors after MCP Tool Retirement: Cross-Tool Transfer through Agent Experience Memory

## 5.1 研究背景

工具描述及返回值可能进入 Agent 的经验记忆。工具服务被删除、恢复为正常版本或失去授权后，工具入口虽已清理，记忆中保存的“成功做法”可能仍影响下一次任务。若下一次任务使用的是另一个合法工具，单靠检查原恶意工具是否存在不能判定后门是否消失。

## 5.2 国内外研究现状

MCPTox 和 MCP Security Bench 已展示工具元数据及响应攻击；GhostSplice 研究跨 MCP 通道碎片化注入；MemoryGraft、MemMorph 和 eTAMP 分别研究经验记忆模仿、记忆驱动工具选择和环境输入造成的跨会话污染。CodeGuard 等实测工作提及记忆可能保留先前 MCP 安全信息。但本次检索未见以“恶意工具退役或描述回滚后的替代工具动作”为主终点的系统性实验。该判断仅限所列文献，不能写成绝对首创。

## 5.3 现有研究不足与明确空白

已有 MCP 攻击多数在恶意工具仍可见或刚刚提供响应时判定成功；已有记忆投毒研究通常不把工具从环境中真实移除。N1 将暴露阶段和测试阶段严格分开：测试时删除攻击者工具与原始攻击文本，保留通过正常流程写成的经验记忆，再观察另一合法工具是否被错误调用。若清理工具后攻击仍成立，就说明工具撤销与经验记忆撤销之间存在可测的安全差距。

## 5.4 研究目标

构建单工具控制、一次暴露、工具退役后的后门实验；量化后门保留率、跨工具迁移率、误触发率及正常任务损失；识别记忆写入、摘要与工具退役顺序对结果的影响。

## 5.5 研究内容与威胁模型

攻击者只控制一个低可信 MCP 服务中的一项工具描述和返回文本，最多影响一次合法暴露任务；不能更改系统指令、其他服务、记忆数据库或后续用户任务。实验测试时，恶意服务已经删除或恢复为正常版本。攻击目标为让 Agent 在后续合法任务中错误选择另一项仍获准使用的模拟工具，或写入错误的模拟工单状态。该行为必须由实际工具调用或环境状态证明，不能仅靠最终回答推断。

研究分为暴露阶段、经验写入阶段、工具退役阶段和延迟测试阶段。暴露阶段只允许攻击者控制一个 MCP 工具；经验写入由 Agent 的正常机制完成；工具退役阶段应验证攻击者工具确实不可调用；测试阶段只提供正常用户任务，并在无原始恶意文本的上下文中进行。

## 5.6 关键科学问题

当攻击入口已经撤销时，哪些记忆表示仍会将低可信工具信息解释为可迁移的工作经验？这种跨工具迁移是否依赖“成功经验”措辞、摘要压缩或合法工具之间的功能相似度？

## 5.7 技术路线

使用 Eino 构建一个带持久经验记忆的 Agent，连接本地模拟 MCP 服务。先在无攻击条件下建立合法任务和工具行为基线；再运行一次受攻击暴露任务，让 Agent 自行写入经验；随后对恶意工具执行删除、描述回滚或服务禁用；最后在新会话中运行匹配、近似匹配和无关任务。每条轨迹保存工具注册版本、记忆写入内容、检索命中、被调用工具、参数及最终环境状态。通过移除记忆、替换为干净记忆和保留恶意工具等反事实设置，估计工具退役后的记忆独立贡献。

## 5.8 实验可行性与评测设计

本方向不需要微调。Eino 与本地 MCP 环境可以实现全流程，实验只涉及虚构数据与模拟动作。计划建立 30—50 个基础任务模板，每个模板包含触发、近似触发及正常对照样本。基线包括静态 MCP 描述投毒、单次工具返回值注入、MemoryGraft 式经验污染和 MemMorph 式记忆改变工具选择。指标为工具退役后端到端攻击成功率、跨工具迁移率、正常任务成功率、误触发率、记忆检索率及残留会话数。消融变量为退役方式、工具相似度、摘要次数、记忆容量、间隔会话数和经验写入条件。数据按任务模板划分设计集与测试集，重复运行并给出置信区间。

## 5.9 拟创新点

第一，明确提出并实测“攻击工具已撤销，后门经经验记忆转移到替代合法工具”的时间边界。第二，建立工具版本、记忆写入、工具撤销与后续动作的可回放因果链。第三，将工具撤销后的残留风险与正常任务效用同时量化。以上均为拟贡献，只有在实验表明跨工具残留显著且不由原攻击文本再次暴露解释时，才可作为论文创新点。

## 5.10 预期成果与风险

预期形成可复现的 MCP 生命周期实验集、带轨迹的评测代码和第一篇小论文初稿，预计 6—7 人周。主要风险为跨工具迁移率偏低，或 MemMorph、eTAMP 的现有配置已覆盖相同现象。开题后的前 3 周应做最小实验：至少比较保留记忆、清空记忆、保留恶意工具三种设置。若工具删除后效果完全消失，应及时停止将本题作为攻击论文主线，不用少量成功个例支撑结论。

## 5.11 研究进度安排

2026 年 9 月下旬完成威胁模型与文献核对；10 月上旬完成 Eino 与本地 MCP 测试床；10 月下旬完成最小可行性实验及继续/停止判断；11 月完成正式数据、基线与消融；12 月上旬完成第一篇论文初稿。

【开题复用片段】现有研究已证明 MCP 工具描述与返回值可被投毒，也证明 Agent 能把受污染内容写入长期经验记忆。然而，当恶意工具已经删除、回滚或禁用时，先前生成的经验是否继续影响后续合法工具调用，仍需在严格分离攻击暴露与后续测试的条件下验证。本课题拟研究工具退役后的记忆型后门残留与跨工具迁移，为工具撤销后的安全检查提供实证依据。

# 六、子课题二：不完整谱系下多 Agent 修复后的再污染

暂定中文题目：不完整来源记录下多 Agent 共享记忆的事后再污染与定点阻断

暂定英文题目：Post-Repair Reinfection in Multi-Agent Shared Memory under Incomplete Provenance

## 6.1 研究背景

多 Agent 系统可能同时保有私有记忆、共享记忆和未处理完的消息。发现投毒后，清理某个数据库条目并不一定清理其他 Agent 已经读入的副本，或排队等待写入的旧消息。系统重新开放任务时，这些残留状态可能再次污染共享记忆。

## 6.2 国内外研究现状

Prompt Infection、Mandela Effect 和 PlanFlip 展示 Agent 间传播或级联影响；MAPLE-Guard 已在记忆写入、检索、共享提升与跨 Agent 重用处设置门控；CAMA 已处理相关记忆的虚假多数；MemSecBench 评测记忆的选择性修复；MemTX 涉及撤销后的级联修复；Forgetting Without Restarting 研究单 Agent 状态的选择性重放。故本课题不能声称“首次研究多 Agent 记忆传播”或“首次提出级联修复”。本次检索未见将“污染发现较晚、多个 Agent 已持有副本、消息仍在队列、来源边部分缺失”组合为主要威胁模型，并用修复后的再次污染率作为核心终点的工作。

## 6.3 现有研究不足与明确空白

现有防护通常在写入或跨 Agent 传播前起作用，或依赖较完整的来源信息。真实事故中，污染可能已扩散，来源链也可能被摘要、日志缺失或异步消息削弱。本课题固定为“事后发现”的场景，衡量局部清理后发生再污染的概率和时间，并研究在日志不完整时的低成本隔离边界。

## 6.4 研究目标

构建可回放的多 Agent 事后修复基准，测量不同残留载体导致的再污染；提出轻量的版本代际标记与待处理写入隔离机制，在安全收益与正常协作效用之间取得可衡量的平衡。

## 6.5 研究内容与威胁模型

攻击者只在初始阶段控制一个 Agent 可见的文档、工具响应或普通查询，不能直接修改其他 Agent 的私有记忆、共享数据库、消息队列或防御代码。修复开始后，攻击者不再发送新内容；若系统重新污染，来源只能是先前残留状态。防御方能访问共享记忆与消息总线，但只获得部分私有记忆日志；通过“完整来源边、随机缺失来源边、摘要丢失来源边”三个条件模拟现实记录差异。

系统含 3—5 个 Agent，每个 Agent 有私有记忆，另设一份共享记忆与异步消息队列。初始投毒内容经正常协作扩散后，由审计者在某时刻发现并清理已知源条目，然后恢复系统运行。研究分别考察私有记忆副本、共享摘要、队列中的旧消息以及它们的组合。

## 6.6 关键科学问题

在来源链不完整且存在异步消息时，哪些残留状态会导致修复后再污染？能否用有限的版本代际信息阻止旧污染重新提升为共享可信记忆，而不清空全部 Agent 状态？

## 6.7 技术路线

建立任务与事件时间线：初始写入、跨 Agent 传播、共享记忆提升、污染发现、局部修复、消息继续送达、再次写入与最终动作。给每次修复赋予新的代际号，后续共享写入必须声明其依赖的源代际；对来源不明但发生在修复前的待处理写入先隔离，再通过重放或独立证据核验决定恢复。方法仅修改记忆与消息中间件，不改变模型参数。与无修复、仅删除源条目、全量清空、来源链级联修复和 MAPLE-Guard 式生命周期门控比较。

## 6.8 实验可行性与评测设计

使用 Eino 建立本地 3—5 Agent 编排与 SQLite 消息、记忆日志；不需要训练，不强制接入 MCP。自建 30—40 个具有来源真值的协作任务，包含正常多源信息与单源污染对照。指标包括修复后再污染率、再污染时间、受影响 Agent 数、端到端目标动作 ASR、正常协作任务成功率、误隔离率和修复成本。消融修复发现时刻、来源边缺失比例、消息延迟、拓扑、共享提升频率与隔离范围。结果必须区分“原污染未清除”与“已清除后重新写入”；只有后者属于本课题定义的再污染。

## 6.9 拟创新点

第一，将事后、异步、来源缺失条件下的“再污染”从一般传播与一般修复中分离出来，建立明确的事件级判定。第二，利用修复代际约束旧消息和旧私有记忆重新写入共享记忆。第三，对定点隔离、全量清空与已有生命周期门控方法进行安全与效用联合比较。上述创新必须以 MAPLE-Guard、MemTX 和 MemSecBench 为强基线。

## 6.10 预期成果与风险

预期形成多 Agent 再污染测试床、来源缺失条件的数据集、隔离原型和第二篇小论文初稿，预计 7—8 人周。主要风险是实验复杂、再污染与未清理残留难区分，以及 MemTX 的级联修复已能解决大部分设置。因此必须将事件日志和系统状态固定为可复现真值；如果强基线在同等可见信息下已经完全阻断再污染，则应如实收缩结论或转向其无法获取完整谱系时的效用代价分析。

## 6.11 研究进度安排

2026 年 10 月构建消息与记忆事件日志；11 月完成初始污染、清理与再污染重放；12 月完成强基线、日志缺失消融及防御实现；2027 年 1 月完成第二篇论文初稿和毕业论文主体材料。

【开题复用片段】现有多 Agent 安全研究已覆盖恶意信息传播、共享记忆门控和部分级联修复方法。但在污染被较晚发现时，Agent 私有记忆、共享摘要和异步消息可能同时保存旧信息，局部清理后仍可能重新写入共享记忆。本课题拟研究来源记录不完整条件下的事后再污染，建立可区分“未清理残留”与“修复后重新出现”的评测方法，并探索维持正常协作能力的定点阻断策略。

# 七、两篇小论文组合与硕士论文技术路线

推荐组合为 N1 攻击论文与 N2 防御论文。两篇的逻辑联系是都研究攻击入口消失后的残留状态；两篇的独立性在于 N1 研究单 Agent 的工具退役与跨工具迁移，N2 研究多 Agent 的事后修复和异步再污染。第二篇除使用 N1 的工具源样本外，还必须使用普通文档或查询源样本，避免成为第一篇的附加实验。

总体技术路线为：文献查重与威胁模型固定—本地 Eino/MCP 与多 Agent 测试床—N1 工具退役后的后门残留实验—N2 事后修复的再污染实验—跨课题指标统一与硕士论文写作。两篇均以实际动作或共享记忆状态为终点，保存完整轨迹，并分别报告攻击成功率、正常任务成功率、误触发、误隔离和实验方差。

预期形成两篇可独立投稿的小论文初稿、一套本地模拟工具与事件日志、两组可复现数据，以及毕业论文的背景、攻击、修复和综合分析章节。研二上完成全部实验与初稿的前提是前期设置明确的继续/停止关口：10 月下旬先判断 N1 是否存在稳定的工具退役后残留；11 月中旬判断 N2 的再污染是否能被事件日志准确区分。若关口不成立，应保留真实负结果并更换课题，不以调整样本或只报告成功案例维持原结论。

| 时间 | 主要工作与可检查交付物 |
| --- | --- |
| 2026 年 9 月下旬 | 查重矩阵、两篇威胁模型、任务与日志格式 |
| 2026 年 10 月 | N1 测试床、先导实验、正式攻击样本与基线 |
| 2026 年 11 月 | N1 消融和第一篇初稿；N2 事件重放原型 |
| 2026 年 12 月 | N2 再污染实验、强基线、缺失日志消融 |
| 2027 年 1 月 | N2 初稿、两篇修订、硕士论文主体草稿 |

# 八、论文写作与新颖性审查要求

第一篇引言应先承认 MCPTox、GhostSplice、MemMorph、MemoryGraft 和 eTAMP 已分别研究工具投毒、跨通道注入与记忆持久性，然后提出严格的新时间边界：测试时恶意工具已经退役，目标动作由另一合法工具执行。第二篇引言应先承认 MAPLE-Guard、CAMA、MemSecBench、MemTX 和 Forgetting Without Restarting 已分别研究传播门控、来源相关性、修复和选择性重放，再明确只讨论事后发现、多副本、异步消息及不完整谱系。

两篇论文均不得使用“首次研究 Agent 记忆后门”“首次提出 MCP 工具链攻击”“首次解决多 Agent 再污染”等未经证明的宽泛语句。可使用“据所列文献，本工作关注此前未被系统评测的特定设置”，并在投稿前重新执行文献检索。若新的直接先例出现，应进一步收窄变量、加强强基线或及时改题。

# 九、参考文献与公开来源

[1] Chen Z, et al. AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases. NeurIPS, 2024. https://papers.nips.cc/paper_files/paper/2024/file/eb113910e9c3f6242541c1652e30dfd6-Paper-Conference.pdf

[2] Dong S, et al. Memory Injection Attacks on LLM Agents via Query-Only Interaction. NeurIPS, 2025. https://papers.nips.cc/paper_files/paper/2025/file/42a97bbd9844d2bf68596730af80bcdf-Paper-Conference.pdf

[3] Srivastava S S, He H. MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval. arXiv, 2025. https://arxiv.org/abs/2512.16962

[4] Zhang X, et al. MemMorph: Tool Hijacking in LLM Agents via Memory Poisoning. arXiv, 2026. https://arxiv.org/abs/2605.26154

[5] Yang X, et al. Zombie Agents: Persistent Control of Self-Evolving LLM Agents via Self-Reinforcing Injections. arXiv, 2026. https://arxiv.org/abs/2602.15654

[6] Pulipaka S, et al. Hidden in Memory: Sleeper Memory Poisoning in LLM Agents. arXiv, 2026. https://arxiv.org/abs/2605.15338

[7] Gao J, et al. MemPoison: Uncovering Persistent Memory Threats and Structural Blind Spots in LLM Agents. arXiv, 2026. https://arxiv.org/abs/2607.14651

[8] Chen X, et al. MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair. arXiv, 2026. https://arxiv.org/abs/2607.27080

[9] Feng Y, et al. BackdoorAgent: A Unified Framework for Backdoor Attacks on LLM-based Agents. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.791/

[10] Wang Z, et al. MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers. AAAI, 2026. https://ojs.aaai.org/index.php/AAAI/article/view/40895

[11] Zhang D, et al. MCP Security Bench: Benchmarking Attacks Against Model Context Protocol in LLM Agents. arXiv, 2025. https://arxiv.org/abs/2510.15994

[12] Ediga M, Chattopadhyay S. Measuring and Exploiting Implicit Trust in LLM Tool-Calling Pipelines. arXiv, 2026. https://arxiv.org/abs/2609.18217

[13] Bhatt M, et al. ETDI: Mitigating Tool Squatting and Rug Pull Attacks in Model Context Protocol. arXiv, 2025. https://arxiv.org/abs/2506.01333

[14] Zou W, et al. Poison Once, Exploit Forever: Environment-Injected Memory Poisoning Attacks on Web Agents. arXiv, 2026. https://arxiv.org/abs/2604.02623

[15] Lee D, Tiwari M. Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems. arXiv, 2024. https://arxiv.org/abs/2410.07283

[16] Wang Y. PlanFlip: Attacking Multi-Agent LLM Systems via Planning-Phase Prompt Injection. arXiv, 2026. https://arxiv.org/abs/2607.16199

[17] Xu N, et al. When Agents “Misremember” Collectively: Exploring the Mandela Effect in LLM-based Multi-Agent Systems. arXiv, 2026. https://arxiv.org/abs/2602.00428

[18] Lin C, et al. Beyond Memory Majority: Latent-Source Reasoning for Multi-Agent Memory Arbitration. arXiv, 2026. https://arxiv.org/abs/2608.19701

[19] Xiong W, et al. MAPLE-Guard: Memory-Aware Link Enforcement Against Memory-Link Poisoning in Multi-Agent Systems. arXiv, 2026. https://arxiv.org/abs/2608.00426

[20] Li X, et al. MemTX: Transactional Belief Commit for Stateful Agent Memory. arXiv, 2026. https://arxiv.org/abs/2607.23929

[21] Yao C, et al. Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents. arXiv, 2026. https://arxiv.org/abs/2609.04875

[22] Ouyang C, Hou R. MemLineage: Lineage-Guided Enforcement for LLM Agent Memory. arXiv, 2026. https://arxiv.org/abs/2605.14421

[23] Louck Y. Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees. arXiv, 2026. https://arxiv.org/abs/2606.24322

[24] Xu J, et al. Memory Provenance Laundering in LLM Agents: A Non-Amplification Firewall for Persistent Memory. arXiv, 2026. https://arxiv.org/abs/2607.29167

[25] ShieldMCP: Securing the Tool Layer: A Threat Taxonomy and Runtime Defense Framework for Model Context Protocol Deployments. ACL Industry Track, 2026. https://aclanthology.org/2026.acl-industry.58/

[26] Shen Y T, et al. Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems. arXiv, 2026. https://arxiv.org/abs/2609.08258

[27] Cerruti T, et al. Agent Memory Is a Surface for Endogenous Authorization Laundering. arXiv, 2026. https://arxiv.org/abs/2609.01836

[28] Conjunctive Prompt Attacks in Multi-Agent LLM Systems. ACL, 2026. https://aclanthology.org/2026.acl-long.1577/

[29] CloudWeGo. Eino 文档与 MCP 工具接入。https://www.cloudwego.io/docs/eino/
