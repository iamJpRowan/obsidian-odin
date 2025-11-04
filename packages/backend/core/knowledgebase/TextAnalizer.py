from __future__ import annotations

from pathlib import Path
import os
import re

from langchain import PromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

from core.knowledgebase import constants


class TextAnalizer:
    def __init__(self: TextAnalizer) -> None:

        # Initialize LLM based on provider
        if constants.LLM_PROVIDER == "ollama":
            from langchain_community.chat_models import ChatOllama
            self.model = ChatOllama(
                model=constants.LLM_MODEL_NAME,
                temperature=constants.LLM_MODEL_TEMPERATURE,
                base_url=constants.OLLAMA_BASE_URL
            )
        else:  # openai
            from langchain_openai import ChatOpenAI
            self.model = ChatOpenAI(
                openai_api_key=constants.OPENAI_API_KEY,
                temperature=constants.LLM_MODEL_TEMPERATURE,
                model_name=constants.LLM_MODEL_NAME
            )

        # Try to use improved prompts if they exist, fall back to original
        self.prompt_names = [
            'prompt_generate_improved', 'system_message_generate_improved',
            'prompt_update', 'system_message_update',
            'prompt_question', 'system_message_question',
            'prompt_explain', 'system_message_explain',
            'prompt_optimize', 'system_message_optimize',
            'prompt_debug', 'system_message_debug',
        ]
        self.prompts = {}
        self.init_prompts()

        self.messages = []

        return

    @staticmethod
    def extract_cypher_from_response(response: str) -> str:
        """
        Extract Cypher code from LLM response.
        
        Handles cases where LLM returns:
        1. Pure Cypher code
        2. Cypher in markdown code blocks (```cypher ... ``` or ``` ... ```)
        3. Explanations followed by Cypher code
        
        Returns the extracted Cypher code, or the original response if no code block found.
        """
        # Try to find Cypher code in markdown code blocks
        # Match ```cypher ... ``` or ``` ... ``` where content looks like Cypher
        code_block_patterns = [
            r'```cypher\s*\n(.*?)```',
            r'```cql\s*\n(.*?)```',  # CQL is another name for Cypher
            r'```\s*\n((?:CREATE|MERGE|MATCH|DELETE|SET|RETURN|WITH|UNWIND).*?)```',
        ]
        
        for pattern in code_block_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                cypher = match.group(1).strip()
                # Remove any leading/trailing whitespace and comments
                cypher = re.sub(r'^\s*//.*$', '', cypher, flags=re.MULTILINE)
                return cypher.strip()
        
        # If no code block found, look for Cypher-like content after certain keywords
        # Common patterns: "Cypher Queries:", "Queries:", "Code:", etc.
        cypher_keywords = [
            r'(?:Cypher\s+Queries?|Queries?|Code):\s*\n',
            r'<cypher>\s*',
        ]
        
        for keyword_pattern in cypher_keywords:
            parts = re.split(keyword_pattern, response, flags=re.IGNORECASE)
            if len(parts) > 1:
                potential_cypher = parts[-1].strip()
                # Check if it starts with Cypher keywords
                if re.match(r'^\s*(CREATE|MERGE|MATCH|DELETE|SET|RETURN)', potential_cypher, re.IGNORECASE):
                    # Remove markdown code blocks if present
                    potential_cypher = re.sub(r'```.*?```', '', potential_cypher, flags=re.DOTALL)
                    return potential_cypher.strip()
        
        # If response starts with Cypher keywords, assume it's pure Cypher
        if re.match(r'^\s*(CREATE|MERGE|MATCH|DELETE|SET|RETURN)', response, re.IGNORECASE):
            return response.strip()
        
        # Last resort: return original response (will likely fail, but preserves info)
        return response.strip()
    
    @staticmethod
    def fix_common_cypher_errors(cypher: str) -> str:
        """
        Fix common syntax errors in generated Cypher queries.
        
        Common issues:
        - MATCH after CREATE in same query
        - Invalid date functions (DATETIME -> string)
        - Inline node creation in relationships
        """
        lines = cypher.split('\n')
        fixed_lines = []
        has_create = False
        has_match = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            # Fix: Replace DATETIME() with string (Memgraph doesn't have DATETIME function)
            if 'DATETIME(' in line.upper() or 'datetime(' in line:
                import re
                # Extract datetime value and convert to string
                line = re.sub(r'datetime\(["\']([^"\']+)["\']\)', r'"\1"', line, flags=re.IGNORECASE)
                line = re.sub(r'DATETIME\(["\']([^"\']+)["\']\)', r'"\1"', line)
            
            # Fix: Remove MATCH statements that come after CREATE
            if line.upper().startswith('CREATE'):
                has_create = True
                fixed_lines.append(line)
            elif line.upper().startswith('MERGE'):
                fixed_lines.append(line)
            elif line.upper().startswith('MATCH'):
                # Only allow MATCH if we haven't done CREATE in this batch
                if not has_create:
                    fixed_lines.append(line)
                # Otherwise skip it (MATCH won't find nodes just created)
            elif line.upper().startswith('SET'):
                # SET is fine after CREATE/MERGE
                fixed_lines.append(line)
            elif line.upper().startswith('ON CREATE'):
                fixed_lines.append(line)
            elif ':' in line and ('->' in line or '<-' in line):
                # Relationship statement
                # Fix: Can't create nodes inline in relationships
                # Pattern: (node)-[:REL]->(new:Type {...})
                import re
                # Check for inline node creation
                inline_pattern = r'\([^:)]+:[^)]+\{[^}]+\}\)'
                if re.search(inline_pattern, line):
                    # Split into separate CREATE and relationship
                    # This is complex, so just warn for now
                    pass
                fixed_lines.append(line)
            else:
                # Other statements
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)

    def init_prompts(self: TextAnalizer) -> None:

        for prompt_name in self.prompt_names:
            prompt_path = Path(os.path.join(
                os.path.dirname(__file__), 'prompts', prompt_name))
            # If improved prompt doesn't exist, fall back to original
            if not prompt_path.exists() and '_improved' in prompt_name:
                original_name = prompt_name.replace('_improved', '')
                prompt_path = Path(os.path.join(
                    os.path.dirname(__file__), 'prompts', original_name))
            if prompt_path.exists():
                prompt_text = prompt_path.read_text()
                prompt_template = PromptTemplate.from_template(prompt_text)
                self.prompts[prompt_name] = prompt_template
            else:
                # Fall back to original if neither exists
                original_name = prompt_name.replace('_improved', '')
                fallback_path = Path(os.path.join(
                    os.path.dirname(__file__), 'prompts', original_name))
                if fallback_path.exists():
                    prompt_text = fallback_path.read_text()
                    prompt_template = PromptTemplate.from_template(prompt_text)
                    self.prompts[prompt_name] = prompt_template
        return

    def text_to_cypher_create(self: TextAnalizer, text: str, repo_path: str, file_path: str) -> str:
        # Use improved prompts if available, fall back to original
        system_prompt_key = 'system_message_generate_improved' if 'system_message_generate_improved' in self.prompts else 'system_message_generate'
        user_prompt_key = 'prompt_generate_improved' if 'prompt_generate_improved' in self.prompts else 'prompt_generate'
        
        self.messages = [
            SystemMessage(
                content=self.prompts[system_prompt_key].format()),
            HumanMessage(content=self.prompts[user_prompt_key].format(
                prompt=text, repo_path=repo_path, file_path=file_path))
        ]
        response = self.model.predict_messages(self.messages).content
        cypher = TextAnalizer.extract_cypher_from_response(response)
        # Fix common syntax errors
        cypher = TextAnalizer.fix_common_cypher_errors(cypher)
        return cypher

    def data_and_text_to_cypher_update(self: TextAnalizer, data: str, text: str, repo_path: str, file_path: str) -> str:
        self.messages = [
            SystemMessage(
                content=self.prompts['system_message_update'].format()),
            HumanMessage(content=self.prompts['prompt_update'].format(
                data=data, prompt=text, repo_path=repo_path, file_path=file_path))
        ]
        response = self.model.predict_messages(self.messages).content
        cypher = TextAnalizer.extract_cypher_from_response(response)
        # Fix common syntax errors
        cypher = TextAnalizer.fix_common_cypher_errors(cypher)
        return cypher

    def generate_questions(self: TextAnalizer, text: str) -> str:
        self.messages = [
            SystemMessage(
                content=self.prompts['system_message_question'].format()),
            HumanMessage(
                content=self.prompts['prompt_question'].format(prompt=text))
        ]
        return self.model.predict_messages(self.messages).content

    def _general_code_question(self: TextAnalizer, prompt_name: str, text: str) -> str:
        self.messages = [
            SystemMessage(
                content=self.prompts[f'system_message_{prompt_name}'].format()),
            HumanMessage(
                content=self.prompts[f'prompt_{prompt_name}'].format(code=text))
        ]
        return self.model.predict_messages(self.messages).content

    def optimize_code_style(self: TextAnalizer, text: str) -> str:
        return self._general_code_question('optimize', text)

    def explain_code(self: TextAnalizer, text: str) -> str:
        return self._general_code_question('explain', text)

    def debug_code(self: TextAnalizer, text: str) -> str:
        return self._general_code_question('debug', text)


if __name__ == '__main__':

    ta = TextAnalizer()

    example_reponame = 'History'
    example_repopath = os.path.join(os.path.dirname(
        __file__), 'examples', example_reponame)

    example_fname = 'napoleon.txt'
    example_fpath = os.path.join(example_repopath, example_fname)

    example_text = Path(example_fpath).read_text()

    ret = ta.text_to_cypher_create(
        example_text, example_repopath, example_fname)
    print(ret)

    questionable_text = """Napoleon initiated many liberal reforms that have persisted, 
    and is considered one of the greatest ever military commanders. His campaigns are still studied at military academies worldwide."""
    ret = ta.generate_questions(questionable_text)
    print(ret)

    code = """
        def evens(l):
            return [x for x in l if x % 2 == 0]
    """

    ret = ta.explain_code(code)
    print(ret)
