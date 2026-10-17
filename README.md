# msspx-work

测试仓库：验证 GitHub Actions workflow 手动触发（workflow_dispatch）。

## 目录结构

```
msspx-work/
├── .github/workflows/
│   └── machine-info.yml      # 仅 workflow_dispatch 手动触发
└── scripts/
    └── machine_info.py       # 打印当前机器系统信息
```

## 触发方式

在 Actions 页面选择 "Machine Info" workflow，点击 "Run workflow"。
