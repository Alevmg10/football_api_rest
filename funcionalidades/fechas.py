from datetime import datetime

def compare_dates(response_date_str):
    # Parse the date string from the response into a datetime object
    response_date = datetime.strptime(response_date_str, "%Y-%m-%dT%H:%M:%SZ")

    # Get the current date and time as a datetime object
    current_date = datetime.utcnow()

    # Compare the two datetime objects
    if response_date > current_date:
        return "The response date is in the future."
    elif response_date < current_date:
        return "The response date is in the past."
    else:
        return "The response date is today."

# Example usage
response_date_str = "2024-06-22T19:00:00Z"
result = compare_dates(response_date_str)
print(result)
