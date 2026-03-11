# Ralplan

A publishable Claude Code plugin repository for consensus planning without OMC or Trellis.

## Package status

This repository is prepared as a **Claude Code plugin repository** using the standard plugin layout:

- manifest in `.claude-plugin/plugin.json`
- root-level `skills/`, `agents/`, and `hooks/`
- hook registration in `hooks/hooks.json`
- runtime state stored in the target project's `.claude/ralplan/state.json`

## Intended installation flow

After publishing the repository, if this repository is also used as a marketplace source, users should be able to install it in marketplace style:

```text
/plugin marketplace add https://github.com/blackzhuge/ralplan
/plugininstall ralplan
```

For local development/testing:

```text
cc --plugin-dir E:\\SourceCode\\ralplan
```

## Contents

- Skill: `skills/ralplan/SKILL.md`
- Agents:
  - `agents/planner-ralplan.md`
  - `agents/architect-ralplan.md`
  - `agents/critic-ralplan.md`
- Hooks:
  - `hooks/hooks.json`
  - `hooks/ralplan-init.py`
  - `hooks/ralplan-session-start.py`
  - `hooks/ralplan-stop.py`
- Manifest: `.claude-plugin/plugin.json`

## Publishing notes

1. Publish this directory as a GitHub repository.
2. Add the repository to Claude Code marketplace sources.
3. Install the plugin by manifest name `ralplan`.
4. Keep runtime state in the target project, not in the plugin repository.
