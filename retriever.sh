#!/bin/bash

# Run the retriever
uvicorn src.retriever:app --host 0.0.0.0 --port 5678
