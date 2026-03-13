# 🤝 Guia de Contribuição — RadCom

Esse documento explica o fluxo de trabalho Git adotado no time.
Leia uma vez, siga sempre. Dúvidas? Chame no grupo.

---

## 📐 Fluxo de trabalho

```
main  ─────────────────────────────────────── (produção / releases)
         ↑ merge via PR (CI obrigatório)
dev   ──●──────●──────●────────────────────── (integração)
         ↑           ↑
feature/xxx      feature/yyy               (branches pessoais)
```

### Regras de ouro

1. **Nunca commite direto na `dev` ou `main`** — sempre via Pull Request
2. **Sempre puxe a `dev` antes de começar** — evita retrabalho
3. **Uma branch por tarefa** — não misture features no mesmo PR
4. **Build verde antes de abrir PR** — rode `pio run` localmente

---

## 🌅 Início do dia (obrigatório)

```bash
# 1. Buscar atualizações remotas
git fetch origin

# 2. Atualizar sua dev local
git checkout dev
git pull origin dev

# 3. Criar branch para sua tarefa de hoje
git checkout -b feature/nome-da-sua-tarefa
```

> ⚠️ Se você já está no meio de uma feature, rode:
> ```bash
> git fetch origin
> git rebase origin/dev
> ```
> Isso reaplica seus commits por cima da dev atualizada.

---

## 📝 Convenção de Commits (obrigatório)

Formato: `tipo(escopo): descrição curta`

| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `refactor` | Melhoria sem mudar comportamento |
| `docs` | Documentação |
| `chore` | Config, dependências, CI |
| `test` | Adição/ajuste de testes |
| `perf` | Melhoria de performance |

### Exemplos

```bash
git commit -m "feat: adiciona leitura de temperatura via I2C"
git commit -m "fix: corrige overflow no buffer UART a 115200bps"
git commit -m "refactor(sensor): simplifica lógica de calibração do DHT22"
git commit -m "docs: atualiza README com diagrama de pinagem"
git commit -m "chore: atualiza dependências do platformio.ini"
```

> ❌ **Errado:**
> ```bash
> git commit -m "ajustes"
> git commit -m "corrigindo bug"
> git commit -m "WIP"
> ```

---

## 🔀 Abrindo um Pull Request

1. Empurre sua branch:
   ```bash
   git push origin feature/sua-tarefa
   ```

2. Abra o PR no GitHub apontando para `dev`

3. Preencha o template de PR completamente

4. Aguarde o CI rodar (build check automático)

5. Solicite review de pelo menos 1 colega

6. Após aprovação + CI verde → merge!

---

## 🏷️ Versionamento (tags)

Usamos [SemVer](https://semver.org/lang/pt-BR/): `vMAJOR.MINOR.PATCH`

| Parte | Quando incrementar |
|-------|-------------------|
| `MAJOR` (v**2**.0.0) | Mudança incompatível / hardware novo |
| `MINOR` (v1.**3**.0) | Nova funcionalidade compatível |
| `PATCH` (v1.3.**2**) | Correção de bug |

```bash
# Criar uma nova versão
git tag -a v1.2.0 -m "feat: suporte ao modem A7608SA"
git push origin v1.2.0
# → Isso dispara o workflow de Release automaticamente!
```

---

## 📁 Binários / Releases

Ao criar uma tag `v*.*.*` na `main`:
- ✅ O build roda automaticamente
- ✅ Um GitHub Release é criado com os binários `.bin`/`.hex`
- ✅ Os arquivos são nomeados: `{firmware}_{versão}_{ambiente}.bin`

Não copie binários manualmente. Use sempre as Releases do GitHub.

---

## 🆕 Criando um repositório novo

```bash
# 1. Crie o repo na organização GitHub normalmente
# 2. Clone e adicione o código inicial
# 3. Execute o script de setup:

python scripts/setup_repo.py --repo NOME_DO_REPO --token SEU_TOKEN

# 4. Copie a pasta .github/ para o novo repo:
cp -r .github/ /caminho/para/novo-repo/
cd /caminho/para/novo-repo
git add .github/
git commit -m "chore: adiciona workflows e configurações RadCom"
git push
```

Isso configura automaticamente: proteção de branches, labels, branch `dev` e todos os workflows.
