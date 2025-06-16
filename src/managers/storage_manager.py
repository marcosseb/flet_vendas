import json
from typing import Dict, Any, Optional

class StorageManager:
    """Gerenciador centralizado de armazenamento de dados"""
    
    def __init__(self, page):
        self.page = page
        self.initialize_storage()
    
    def initialize_storage(self):
        """Inicializa o armazenamento com valores padrão"""
        # Verifica se é a primeira execução
        if not self.page.client_storage.get("app_initialized"):
            self.set_default_values()
            self.page.client_storage.set("app_initialized", True)
    
    def set_default_values(self):
        """Define valores padrão para o aplicativo"""
        defaults = {
            "theme_mode": "light",
            "usuario_logado": None,
            "empresa_logada": None,
            "configuracoes": {
                "notificacoes": True,
                "tema_automatico": False
            }
        }
        
        for key, value in defaults.items():
            if not self.page.client_storage.get(key):
                self.page.client_storage.set(key, value)
    
    def get_user_data(self, username: str) -> Optional[Dict]:
        """Recupera dados completos do usuário"""
        from data import usuarios
        return next((u for u in usuarios if u["usuario"] == username), None)
    
    def update_empresa_name(self, new_name: str):
        """Atualiza nome da empresa em todos os locais necessários"""
        # Atualiza no storage
        self.page.client_storage.set("empresa_logada", new_name)
        
        # Atualiza nos dados do usuário
        usuario_logado = self.page.client_storage.get("usuario_logado")
        if usuario_logado:
            from data import usuarios
            for usuario in usuarios:
                if usuario["usuario"] == usuario_logado:
                    usuario["empresa"] = new_name
                    break
        
        # Força atualização da página
        self.page.update()
    
    def get_theme_mode(self) -> str:
        """Recupera o modo de tema salvo"""
        return self.page.client_storage.get("theme_mode") or "light"
    
    def set_theme_mode(self, mode: str):
        """Salva o modo de tema"""
        self.page.client_storage.set("theme_mode", mode)
    
    def is_logged_in(self) -> bool:
        """Verifica se há usuário logado"""
        return bool(self.page.client_storage.get("usuario_logado"))
    
    def get_empresa_name(self) -> str:
        """Recupera nome da empresa atual"""
        return self.page.client_storage.get("empresa_logada") or "Empresa não identificada"
    
    def logout(self):
        """Limpa dados de sessão"""
        self.page.client_storage.remove("usuario_logado")
        self.page.client_storage.remove("empresa_logada")
