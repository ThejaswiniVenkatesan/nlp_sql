from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#  Step 1: Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast

#  Step 2: Reference questions
reference_questions = [
    "Total no of machines offline in cell 1 today",
    "Total no of machines active in cell 1 today",
    "Total no of machines idle in cell 1 today",
    "show me Machine with the highest downtime in site 1 padi",
    "Machine with the highest downtime in cell 2",
    "what is the total downtime of C-12 machine this month",
    "Machine with the most breakdown this month",
    "Total production of part no B 11458 in V-12 machine this month",
    "total active time of C-12 machine yesterday shift 1",
    "OEE percetange of v-12 machine from 2-06-25 to 08-06-25",
    "All users with superuser role",
    "assets which have been scrapped",
    "All currently running part and operation",
    "show me machines with the lowest OEE",
    "show me machines with oee above 80%",
    "show me production count yet",
    "How many machines are currently marked as Active?",
    "Show all Idle machines in Site 1.",
    "List all Offline machines across all cells.",
    "Get the number of machines in Shutdown mode.",
    "Fetch machines with status Not Active.",
    "Which assets are currently in Idle status in Site 3?",
    "Count all Active assets in Cell 2.",
    "What machines were updated today and are Offline?",
    "Retrieve all Active machines from PasP40Asset.",
    "How many assets are marked as Idle right now?",
    "Find all machines that are currently shut down.",
    "Get total number of Offline machines in Site 2.",
    "Which assets have Machine Status as Active in Site 1?",
    "Show machine IDs that are not Active.",
    "Get the machines where Machine_Status is 'Shutdown'.",
    "List machines marked as 'Idle' and updated today.",
    "How many assets are running in Site 1?",
    "Machines that have been idle for over 1 hour?",
    "What are all the Offline assets listed today?",
    "Get assets with P40_Machine_Status as 'Idle'.",
    "Retrieve count of Active assets by Site.",
    "Machines showing 'Not Active' in P40_Machine_Status.",
    "Total number of assets that were updated and are Idle.",
    "How many machines are Active but not in Site 1?",
    "Show all Offline machines along with last update time.",
    "Machines in PasP40Asset where status is Idle.",
    "Fetch count of Idle machines grouped by Site ID.",
    "List asset IDs that are shutdown in Site 3.",
    "Machines from PasP40Asset with P40_Is_Active = 0 and status Idle.",
    "Assets that are Offline and belong to Site 2."
]

#  Step 3: Precompute embeddings
ref_embeddings = model.encode(reference_questions)
print(" Model Loaded and Vector Index Ready!")
print("Type your question (or type 'exit' to quit)\n")

#  Step 4: Query loop
while True:
    user_question = input("🧑 You: ").strip()
    if user_question.lower() in ["exit", "quit"]:
        print("👋 Exiting...")
        break

    user_embedding = model.encode([user_question])
    similarities = cosine_similarity(user_embedding, ref_embeddings)[0]
    best_idx = similarities.argmax()
    best_match = reference_questions[best_idx]
    score = similarities[best_idx]

    if score < 0.55:
        print(" No strong match found. Try asking differently.\n")
    else:
        print(f"\n Best match: {best_match}")
        print(f" Similarity score: {score:.2f}\n")
