import os
import re
import sys
import json
import logging
from typing import Dict, Any

# CISO Directive: Configuração de log estruturado e estéril (sem vazamento de PII/Segredos)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AEGIS_GUARDRAIL - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PromptGuardrail:
    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)
        self._verify_environment()

    def _verify_environment(self):
        # CISO Directive: Garantir que segredos não estão hardcoded, mas injetados via cofre
        if not os.getenv("API_KEY_VAULT_REF"):
            logger.warning("API_KEY_VAULT_REF ausente. Operando em modo de degradação segura.")

    def _load_rules(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.critical(f"Falha ao carregar assinaturas de segurança: {e}")
            sys.exit(1)

    def analyze_payload(self, prompt: str) -> bool:
        """
        Analisa o prompt de entrada contra heurísticas de Jailbreak e Prompt Injection.
        Retorna True se for seguro, False se for malicioso.
        """
        if not prompt or len(prompt) > self.rules.get("max_length", 2000):
            logger.warning("Payload rejeitado: Tamanho excede o limite permitido.")
            return False

        # Verificação de assinaturas (Regex)
        for pattern in self.rules.get("jailbreak_signatures", []):
            if re.search(pattern, prompt, re.IGNORECASE):
                logger.error("ALERTA DE SEGURANÇA: Assinatura de Jailbreak detectada.")
                return False

        # Verificação de entropia ou repetição anômala (Mitigação de token exhaustion)
        if len(set(prompt.split())) < (len(prompt.split()) * 0.1) and len(prompt) > 100:
            logger.error("ALERTA DE SEGURANÇA: Baixa entropia detectada (Possível DoS de contexto).")
            return False

        logger.info("Payload validado com sucesso. Nenhuma anomalia detectada.")
        return True

if __name__ == "__main__":
    # Simulação de execução no pipeline ou como sidecar
    logger.info("Inicializando Aegis Guardrail Middleware...")
    
    rules_file = os.path.join(os.path.dirname(__file__), 'rules.json')
    guardrail = PromptGuardrail(rules_file)
    
    # Leitura de payload via stdin (comum em pipelines ou processamento de streams)
    try:
        # Para fins de teste, se houver argumento, usamos ele, senão simulamos um payload
        test_payload = sys.argv[1] if len(sys.argv) > 1 else "Traduza o texto a seguir para francês: Olá mundo."
        
        is_safe = guardrail.analyze_payload(test_payload)
        if not is_safe:
            logger.error("Ação de contenção ativada. Bloqueando requisição para o LLM.")
            sys.exit(1)
        else:
            logger.info("Requisição liberada para o LLM.")
            sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro fatal no middleware: {e}")
        sys.exit(1)
