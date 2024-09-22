from rag.utils import extract_website_data, create_embeddings
import time
extract_website_data("https://in.pycon.org/cfp/2024/proposals/", start_time=time.time())
extract_website_data("https://in.pycon.org/2024/", start_time=time.time())
# create_embeddings("/Users/omkhade/Projects/pycon/poki_friendly_pycon_guide/pycon_website_2.txt") 