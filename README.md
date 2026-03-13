# ⚙️ RadCom DevOps — Automação de repositórios

Conjunto de workflows, scripts e templates para padronizar o desenvolvimento
de firmwares embarcados (C++ / PlatformIO) na organização **RadCom-Comunity**.

---

## 📦 O que está incluído

```
.github/
├── workflows/
│   ├── ci-build-check.yml      # ✅ Bloqueia PR se o build falhar
│   ├── release-publish.yml     # 🚀 Gera Release + binários ao taguear
│   ├── changelog.yml           # 📝 Gera CHANGELOG.md automaticamente
│   ├── lint-commits.yml        # 🔍 Valida mensagens de commit no PR
│   └── morning-reminder.yml    # 🌅 Lembrete diário de sync com dev
├── pull_request_template.md    # 📋 Template de PR obrigatório
scripts/
└── setup_repo.py               # 🤖 Configura repo novo automaticamente
CONTRIBUTING.md                 # 📖 Guia de fluxo Git para o time
```

---

## 🚀 Como aplicar em um repositório

### 1. Copie a pasta `.github/` para o repositório

```bash
cp -r .github/ /caminho/para/seu-repo/
cd /caminho/para/seu-repo
git add .github/
git commit -m "chore: adiciona workflows RadCom DevOps"
git push
```

### 2. Execute o script de setup (uma vez por repo)

```bash
pip install requests

python scripts/setup_repo.py \
  --repo NOME_DO_REPO \
  --token ghp_SeuTokenAqui
```

> O token precisa de permissões: `repo` + `admin:org`
> Gere em: https://github.com/settings/tokens

### 3. Configure as variáveis de repositório (opcional)

Para habilitar cópia automática à pasta de rede:

| Variável | Valor exemplo | Descrição |
|----------|---------------|-----------|
| `NETWORK_SHARE_ENABLED` | `true` | Ativa cópia para pasta de rede |
| `NETWORK_SHARE_PATH` | `/mnt/firmwares` | Caminho da pasta compartilhada |

Configure em: **Settings → Secrets and variables → Actions → Variables**

---

## 🔒 O que o setup configura automaticamente

| Recurso | Detalhes |
|---------|----------|
| Branch `dev` criada | A partir da `main`/`master` |
| Proteção da `dev` | PR obrigatório + CI verde + 1 aprovação |
| Proteção da `main` | PR obrigatório + CI verde + 1 aprovação |
| Labels padrão | `bug`, `feature`, `refactor`, `docs`, `hardware`, `release`, `wip`… |
| Delete branch on merge | Branches limpas após merge |
| Squash merge | Histórico limpo na `dev` |

---

## 🛠️ Problemas resolvidos

| # | Problema | Solução |
|---|----------|---------|
| 1 | Merge de código quebrado na `dev` | CI bloqueia PR se `pio run` falhar |
| 2 | Devs esquecendo de puxar a `dev` | Issue automática às 08h com checklist |
| 3 | Falta de documentação nos commits | Lint de commits + template de PR + CHANGELOG automático |
| 4 | Cópia manual de binários | Release automático com binários nomeados ao criar tag |
| 5 | Setup manual em cada repo novo | Script `setup_repo.py` + copiar `.github/` |

---

## 📋 Fluxo resumido do dia a dia

```
Início do dia
  └─ git pull origin dev
  └─ git checkout -b feature/sua-tarefa

Desenvolvimento
  └─ git commit -m "feat: descrição clara"   ← siga a convenção!

Pronto para revisar
  └─ git push origin feature/sua-tarefa
  └─ Abrir PR → dev no GitHub
  └─ CI roda build automaticamente
  └─ Colega revisa e aprova
  └─ Merge!

Nova versão
  └─ git tag -a v1.2.0 -m "release: v1.2.0"
  └─ git push origin v1.2.0
  └─ Release + binários gerados automaticamente 🎉
```

---

## ❓ Dúvidas

Consulte o [CONTRIBUTING.md](./CONTRIBUTING.md) para o guia completo de fluxo Git.
