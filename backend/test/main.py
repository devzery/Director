import logging
from services.agent_connector import call_director
from utils.reporter import create_html_report
from utils.file_handler import FileHandler
import json
from utils.process_input import remove_links, process_json_response
from evaluation.evaluator import evaluate_response
from datetime import datetime
from utils.logs import setup_logger

async def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("Starting Director evaluation process")
    
    try:
        data = FileHandler.load_json("test/data/director_conv.json")
        logger.info(f"Loaded conversation data with {len(data)} items")
        
        eval_results = []
        for idx, item in enumerate(data):
            
            logger.info(f"Processing item {idx+1}/{len(data)}")
            collection_id = item.get("collection_id")
            logger.info(f"Collection ID: {collection_id}")
            
            _, processed_data = remove_links(process_json_response(item))
            logger.info("Processed input data")
            session_id = None
            results = []
            
            conversation = item.get("conversation", [])
            logger.info(f"Found {len(conversation)} conversation messages")
            
            for i in conversation:
                if i.get("msg_type") == "input":
                    if not i.get("content"):
                        logger.warning("Empty content in input message")
                        continue
                        
                    prompt = i.get("content")[0].get("text", "")
                    logger.info(f"Processing prompt: {prompt[:50]}...")
                    try:
                        result = await call_director(prompt, session_id=session_id, collection_id=collection_id)
                        session_id = result.get("session_id")
                        logger.info(f"Received result with session ID: {session_id}")
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Error calling director API: {str(e)}")
                else:
                    logger.debug(f"Skipping message of type: {i.get('msg_type')}")
            
            print(json.dumps(results, indent=4))
            with open(f"test/data/raw_test-{idx}.json", "w") as f_out:
                json.dump(results, f_out, indent=4)
            logger.info(f"Retrieved {len(results)} results from Director API")
            # continue
            try:
                links, result = remove_links(process_json_response(results))
                print(json.dumps(result, indent=4))

                logger.info(f"Extracted {len(links)} links from results")
                with open("test/data/processed_test.json", "w") as f_out:
                    json.dump(result, f_out, indent=4)
                logger.info("Starting evaluation")
                eval_result = evaluate_response({"actual": result, "expected": processed_data})
                logger.info("Evaluation completed")
                
                eval_result["output"]["session_id"] = session_id
                eval_result["output"]["collection_id"] = collection_id
                eval_result["links"] = links
                
                eval_results.append(eval_result)
                logger.info(f"Added evaluation result for item {idx+1}")
            except Exception as e:
                logger.error(f"Error during evaluation: {str(e)}")

        logger.info("All items processed, generating report")
        
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with open("test/results/evaluation_report-{now_str}.json", "w") as f:
            json.dump(eval_results, f, indent=4)
        logger.info("Evaluation report JSON saved")
        
        create_html_report(eval_results, f"test/results/evaluation_report-{now_str}.html")
        logger.info("HTML report generated successfully")
        
        logger.info("Evaluation process completed")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())