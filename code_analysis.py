import openai
from pinecone import Pinecone, ServerlessSpec
import os

# Initialize OpenAI API Key and Pinecone API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Define the index name
index_name = "code-embeddings"

# Manually specify a supported region
region = "us-east-1"  # Replace with the valid region for your account

# Create or connect to the index
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Replace with the actual dimension of your embeddings
        metric="euclidean",  # You can use other metrics like "cosine"
        spec=ServerlessSpec(
            cloud="aws",  # Adjust the cloud provider if necessary
            region=region
        )
    )

# Initialize the index
index = pc.Index(index_name)


def get_embedding(text):
    chunks = split_text(text, max_chunk_size=4000)  # Split text into chunks
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(
            model="text-embedding-3-small",  # Correct embedding model
            input=[chunk]  # Input must be a list of strings
        )
        embeddings.append(response['data'][0]['embedding'])  # Append each embedding
    return embeddings



def split_code_into_chunks(code, max_chunk_size=500):
    # Split code into smaller chunks, each with a maximum size
    lines = code.splitlines()
    chunks = []
    current_chunk = []

    for line in lines:
        if len("\n".join(current_chunk)) + len(line) <= max_chunk_size:
            current_chunk.append(line)
        else:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
    
    if current_chunk:
        chunks.append("\n".join(current_chunk))  # Add the last chunk
    
    return chunks


def debug_pinecone_metadata():
    print("Stored metadata in Pinecone:")
    for vector in index.query(vector=[0.0] * 1536, top_k=10, include_metadata=True)["matches"]:
        print(f"ID: {vector['id']}, Metadata: {vector.get('metadata')}")


def store_embeddings_in_pinecone(chunks):
    try:
        for i, chunk in enumerate(chunks):
            # Truncate metadata to avoid exceeding the limit
            metadata = {"code": chunk[:4000]}  # Limit metadata size to ~4000 characters
            embedding = get_embedding(chunk)[0]  # Extract the first (and only) embedding
            index.upsert(
                vectors=[(str(i), embedding, metadata)]  # Store embedding with metadata
            )
    except Exception as e:
        print(f"Error storing embeddings: {e}")



def query_embeddings(query):
    query_embedding = get_embedding(query)[0]  # Extract the first (and only) embedding
    results = index.query(
        vector=query_embedding,
        top_k=5,  # Retrieve top 5 most similar vectors
        include_metadata=True  # Ensure metadata is included
    )

    # Debug: Print the retrieved matches
    print("Pinecone Query Results:")
    for match in results["matches"]:
        if "metadata" in match and "code" in match["metadata"]:
            print(f"ID: {match['id']}, Score: {match['score']}\nCode:\n{match['metadata']['code']}\n")
        else:
            print(f"ID: {match['id']}, Score: {match['score']} (No code found in metadata)\n")
    
    return results


def analyze_code_with_gpt(chunks):
    results = []
    for idx, chunk in enumerate(chunks):
        prompt = f"Here is a chunk of code:\n\n{chunk}\n\nPlease explain what this code does in detail."
        try:
            response = openai.Completion.create(
                model="gpt-4o-mini",
                prompt=prompt,
                max_tokens=16000  # Adjust based on response size
            )
            analysis_text = response['choices'][0]['text']
            results.append(f"### Analysis for Chunk {idx + 1}:\n\n{analysis_text}\n")
        except Exception as e:
            print(f"Error analyzing chunk {idx + 1}: {e}")
    return results


def interactive_query():
    while True:
        custom_prompt = input("Enter your custom prompt (or 'exit' to quit): ")
        if custom_prompt.lower() == 'exit':
            break
        similar_code = query_embeddings(custom_prompt)
        relevant_code = [result['metadata']['code'] for result in similar_code['matches']]
        analysis = analyze_code_with_gpt(relevant_code)
        print(f"Analysis: {analysis}")

def split_text(text, max_chunk_size=8000):
    # Split text into manageable chunks
    return [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]


def main():
    # Load your large code file
    with open('processed_code_output.txt', 'r', encoding='utf-8') as file:
        code = file.read()
        code_chunks = split_code_into_chunks(code)

        # Store embeddings in Pinecone
        store_embeddings_in_pinecone(code_chunks)

        # Query with a custom prompt
        query = input("Enter your prompt: ")
        similar_code = query_embeddings(query)

        # Construct the GPT prompt with relevant code snippets
        gpt_prompt = f"You have the following code snippets from the application:\n\n"
        for match in similar_code["matches"]:
            if "metadata" in match and "code" in match["metadata"]:
                gpt_prompt += f"### Code Snippet (ID: {match['id']}):\n{match['metadata']['code']}\n\n"
        
        # Check if any snippets were added
        if len(similar_code["matches"]) == 0 or "metadata" not in similar_code["matches"][0]:
            print("No relevant code snippets retrieved from Pinecone.")
            return

        gpt_prompt += f"### Question:\n{query}\n\nPlease provide a detailed response tailored to the code snippets provided above."

        # Generate GPT response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that tailors responses to specific code snippets."},
                    {"role": "user", "content": gpt_prompt}
                ],
                max_tokens=16000,
                temperature=0.7
            )
            gpt_response = response['choices'][0]['message']['content']

            # Save GPT response to markdown
            output_file = "gpt_response.md"
            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(f"# GPT Response\n\n## Prompt\n{query}\n\n## Response\n{gpt_response}")

            print(f"Response saved to {output_file}")

        except Exception as e:
            print(f"Error generating GPT response: {e}")



if __name__ == "__main__":
    main()
