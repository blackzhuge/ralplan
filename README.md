# ralplan

这是一个可发布的 Claude Code plugin 仓库，目标是提供与 OMC 类似的插件安装体验，同时保持 `ralplan` 的独立共识规划能力。

## 安装

发布到 GitHub 后，如果该仓库同时作为 marketplace 源，也可以按如下方式安装：

```text
/plugin marketplace add https://github.com/blackzhuge/ralplan
/plugin install ralplan
```

本地开发测试也可以直接使用插件目录：

```text
cc --plugin-dir E:\\SourceCode\\ralplan
```

## 仓库结构

- `.claude-plugin/plugin.json`：插件 manifest
- `skills/ralplan/SKILL.md`：主技能
- `agents/planner-ralplan.md`：Planner 代理
- `agents/architect-ralplan.md`：Architect 代理
- `agents/critic-ralplan.md`：Critic 代理
- `hooks/hooks.json`：插件 hooks 配置
- `hooks/ralplan-init.py`：初始化状态
- `hooks/ralplan-session-start.py`：恢复未完成流程
- `hooks/ralplan-stop.py`：阻止未完成时提前退出

## 使用

```text
/ralplan "你的任务描述"
```

可选参数：

```text
/ralplan --interactive --deliberate "你的任务描述"
```

## 运行时状态

插件仓库采用官方 plugin 目录结构；运行时状态仍写入目标项目：

```text
.claude/ralplan/state.json
```

## 说明

- 不依赖 OMC / Trellis
- Hook 仅依赖 Python 标准库
- Architect 与 Critic 严格串行，不并行
