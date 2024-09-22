# Website Querying App

Hello,
The application that I've built has a streamlit interface, which has 2 text boxes, one which takes a website url, and processes the website, and stores the vector embeddings in the Supabase database.

When a user enters query, the chunk is extracted and sent to tune studio to get the appropriate response.

## Steps to run:
### To run backend:
```
python3 main.py
```

### To run streamlit frontend:
```
streamlit run streamlit_app.py
```

## Screenshot:
![alt text](./Application%20working%20image.png)
![alt text](./Supabase%20Embeddings%20Image.png)
![alt text](./Website%20Ingestion.png)