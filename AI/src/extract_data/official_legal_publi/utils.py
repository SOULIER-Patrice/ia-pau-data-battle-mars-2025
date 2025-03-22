import csv


def save_as_csv(data, csv_filename):
    """
    Save data to a CSV file.
    
    Args:
        data (list[dict]): List of dictionaries to save
        csv_filename (str): Path to save the CSV file
    """
    # Write to CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        # Define column names from the keys of the first dictionary
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header (column names)
        writer.writeheader()
        
        # Write data rows
        writer.writerows(data)
        
    print(f"File {csv_filename} saved successfully!")