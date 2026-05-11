# 家装助手：施工问题检测 Skill

`home-renovation-assistant` 是一个面向家装场景的助手仓库，后续可以扩展预算审核、材料选型、施工进度、验收辅助、维权资料整理等能力。

当前仓库先提供一个可用于 Claude、Codex 及其他兼容 Skill 机制的 **施工问题检测 skill**。它根据用户提供的图片、视频、文字、图纸或施工记录，先识别当前施工阶段，再按该阶段的必检项、常见问题、偷工/遮掩模式和参考标准进行比对，辅助判断住宅装修或精装修施工中是否存在可见的质量、安全、工艺、工序和验收风险。

该 skill 的目标不是简单给出“合格/不合格”，而是帮助用户发现问题、判断严重程度、确认是否阻塞下一道工序，并给出补拍、复验和整改闭环建议。参考依据优先使用中国现行国家标准和强制性工程建设规范；当国标没有覆盖具体工艺细节时，可将大型装企或房企公开施工标准作为补充参考，并明确标注其非强制性属性。

## 当前 Skill

- Skill 名称：`renovation-inspection`
- 中文定位：施工问题检测
- 路径：`.codex/skills/renovation-inspection/`
- 当前状态：可用于图片、视频、文字、图纸和施工记录的阶段化问题检测

## 能力范围

- 支持图片、视频、文字及混合输入。
- 支持把设计图纸、施工记录作为辅助证据，但不会把图纸照片误判为现场施工缺陷。
- 先识别施工阶段，再加载该阶段的检查项和参考资料。
- 覆盖水电粗装、防水、门窗安装与窗边收口、贴砖与地面、竣工验收等重点阶段。
- 识别可见的施工质量、工艺、安全、保护、材料安装、工序跳步和下一工序风险。
- 区分证据强度：`confirmed`、`suspected`、`not_verifiable`。
- 输出阶段门风险，判断是否不建议进入下一道工序。
- 识别常见偷工或遮掩模式，例如大缝隙用厚胶遮盖、未测试即封槽、未留节点照片即覆盖防水。
- 按 `critical`、`high`、`medium`、`low`、`info` 排序输出风险。
- 为每个问题提供观察证据、风险说明、参考依据、证据强度、置信度、整改建议和复验资料。
- 对证据不足、画面模糊、隐蔽工程不可见等情况给出明确的不确定性说明。
- 主动提示用户可以继续补充图片、视频、带尺照片、测试记录或施工记录。
- 支持使用优秀施工参考图片做视觉对比，但不会把参考图片当成强制验收依据。

## 目录结构

```text
.codex/skills/renovation-inspection/
├── SKILL.md
├── references/
│   ├── output-schema.json
│   ├── shortcut-patterns.yaml
│   ├── stage-inspection-matrix.yaml
│   ├── standards-sources.yaml
│   ├── stages/
│   │   ├── completion-acceptance.yaml
│   │   ├── plumbing-electrical-rough-in.yaml
│   │   ├── tiling-flooring.yaml
│   │   ├── waterproofing.yaml
│   │   └── window-door-installation.yaml
│   ├── reference-image-strategy.md
│   └── severity-and-confidence.md
└── tests/
    ├── validation-checklist.md
    └── fixtures/README.md
```

文件说明：

- `SKILL.md`：主 skill 指令，定义适用场景、输入处理、分析流程、输出风格和限制。
- `references/output-schema.json`：结构化输出字段约束。
- `references/stage-inspection-matrix.yaml`：施工阶段识别、阶段必检项、常见问题和下一工序门槛。
- `references/stages/`：重点施工阶段的专门检查包。
- `references/shortcut-patterns.yaml`：常见偷工、遮掩、跳步施工模式库。
- `references/standards-sources.yaml`：初始国标、强制性规范、行业标准和企业补充标准清单。
- `references/reference-image-strategy.md`：优秀施工图片检索和对比规则。
- `references/severity-and-confidence.md`：严重程度和置信度判断规则。
- `tests/`：人工或自动化验证用例说明。

## 在 Codex 中使用

将仓库中的 skill 目录放在 Codex 可识别的 skills 路径下：

```text
.codex/skills/renovation-inspection/
```

当前仓库已经采用这个结构，可以直接作为 Codex skill 仓库使用。

## 在 Claude 中使用

如果你的 Claude 环境使用 `.claude/skills` 作为 skill 目录，可以复制同一个 skill：

```bash
mkdir -p .claude/skills
cp -R .codex/skills/renovation-inspection .claude/skills/
```

复制后路径为：

```text
.claude/skills/renovation-inspection/
```

只要运行环境支持读取 `SKILL.md` 及其相对路径下的 `references/` 文件，这个 skill 就可以在 Claude、Codex 或其他 agent 框架中复用。

## 典型使用场景

- 用户上传卫生间防水施工照片，询问是否有漏刷、翻边高度不足或管根处理问题。
- 用户上传水电阶段视频，要求检查线管、水管、开槽、固定、交叉和封槽前风险。
- 用户上传窗边、门槛、地砖收口照片，要求判断是否存在大缝隙、填塞不密实或厚胶遮盖风险。
- 用户描述墙砖空鼓、地漏排水慢、墙面开裂、插座位置异常等问题，要求判断严重程度和下一步处理方式。
- 用户上传设计图纸，要求作为后续现场核对依据，而不是直接判断施工合格。
- 项目经理希望按严重程度生成整改清单，便于和施工方沟通。

## 输出原则

默认使用简体中文输出巡检结果；`critical`、`high`、`confirmed`、`not_verifiable` 等结构化枚举值可以保留英文，并在需要时用中文解释。除非用户明确要求英文或其他语言，否则面向用户的判断、风险说明、整改建议和补充证据提示都应使用中文。

该 skill 的输出应尽量包含：

- 总体判断。
- 施工阶段识别。
- 已检查项和未验证必检项。
- 最紧急的下一步。
- 按严重程度排序的问题列表。
- 每个问题对应的图片或视频证据编号。
- 可能风险。
- 标准或参考依据。
- 证据强度和置信度。
- 是否阻塞下一道工序。
- 整改建议。
- 复验资料要求。
- 需要补充的图片、视频、测量或施工记录。

## 当前测试样例

- 窗框下口与地面/地砖收口缝隙偏大：可识别为门窗安装与窗边收口问题，命中“大缝隙用厚胶遮盖”模式，并提示不建议直接进入收口工序。
- 水电粗装照片：能列出水管打压、排水测试、线管通管、封槽前全路径照片等未验证必检项，避免凭单张照片直接判定合格。
- 防水和窗边节点照片：能区分可见防水层、疑似节点风险和闭水/淋水记录缺失。
- 图纸照片：能识别为设计/施工准备资料，不硬判施工缺陷，并建议补充现场照片做核对。

## 注意事项

- 标准清单是初始参考源，正式用于合同、验收、维权或法律场景前，必须核对官方或授权标准文本。
- 该 skill 只能判断用户提供证据中可见的内容，不能替代现场监理、结构工程师、电工、水工、燃气或消防等专业人员。
- 对隐蔽工程、结构安全、电气安全、防水闭水、管道打压等问题，如果缺少照片、视频或测试记录，应输出证据不足，而不是给出确定结论。
