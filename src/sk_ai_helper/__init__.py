import logging


from utils.sklogger import logger
from utils.config_parser import SkConfig
from utils.http_tools import SkHttpClient

def query_ollama(ollama_host: str, query: str, model: str = "deepseek-r1:14b") -> str| None:
    http_client = SkHttpClient(ollama_host)
    resp = http_client.post_json("/api/generate", json={"prompt": query, "stream":False, "model": model})
    if resp.status_code >= 400:
        logger.error(f"query_ollama failed with status code {resp.status_code}, resp: {resp.content}")
        return
    return resp.json["response"] 

class OpenWebUIHelper:
    def __init__(self, open_webui_host: str,
                  open_webui_token: str) -> None:
        self.open_webui_host: str = open_webui_host
        self.open_webui_token: str = open_webui_token
        self.client: SkHttpClient = SkHttpClient(open_webui_host)
    
    def add_knowledge(self, knowledge: str) -> None:
        pass

    def get_knowledge(self) -> str:
        pass

    def query_with_knowledge(self, query: str, model: str) -> str:
        pass

    def query(self, query: str, model: str) -> str:
        pass


def main():
    config: SkConfig = SkConfig('config.ini')
    log_level: int = config.get_int('root', 'log_level', logging.INFO)
    logger.setLevel(log_level)
    logger.info('sk_ai_helper start...')

    ollama_host: str = config.get_str("ollama", "host", "http://192.168.13.207:11434")
    ollama_model: str = config.get_str("ollama", "model", "deepseek-r1:14b")

    open_webui_host: str = config.get_str("open_webui", "host", "http://192.168.13.207:3000")
    open_webui_token: str = config.get_str("open_webio", "token", "")

    question: str = "hello world"
    resp: str = query_ollama(ollama_host, question, ollama_model)
    logger.info(f" query_ollama resp: {resp}")




    logger.info('sk_ai_helper end...')




if __name__ == '__main__':
    main()
    


