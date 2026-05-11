# 装修施工巡检 Skill

这是一个面向 Claude、Codex 及其他兼容 Skill 机制的装修施工巡检 skill。它用于根据用户提供的图片、视频和文字描述，辅助判断住宅装修或精装修施工中是否存在可见的质量、安全、工艺、工序和标准相关问题。

该 skill 会按严重程度输出问题清单，优先参考中国现行国家标准和强制性工程建设规范；当国标没有覆盖到具体工艺细节时，可将大型装企或房企公开施工标准作为补充参考，并会明确标注其非强制性属性。

## 能力范围

- 支持图片、视频、文字及混合输入。
- 识别可见的施工质量、工艺、安全、保护、材料安装和工序问题。
- 按 `critical`、`high`、`medium`、`low`、`info` 排序输出风险。
- 为每个问题提供观察证据、风险说明、参考依据、置信度和整改建议。
- 对证据不足、画面模糊、隐蔽工程不可见等情况给出明确的不确定性说明。
- 支持使用优秀施工参考图片做视觉对比，但不会把参考图片当成强制验收依据。

## 目录结构

```text
.codex/skills/renovation-inspection/
├── SKILL.md
├── references/
│   ├── output-schema.json
│   ├── standards-sources.yaml
│   ├── reference-image-strategy.md
│   └── severity-and-confidence.md
└── tests/
    ├── validation-checklist.md
    └── fixtures/README.md
```

文件说明：

- `SKILL.md`：主 skill 指令，定义适用场景、输入处理、分析流程、输出风格和限制。
- `references/output-schema.json`：结构化输出字段约束。
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
- 用户描述墙砖空鼓、地漏排水慢、墙面开裂、插座位置异常等问题，要求判断严重程度和下一步处理方式。
- 项目经理希望按严重程度生成整改清单，便于和施工方沟通。

## 输出原则

默认使用简体中文输出巡检结果；`critical`、`high`、`confirmed`、`not_verifiable` 等结构化枚举值可以保留英文，并在需要时用中文解释。除非用户明确要求英文或其他语言，否则面向用户的判断、风险说明、整改建议和补充证据提示都应使用中文。

该 skill 的输出应尽量包含：

- 总体判断。
- 最紧急的下一步。
- 按严重程度排序的问题列表。
- 每个问题对应的图片或视频证据编号。
- 可能风险。
- 标准或参考依据。
- 整改建议。
- 置信度。
- 需要补充的证据。

## 注意事项

- 标准清单是初始参考源，正式用于合同、验收、维权或法律场景前，必须核对官方或授权标准文本。
- 该 skill 只能判断用户提供证据中可见的内容，不能替代现场监理、结构工程师、电工、水工、燃气或消防等专业人员。
- 对隐蔽工程、结构安全、电气安全、防水闭水、管道打压等问题，如果缺少照片、视频或测试记录，应输出证据不足，而不是给出确定结论。
