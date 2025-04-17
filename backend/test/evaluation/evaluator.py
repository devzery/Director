import json
import logging
from director.constants import RoleTypes
from director.llm.videodb_proxy import VideoDBProxy
from director.core.session import ContextMessage
from prompts.evaluator import EVALUATOR_PROMPT

logger = logging.getLogger(__name__)

def evaluate_response(response: dict):
    """Process a single example and return the evaluation result."""
    llm = VideoDBProxy()

    system_prompt = ContextMessage(
        content=EVALUATOR_PROMPT,
        role=RoleTypes.system,
    )

    evaluation_data = ContextMessage(
        content=json.dumps(response),
        role=RoleTypes.user,
    )
    logger.info(f"Evaluating response: {evaluation_data.content}")
    llm_response = llm.chat_completions(
        [system_prompt.to_llm_msg(), evaluation_data.to_llm_msg()],
        response_format={"type": "json_object"},
    )

    output = json.loads(llm_response.content) 
    logger.info(f"Evaluation output: {output}")
    return {
        "output": output,
    }