def create_html_report(json_data, html_file):
    """
    Generates an HTML report from a JSON file containing evaluation results.

    Args:
        json_file (str): Path to the JSON file.
        html_file (str): Path to the output HTML file.
    """

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Evaluation Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Evaluation Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Session ID</th>
                    <th>Collection ID</th>
                    <th>Tool Selection</th>
                    <th>Reasoning</th>
                    <th>Response Quality</th>
                    <th>Trajectory</th>
                    <th>At Par or Better</th>
                    <th>Links</th>
                </tr>
            </thead>
            <tbody>
    """

    for entry in json_data:
        session_id = entry["output"].get("session_id", "N/A")
        collection_id = entry["output"].get("collection_id", "N/A")
        tool_selection = entry["output"]["tool_selection"]
        reasoning = entry["output"]["reasoning"]
        response_quality = entry["output"]["response_quality"]
        trajectory = entry["output"]["trajectory"]
        at_par = "✅" if entry["output"]["at_par_or_better_than_existing"] else "❌"
        links = entry.get("links", [])

        html_content += f"""
                <tr>
                    <td>{session_id}</td>
                    <td>{collection_id}</td>
                    <td>{tool_selection}</td>
                    <td>{reasoning}</td>
                    <td>{response_quality}</td>
                    <td>{trajectory}</td>
                    <td>{at_par}</td>
                    <td>
                        <ul>
        """
        for link_data in links:
            print(links)
            print(link_data)
            link = link_data["link"]
            status_message = link_data["status_message"]
            html_content += f"<li><a href='{link}'>{status_message}</a></li>"
        html_content += """
                        </ul>
                    </td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(html_file, 'w') as f:
        f.write(html_content)

    print(f"HTML report saved to {html_file}")