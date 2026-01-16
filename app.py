# =============================================
# 🧠 Literary Chat with Richard Wagner (Windows)
# =============================================

# 1. Prevent multiprocessing issues on Windows
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Required on Windows
    multiprocessing.set_start_method("spawn", force=True)

    # 2. Import main libraries
    from sentence_transformers import SentenceTransformer, util
    import nltk
    from nltk.tokenize import sent_tokenize
    import torch

    # 3. Download NLTK resources (only the first time)
    nltk.download("punkt", quiet=True)

    # 4. Path to your text file
    file_path = r"C:\Users\neyma\Desktop\RWagner.txt"  # Use raw string for Windows paths

    # 5. Read the text file
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 6. Split the text into sentences
    sentences = sent_tokenize(raw_text)

    # 7. Load the model
    print("🧩 Loading model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 8. Generate embeddings (uses GPU if available)
    print("⚙️ Generating embeddings...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True, device=device)

    # 9. Function to answer questions
    def answer_question(question, top_k=5):
        question_embedding = model.encode(question, convert_to_tensor=True, device=device)
        similarities = util.cos_sim(question_embedding, sentence_embeddings)[0]
        top_indices = similarities.topk(k=top_k).indices
        answers = [sentences[i] for i in top_indices]
        return answers

    # 10. Interactive chat loop
    print("\n📚 Literary Chat with Richard Wagner — Ask a question (or type 'exit'):\n")

    while True:
        try:
            question = input("You: ")
            if question.lower().strip() in ["exit", "quit", "sair"]:
                print("Chat closed.")
                break

            answers = answer_question(question)
            print("\nAnswer(s):")
            for a in answers:
                print("-", a)
            print("\n---\n")

        except KeyboardInterrupt:
            print("\nChat interrupted by user.")
            break
