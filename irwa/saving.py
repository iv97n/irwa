import csv


def save_scores_to_csv(doc_scores, filename):
    """
    Save document scores to a CSV file.

    Args:
        doc_scores (list): A list of tuples where each tuple contains a document ID and its score.
        filename (str): The name of the CSV file to save the results to.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Document ID", "Score"])
        
        # Write document scores
        for doc_id, score in doc_scores:
            writer.writerow([doc_id, score])

    print(f"Results saved to {filename}")