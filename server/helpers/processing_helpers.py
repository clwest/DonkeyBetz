# process urls into batches
def process_in_batches(urls, batch_size, process_function):
    """Process documents in batches"""
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i : i + batch_size]
        print(
            f"Processing batch of {i//batch_size + 1} : URLs {i} to {i + batch_size - 1}"
        )
        process_function(batch_urls)
        print(f"Finished processing batch {i//batch_size + 1}")
