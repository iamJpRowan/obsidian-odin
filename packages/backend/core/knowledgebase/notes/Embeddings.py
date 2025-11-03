from __future__ import annotations

from typing import List

from core.knowledgebase import constants


class Embeddings:
    _local_model = None  # Cache for sentence-transformers model
    
    @staticmethod
    def get_embedding(text: str, model=None) -> List[float]:
        text = text.replace("\n", " ")
        
        if constants.EMBEDDING_PROVIDER == "local":
            # Use local sentence-transformers model
            if Embeddings._local_model is None:
                from sentence_transformers import SentenceTransformer
                model_name = model or constants.EMBEDDING_MODEL_NAME
                Embeddings._local_model = SentenceTransformer(model_name)
            return Embeddings._local_model.encode(text).tolist()
        else:  # openai
            import openai
            openai.api_key = constants.OPENAI_API_KEY
            model_name = model or constants.EMBEDDING_MODEL_NAME
            return openai.Embedding.create(input=[text], model=model_name)['data'][0]['embedding']


if __name__ == '__main__':
    print(Embeddings.get_embedding('bonaparte'))
