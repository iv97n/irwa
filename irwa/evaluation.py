import numpy as np


def precision_at_k(doc_score, y_score, k=10):
    """
    Parameters
    ----------
    doc_score: Ground truth (true relevance labels).
    y_score: Predicted scores.
    k : number of doc to consider.

    Returns
    -------
    precision @k : float
    recall @k : float

    """
    order = np.argsort(y_score)[::-1]
    doc_score = doc_score[order[:k]]
    relevant = sum(doc_score == 1)
    precision = float(relevant) / k

    total_relevant = sum(doc_score)
    if total_relevant == 0:
        recall = 0
    else:
        recall = float(relevant) / total_relevant
    return precision, recall


def avg_precision_at_k(doc_score, y_score, k=10):
    """
    Parameters
    ----------
    doc_score: Ground truth (true relevance labels).
    y_score: Predicted scores.
    k : number of doc to consider.

    Returns
    -------
    average precision @k : floa
    """
    order = np.argsort(y_score)[::-1]  # get the list of indexes of the predicted score sorted in descending order.

    prec_at_i = 0
    prec_at_i_list = []
    number_of_relevant = 0
    number_to_iterate = min(k, len(order))

    for i in range(number_to_iterate):
        if doc_score[order[i]] == 1:
            number_of_relevant += 1
            prec_at_i = number_of_relevant / (i + 1)
            prec_at_i_list.append(prec_at_i)

    if number_of_relevant == 0:
        return 0
    else:
        return np.sum(prec_at_i_list) / number_of_relevant
  
  
def f1_score(precision, recall):

    if precision + recall == 0:
        return 0.0
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1


def map_at_k(search_res, k=10):
    """
    Parameters
    ----------
    search_res: search results dataset containing:
        query_id: query id.
        doc_id: document id.
        predicted_relevance: relevance predicted through LightGBM.
        doc_score: actual score of the document for the query (ground truth).
    k:

    Returns
    -------
    mean average precision @ k : float
    """
    avp = []
    for q in search_res["query_id"].unique():  # Loop over all query id
        curr_data = search_res[search_res["query_id"] == q]  # Select data for current query
        avp.append(avg_precision_at_k(np.array(curr_data["is_relevant"]),
                   np.array(curr_data["predicted_relevance"]), k))  # Append average precision for current query
    return np.sum(avp) / len(avp), avp  # return mean average precision


def rr_at_k(doc_score, y_score, k=10):
    """
    Parameters
    ----------
    doc_score: Ground truth (true relevance labels).
    y_score: Predicted scores.
    k : number of doc to consider.

    Returns
    -------
    Reciprocal Rank for qurrent query
    """

    # Get the list of indexes of the predicted score sorted in descending order.
    order = np.argsort(y_score)[::-1]
    # Sort the actual relevance label of the documents based on predicted score(hint: np.take) and take first k.
    doc_score = np.take(doc_score, order[:k])
    # If there are no relevant documents return 0
    if np.sum(doc_score) == 0:
        return 0
    return 1 / (np.argmax(doc_score == 1) + 1)


def dcg_at_k(doc_score, y_score, k=10):
    # Get the list of indexes of the predicted score sorted in descending order.
    order = np.argsort(y_score)[::-1]
    # Sort the actual relevance label of the documents based on predicted score(hint: np.take) and take first k.
    doc_score = np.take(doc_score, order[:k])
    # Compute gain (use formula 7 above)
    gain = 2 ** doc_score - 1
    # Compute denominator
    discounts = np.log2(np.arange(len(doc_score)) + 2)
    # Return dcg@k
    return np.sum(gain / discounts)


def ndcg_at_k(doc_score, y_score, k=10):
    dcg_max = dcg_at_k(doc_score, doc_score, k)
    if not dcg_max:
        return 0
    return np.round(dcg_at_k(doc_score, y_score, k) / dcg_max, 4)
