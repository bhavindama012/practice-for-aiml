import fitz  # PyMuPDF
import easyocr
from groq import Groq
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("--- Step 1: Loading & Embedding Scanned Book (Done Once) ---")
pdf_path = "my_document2.pdf"  # Your scanned PDF file

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Open PDF natively using PyMuPDF
doc_file = fitz.open(pdf_path)
raw_documents = []

# Loop through pages (process the book once)
for page_num in range(0,5):
    print(f"Running OCR on page {page_num + 1} of {len(doc_file)}...")
    page = doc_file[page_num]
    pix = page.get_pixmap(dpi=100)
    image_bytes = pix.tobytes("png")
    
    results = reader.readtext(image_bytes)
    page_text = "\n".join([result[1] for result in results])
    
    doc = Document(
        page_content=page_text,
        metadata={"source": pdf_path, "page": page_num + 1}
    )
    raw_documents.append(doc)

print(f"Successfully processed {len(raw_documents)} pages.")

print("--- Step 2: Chunking & Creating Vector Database ---")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(raw_documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from a .env file if you have one
api_key = os.getenv("GROQ_API_KEY")

# Pass it to Groq
client = Groq(api_key=api_key)
print("\n" + "="*50)
print("🤖 RAG Chatbot is Ready! Ask anything about your PDF.")
print("Type 'exit' or 'quit' to end the chat.")
print("="*50 + "\n")

# Interactive Chat Loop
while True:
    query = input("\nAsk a question: ").strip()
    
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
        
    if not query:
        continue

    print("Searching document and generating answer...")
    relevant_docs = retriever.invoke(query)

    # Combine retrieved text chunks as context
    context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
    pages = [doc.metadata.get('page') for doc in relevant_docs]

    # Prompt the LLM using the retrieved context
    prompt = f"""
    You are a helpful AI document assistant. Answer the user's question accurately using ONLY the provided context below. 
    If the answer cannot be found in the context, say "I can't find that in the document."
    Always mention the source page number(s) in your response.

    Context:
    {context_text}

    User Question: {query}
    """

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # <-- Updated active production model ID
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    print(f"\n--- Answer ---")
    print(completion.choices[0].message.content)
    print(f"\n📚 Source Pages: {pages}")