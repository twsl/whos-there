#!/bin/sh

curl -fsSL https://gh.io/copilot-install | bash
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 bash

curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | bash

curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | bash
codegraph init
