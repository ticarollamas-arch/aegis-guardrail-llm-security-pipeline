```
    ___    ___________ ____________
   /   |  / ____/ ____/  _/ ___/
  / /| | / __/ / / __ / / \__ \ 
 / ___ |/ /___/ /_/ // / ___/ / 
/_/  |_/_____/\____/___//____/  
  CISO ADJUNTO - TACTICAL GUARDRAIL
```

# Aegis Guardrail - LLM Security Pipeline

> **Objetivo:** Implementar contenção estéril e resiliente contra Prompt Injection e Jailbreak em pipelines de deploy automatizado.

## Sobre o Projeto
Implementar contenção estéril e resiliente contra Prompt Injection e Jailbreak em pipelines de deploy automatizado.

## 🛠️ Tecnologias e Módulos

- **Linguagens principais:** Python 3.11, Bash
- **Módulos nativos recomendados:** re, os, json, logging, sys
- **Dependências Externas:**
  - `pydantic` (^2.4.0): Validação estrita de schemas e payloads de entrada/saída.

## 🔒 Configurações de Segurança & Higiene Digital

- **Abordagem defensiva:** `DEFENSIVO - CRÍTICO`
- **Práticas de higiene digital:** Zero Trust, Rootless Containers, Imutabilidade, Sanitização Heurística
### Medidas de Mitigação Implementadas:
- **Risco / Ameaça:** Vazamento de Segredos → **Plano de Mitigação:** Uso exclusivo de variáveis de ambiente injetadas no runtime via Vault; ausência de hardcoding.
- **Risco / Ameaça:** Escalonamento de Privilégios → **Plano de Mitigação:** Execução via Podman Rootless, com filesystem read-only e drop de todas as capabilities (cap-drop=ALL).

## 💻 Interface de Linha de Comando (CLI)

- **Pre-requisito / Comando:** `./scripts/audit.sh`
- **Instruções de Inicialização:** `bash ./scripts/audit.sh [analyze|stress]`
### Argumentos & Flags Configurados:
- `a, analyze` (command): Analisa o histórico do git em busca de segredos expostos. (Exemplo: `./scripts/audit.sh analyze`)
- `s, stress` (command): Executa o container em modo efêmero e injeta payloads maliciosos para teste. (Exemplo: `./scripts/audit.sh stress`)

## 📂 Estrutura de Arquivos Criada

Este repositório foi construído de forma limpa e descompactada contendo os seguintes módulos funcionais:

- `Containerfile`
- `pipeline-ci.yml`
- `src/middleware.py`
- `src/rules.json`
- `scripts/audit.sh`

---
*Blueprint gerado com orgulho através do Senior Software Architecture Hub no AI Studio.*