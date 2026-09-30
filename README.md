# How to Create a Vector Search Index in MongoDB

This repository contains the code samples for the "How to Create a Vector Search Index in MongoDB" tutorial. The sample project indexes a folder of text documents in MongoDB Atlas, then uses the index to answer questions about them. It covers:

- embedding generation with Voyage AI's free tier
- paragraph-based document chunking
- Atlas Vector Search index creation, setting by setting
- index status checks, and why `queryable` is the field to check
- question answering grounded in retrieved chunks, through a local language model
- editing, monitoring, and deleting the index

The project is written in Python. It uses the `voyage-4` embedding model, the `llama3.2:3b` model through [Ollama](https://ollama.com/), and a MongoDB Atlas free tier cluster.

## Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/download) installed on your machine
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register/) account with an M0 (free tier) cluster
- Your MongoDB Atlas connection string, available under **Database > Connect > Drivers** in the Atlas UI
- A Voyage AI model API key, created under **AI Model APIs** in the same Atlas project as your cluster

Add your current IP address to the MongoDB Atlas access list before you run any script. Go to **Security > Network Access** in the MongoDB Atlas UI and add it. Your scripts won't connect to your MongoDB cluster without this configuration.

## Clone the Repository

Run the following command to clone the repository to your machine:

```bash
git clone https://github.com/activus-d/vector-search-index-tutorial.git
```

## Set Up Your Environment

Navigate into the project folder:

```bash
cd vector-search-index-tutorial
```

If you use the Ollama desktop application, open it. If you use Ollama from the command line, start the server. This command holds its terminal, so leave it running and open a second terminal for the remaining steps:

```bash
ollama serve
```

In the second terminal, pull the language model:

```bash
cd vector-search-index-tutorial
ollama pull llama3.2:3b
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, create the virtual environment with `python -m venv venv`, and activate it with:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Create a file named `.env` in the project folder, and add your connection string and Voyage AI API key:

```
MONGODB_URI="<your-connection-string>"
VOYAGE_API_KEY="<your-voyage-api-key>"
```

Replace the placeholders with your own values.

## Run the Scripts

Run the scripts in this order:

1. Embed the sample documents and store them in Atlas:

   ```bash
   python ingest.py
   ```

   The script pauses 21 seconds after each embedding call, to stay within Voyage AI's free tier rate limits. Expect it to take about a minute for the three sample documents.

2. Create the Vector Search index. The script waits until the index is queryable:

   ```bash
   python create_index.py
   ```

3. Run a test search with a sample question:

   ```bash
   python search.py
   ```

4. Make sure Ollama is running, then start an interactive question-and-answer session:

   ```bash
   python ask.py
   ```

   Type a question at the prompt and press Enter. Try "What unalienable rights does the Declaration list?" Type `quit`, or press Enter on an empty line, to exit.

5. Check the index status:

   ```bash
   python manage_index.py
   ```

   To edit or delete the index, replace `show_index_status()` in the `__main__` block of `manage_index.py` with `update_quantization()` or `delete_index()`. A deleted index stops `search.py` and `ask.py` working until you run `create_index.py` again.

## Sample Documents

The `sample_documents` folder holds three public domain texts from [Project Gutenberg](https://www.gutenberg.org):

- The Declaration of Independence
- "A Modest Proposal" by Jonathan Swift
- "The Cask of Amontillado" by Edgar Allan Poe

To analyze your own documents, replace them with your own `.txt` files.

Refer to the tutorial for a full explanation of each index setting, the status values, and how the question-answering step works.
