# Skill Install Recovery

If skill installation was interrupted, run:

```
mcp_call_tool({
  serverName: "system_tool_manager",
  toolName: "skill_install",
  arguments: {
    source: "local",
    path: "/Users/yjzhuang/.box/Workspace/output/28d94087-9a14-4296-8232-0a1005e6ff79/okf-memex",
    skillName: "okf-memex"
  }
})
```
