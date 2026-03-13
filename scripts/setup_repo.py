#!/usr/bin/env python3
"""
setup_repo.py — RadCom DevOps
Configura automaticamente um repositório novo na organização RadCom-Comunity:
  - Proteção de branches (dev e main)
  - Labels padrão
  - Branch dev criada
  - Copia os workflows de .github/

Uso:
  python scripts/setup_repo.py --repo NOME_DO_REPO --token SEU_TOKEN

Requisitos:
  pip install requests
"""

import argparse
import json
import sys
import requests

ORG = "RadCom-Comunity"

HEADERS = {}  # preenchido em runtime com o token

# ─── Labels padrão ────────────────────────────────────────────────────────────
DEFAULT_LABELS = [
    {"name": "bug",              "color": "d73a4a", "description": "Algo não está funcionando"},
    {"name": "feature",          "color": "0075ca", "description": "Nova funcionalidade"},
    {"name": "refactor",         "color": "e4e669", "description": "Melhoria de código sem mudança de comportamento"},
    {"name": "documentação",     "color": "0052cc", "description": "Melhorias ou adições à documentação"},
    {"name": "hardware",         "color": "f9d0c4", "description": "Relacionado ao hardware / pinagem"},
    {"name": "lembrete-diario",  "color": "c2e0c6", "description": "Issue automática de início do dia"},
    {"name": "sync-dev",         "color": "bfd4f2", "description": "Lembrete de sincronização com dev"},
    {"name": "release",          "color": "0e8a16", "description": "Release / versão publicada"},
    {"name": "wip",              "color": "fbca04", "description": "Work in progress — não revisar ainda"},
    {"name": "em-revisão",       "color": "d4c5f9", "description": "PR aguardando revisão"},
]

def api(method, path, **kwargs):
    url = f"https://api.github.com{path}"
    resp = getattr(requests, method)(url, headers=HEADERS, **kwargs)
    return resp

def setup_labels(repo):
    print(f"\n🏷️  Configurando labels em {repo}...")
    # Remove labels default do GitHub que não usamos
    existing = api("get", f"/repos/{ORG}/{repo}/labels").json()
    for label in existing:
        if label["name"] in ["enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix", "duplicate"]:
            api("delete", f"/repos/{ORG}/{repo}/labels/{label['name']}")
            print(f"   🗑️  Removido: {label['name']}")

    existing_names = {l["name"] for l in api("get", f"/repos/{ORG}/{repo}/labels").json()}
    for label in DEFAULT_LABELS:
        if label["name"] in existing_names:
            api("patch", f"/repos/{ORG}/{repo}/labels/{label['name']}", json=label)
            print(f"   ✏️  Atualizado: {label['name']}")
        else:
            r = api("post", f"/repos/{ORG}/{repo}/labels", json=label)
            if r.status_code == 201:
                print(f"   ✅ Criado: {label['name']}")
            else:
                print(f"   ⚠️  Erro ao criar {label['name']}: {r.text}")

def create_dev_branch(repo):
    print(f"\n🌿  Verificando branch dev em {repo}...")
    # Pega o SHA do main/master
    for base in ["main", "master"]:
        r = api("get", f"/repos/{ORG}/{repo}/git/ref/heads/{base}")
        if r.status_code == 200:
            sha = r.json()["object"]["sha"]
            # Tenta criar dev
            r2 = api("post", f"/repos/{ORG}/{repo}/git/refs", json={
                "ref": "refs/heads/dev",
                "sha": sha
            })
            if r2.status_code == 201:
                print(f"   ✅ Branch 'dev' criada a partir de '{base}'")
            elif r2.status_code == 422:
                print(f"   ℹ️  Branch 'dev' já existe")
            else:
                print(f"   ⚠️  Erro: {r2.text}")
            return
    print("   ⚠️  Não encontrou branch main ou master")

def protect_branch(repo, branch):
    print(f"\n🔒  Protegendo branch '{branch}' em {repo}...")
    payload = {
        "required_status_checks": {
            "strict": True,  # Exige que a branch esteja atualizada com dev antes do merge
            "contexts": ["Compilar com PlatformIO"]  # Nome do job no CI
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1  # Pelo menos 1 aprovação
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    r = api("put", f"/repos/{ORG}/{repo}/branches/{branch}/protection", json=payload)
    if r.status_code in [200, 201]:
        print(f"   ✅ Branch '{branch}' protegida com sucesso")
    else:
        print(f"   ⚠️  Erro ao proteger '{branch}': {r.status_code} — {r.text}")

def set_repo_settings(repo):
    print(f"\n⚙️  Ajustando configurações do repositório...")
    payload = {
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "allow_squash_merge": True,
        "allow_merge_commit": False,   # Forçar squash ou rebase
        "allow_rebase_merge": True,
        "delete_branch_on_merge": True  # Limpa branches após merge automático
    }
    r = api("patch", f"/repos/{ORG}/{repo}", json=payload)
    if r.status_code == 200:
        print("   ✅ Configurações aplicadas")
    else:
        print(f"   ⚠️  Erro: {r.text}")

def main():
    parser = argparse.ArgumentParser(description="Setup RadCom repo")
    parser.add_argument("--repo",  required=True, help="Nome do repositório (sem organização)")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token com permissão admin:org e repo")
    args = parser.parse_args()

    HEADERS["Authorization"] = f"token {args.token}"
    HEADERS["Accept"] = "application/vnd.github+json"
    HEADERS["X-GitHub-Api-Version"] = "2022-11-28"

    # Verifica se o repo existe
    r = api("get", f"/repos/{ORG}/{args.repo}")
    if r.status_code != 200:
        print(f"❌ Repositório '{args.repo}' não encontrado na org {ORG}.")
        sys.exit(1)

    print(f"🚀 Configurando repositório: {ORG}/{args.repo}\n{'='*50}")

    set_repo_settings(args.repo)
    create_dev_branch(args.repo)
    setup_labels(args.repo)
    protect_branch(args.repo, "dev")
    protect_branch(args.repo, "main")

    print(f"\n{'='*50}")
    print(f"✅ Setup completo para {ORG}/{args.repo}")
    print(f"   👉 Próximo passo: copie a pasta .github/ para o novo repo e dê push.")

if __name__ == "__main__":
    main()
