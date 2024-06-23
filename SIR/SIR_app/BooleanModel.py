import os
import re
from .Read import read_doc_file

# Function to read all documents
def read_documents():
    list_files = [
        '1.doc', '2.doc', '3.doc', '4.doc', '5.doc', '6.doc', '7.doc', '8.doc', '9.doc',
        'M0.doc', 'M1.doc', 'M2.doc', 'M3.doc', 'M4.doc', 'M5.doc', 'M6.doc', 'M7.doc',
        'M8.doc', 'M9.doc', 'M10.doc', 'M11.doc', 'M12.doc'
    ]
    documents = {}
    for file in list_files:
        document_text = read_doc_file(file)
        if document_text is not None:
            documents[file] = document_text
        else:
            print(f"Warning: Failed to read {file}. Skipping.")

    return documents

# Function to preprocess text
def preprocess(text):
    if text is None:
        return set()  # Return an empty set if text is None
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return set(words)

# Function to create inverted index
def create_index(documents):
    index = {}
    for doc, text in documents.items():
        words = preprocess(text)
        for word in words:
            index.setdefault(word, []).append(doc)
    return index

# Function to parse query
def parse_query(query):
    query = preprocess(query)
    stack = []
    precedence = {"not": 3, "and": 2, "or": 1}
    for word in query:
        if word in precedence:
            while stack and stack[-1] in precedence and precedence[word] <= precedence[stack[-1]]:
                yield stack.pop()
            stack.append(word)
        else:
            yield word
    while stack:
        yield stack.pop()

# Function to evaluate query
def evaluate_query(query, index):
    query = parse_query(query)
    stack = []
    for word in query:
        if word in {"not", "and", "or"}:
            if stack:
                a = stack.pop()
            else:
                a = set()
            if stack:
                b = stack.pop()
            else:
                b = set()

            if word == "not":
                stack.append(a - b)
            elif word == "and":
                stack.append(a & b)
            elif word == "or":
                stack.append(a | b)
        else:
            stack.append(set(index.get(word, [])))
    return stack.pop() if stack else set()

# Function to display query results
def show(query):
    # Read the documents from a folder
    documents = read_documents()

    # Create an inverted index from the documents
    index = create_index(documents)

    result = evaluate_query(query, index)
    result_text = ", ".join(result) if result else "None"
    return result_text
