def build_trace(retrieved):
    return [
        {
            "fact_id": item["id"],
            "source": item["source"]
        }
        for item in retrieved
    ]
