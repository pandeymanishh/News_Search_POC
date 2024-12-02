def serp_google_search(query, serp_key, nws=False, top_res = 50):
    from serpapi import GoogleSearch
    import json

    params = {
      "api_key": serp_key,
      "engine": "google",
      "q": query,
      "location": "Austin, Texas, United States",
      "google_domain": "google.com",
      "gl": "us",
      "hl": "en",
      "num":top_res
    }
    if nws:
        params['tbm'] = "nws"
    # tbm:"nws"
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if results:
        results['query'] = query
        return results
    else:
        return None



def append_to_json(file_path, data):
    import json

    """
    Append a dictionary to a JSON file in JSON Lines format.
    Args:
        file_path (str): Path to the JSON file.
        data (dict): Dictionary to append to the file.
    """
    try:
        # Open the file in append mode
        with open(file_path, "a") as file:
            json.dump(data, file)  # Serialize dictionary as JSON
            file.write("\n")  # Add a newline after each dictionary
        print(f"Appended data to {file_path}")
    except Exception as e:
        print(f"Error appending data: {e}")


def read_json_as_dicts(file_path):
    """
    Read JSON Lines file and return a list of dictionaries.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        List[dict]: List of dictionaries read from the file.
    """
    import json
    data = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                data.append(json.loads(line))  # Deserialize each line into a dictionary
    except Exception as e:
        print(f"Error reading data: {e}")
    return data

def convert_to_month_year(date_str, ref_date):
    # Try parsing exact dates
    from datetime import datetime, timedelta
    import re
    try:
        parsed_date = datetime.strptime(date_str, "%b %d, %Y")
        return parsed_date.strftime("%b %Y")
    except ValueError:
        pass
    
    # Handle approximate dates like "X hours ago", "X days ago"
    match = re.match(r"(\d+)\s+(hour|day|week|month|year)s?\s+(ago|later)", date_str)
    if match:
        value, unit, direction = match.groups()
        value = int(value)
        if unit == "hour":
            delta = timedelta(hours=value)
        elif unit == "day":
            delta = timedelta(days=value)
        elif unit == "week":
            delta = timedelta(weeks=value)
        elif unit == "month":
            delta = timedelta(days=30 * value)  # Approximation
        elif unit == "year":
            delta = timedelta(days=365 * value)  # Approximation
        
        if direction == "ago":
            calculated_date = ref_date - delta
        else:
            calculated_date = ref_date + delta
        
        return calculated_date.strftime("%b %Y")
    
    return "Invalid format"

# Convert month-year format to the first day of the month
def convert_month_year_to_date(month_year_str):
    from datetime import datetime, timedelta
    try:
        return datetime.strptime(month_year_str, "%b %Y")
    except ValueError:
        return None
