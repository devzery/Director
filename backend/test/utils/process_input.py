import re


def remove_links(json_data: dict) -> tuple[dict, list]:
    """
    Process the JSON response to remove <a> tags and URL links while also returning the extracted links
    with their corresponding status messages (if available).

    Args:
        json_data (dict): The JSON data to process.

    Returns:
        tuple: A tuple containing:
               - dict: The processed JSON data with <a> tags and URL links replaced by placeholders.
               - list: A list of dictionaries, where each dictionary contains the
                     'link' and its corresponding 'status_message' (if found in the same content block).
    """
    def replace_links(content: str, status_message: str = None) -> tuple[str, list]:
        extracted_links = []

        # Extract and replace <a> tags
        tag_links = re.findall(r'<a\s+[^>]*href\s*=\s*["\']([^"\']+)["\']', content, flags=re.IGNORECASE)
        for link in tag_links:
            extracted_links.append({"link": link, "status_message": status_message})
        content = re.sub(r'<a\s+[^>]*>.*?</a>', '[LINK]', content, flags=re.DOTALL)

        # Extract and replace plain URLs
        plain_links = re.findall(r'http[s]?://\S+', content)
        for link in plain_links:
            extracted_links.append({"link": link, "status_message": status_message})
        content = re.sub(r'http[s]?://\S+', '[LINK]', content)

        return content, extracted_links

    extracted_links_with_status = []

    def process_data(data, current_status_message=None):
        nonlocal extracted_links_with_status
        if isinstance(data, dict):
            new_dict = {}
            status = data.get("status_message")
            new_status = status if status else current_status_message
            for key, value in data.items():
                if isinstance(value, str):
                    new_content, links = replace_links(value, new_status)
                    new_dict[key] = new_content
                    extracted_links_with_status.extend(links)
                elif isinstance(value, (dict, list)):
                    processed_value, links = process_data(value, new_status)
                    new_dict[key] = processed_value
                    extracted_links_with_status.extend(links)
                else:
                    new_dict[key] = value
            return new_dict, []  
        elif isinstance(data, list):
            new_list = []
            for item in data:
                if isinstance(item, str):
                    new_content, links = replace_links(item, current_status_message)
                    new_list.append(new_content)
                    extracted_links_with_status.extend(links)
                elif isinstance(item, (dict, list)):
                    processed_item, links = process_data(item, current_status_message)
                    new_list.append(processed_item)
                    extracted_links_with_status.extend(links)
                else:
                    new_list.append(item)
            return new_list, []
        else:
            return data, []

    processed_data, _ = process_data(json_data)
    return extracted_links_with_status, processed_data


    

def process_json_response(json_data) -> object:
    """
    Process the JSON to remove unwanted key value pairs from the response.
    
    Supports both dictionaries and lists, including nested lists.
    
    Args:
        json_data (dict or list): The JSON data to process.

    Returns:
        dict or list: The processed JSON data.
    """
    if isinstance(json_data, list):
        return [process_json_response(item) for item in json_data]

    elif isinstance(json_data, dict):
        # Remove unwanted keys from the dictionary
        unwanted_keys = [
            "conv_id",
            "created_at",
            "metadata",
            "msg_id",
            "status",
            "updated_at",
            "session_id",
            "user_id",
            "collection_id",
        ]
        for key in unwanted_keys:
            json_data.pop(key, None)

        # Recursively process values that are dicts or lists
        for key, value in json_data.items():
            if isinstance(value, (dict, list)):
                json_data[key] = process_json_response(value)

        return json_data

    return json_data

# # Save the processed data to a new file
# # with open("test/data/processed_test.json", "w") as f_out:
# #     json.dump(processed_data, f_out, indent=4)
# # print("Processed data saved to processed_test.json")