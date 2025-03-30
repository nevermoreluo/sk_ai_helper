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
        self.headers = {"Authorization": f"Bearer {open_webui_token}", "Content-Type": "application/json"}
        self.knowledge_cache = []
    
    def add_knowledge(self, knowledge: str) -> None:
        pass

    def update_knowledge(self, knownledge: str) -> None:
        pass


    def get_knowledge(self) -> str:
        """
        获取知识库列表
        """
        uri = "/api/v1/knowledge/"
        self.knowledge_cache = self.client.get_json(uri, headers=self.headers).json
        return self.knowledge_cache

    def query_with_knowledge(self, query: str, model: str) -> str:
        """
        匹配所有知识库id也可以选择指定id的知识库查询
        """
        uri = "/api/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": query}],
            "files": [{'type': 'collection', 'id': k.get("id")} for k in self.get_knowledge() if k.get("id")]
        }
        resp = self.client.post_json(uri, json=data, headers=self.headers)
        return resp.json

    def query(self, query: str, model: str) -> str:
        pass





def main():
    config: SkConfig = SkConfig('config.ini')
    log_level: int = config.get_int('root', 'log_level', logging.INFO)
    logger.setLevel(log_level)
    logger.info('sk_ai_helper start...')

    ollama_host: str = config.get_str("ollama", "host", "http://192.168.13.207:11434")
    ollama_model: str = config.get_str("ollama", "model", "deepseek-r1:14b")

    open_webui_host: str = config.get_str("open_webui", "host", "http://192.168.13.207:8080")
    open_webui_token: str = config.get_str("open_webio", "token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM1MDhhOTUzLWM5YjUtNDEzMC1iZmE0LTdiNjQzMmEwMmRkZiJ9.178U963OzrC7nKeiy7I08uvHjwguBJXQF2FMirrUdeI")

    question: str = "hello world"
    # resp: str = query_ollama(ollama_host, question, ollama_model)
    # logger.info(f" query_ollama resp: {resp}")
    open_webui_helper = OpenWebUIHelper(open_webui_host, open_webui_token)
    resp = open_webui_helper.query_with_knowledge("李浩然", "deepseek-r1:14b")
    logger.info(resp)

    # logger.info(f"knowledge: {open_webui_helper.get_knowledge()}")



    logger.info('sk_ai_helper end...')




if __name__ == '__main__':
    main()
    


