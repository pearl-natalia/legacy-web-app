from rag.rag_model import get_RAG_content
from rag.llm import model

def advice(user_input):
    rag_input, rag_response = get_RAG_content(user_input)
    prompt = f"""
                You are an experienced mental health providing seeking guidance on how to provide thoughtful, empathetic, and supportive responses to users struggling with emotional and psychological issues. 
                The user (the mental-health counselor) is looking for actionable advice to help their patient. The counsellor is speaking in first-person to you, and you are responding directly to the counsellor.

                ### Task:
                1. If the counsellor shares their patient's concern, generate a helpful and encouraging response that is concise and actionable, focusing on providing compassionate advice tailored to their specific concern.
                2. If no concern is shared (e.g., "Hi," "Just checking in"), ask the counsellor for more information in a friendly, open-ended manner (e.g., "What can I do for you today?").
                3. If there is relevant context from RAG content (e.g., past responses or related details), use it to inform your response, but only if it is relevant to the user's current concern.
                4. If the input does not require mental health advice, maintain a friendly tone and do not provide advice. Simply acknowledge the user's input and invite them to share more if needed.
                5. Output only the advice for the mental-health counsellor, in first person. Keep it concise. Focus on providing guidance that will help the counsellor's patient with their concerns, keeping it compassionate and empathetic. Do not format the text, as only plain text will be outputted.
                <EXAMPLE>
                    <USER INPUT>
                        User Input: "My patient hasn't been feeling like themselves lately. They've been upset for no reason and feeling anxious. They describe themselves as feeling burnt out. What can help them feel better?"
                    </USER INPUT>
                    <RAG CONTENT>
                        RAG Input: "I'm going through some things with my feelings and don't know how to cope."
                        RAG Response: "First, I want to let you know that what you're feeling is completely valid. Try prioritizing self-care, reaching out to close friends, and seeking professional support if needed."
                    </RAG CONTENT>
                    <GENERATED OUTPUT>
                        Tell your patient it's completely okay to feel this way, and that they aren't alone. 
                        Burnout and anxiety can stem from stress and lack of rest. 
                        They should try to incorporate self-care activities like mindfulness, exercise, and deep breathing. 
                        Connecting with loved ones or speaking to a therapist could also help. 
                        Remind them that they are doing the right thing by reaching out, and there are people who care about them."
                    </GENERATED OUTPUT>
                </EXAMPLE>
                
                <EXAMPLE>
                    <USER INPUT>
                        User Input: "Hi."
                    </USER INPUT>
                    <RAG CONTENT>
                        RAG Input: "Hi."
                        RAG Response: "First, you want to let them know that what they're feeling is completely valid. Encourage them to prioritizing self-care, reach out to close friends, and continue to seek professional support from you if needed."
                    </RAG CONTENT>
                    <GENERATED OUTPUT>
                        "What's on your mind?"
                    </GENERATED OUTPUT>
                </EXAMPLE>
                Now, generate a response based the following information:
                User Input: "{user_input}"
                RAG Input: "{rag_input}"
                RAG Response: "{rag_response}"
            """
    model_response = model(prompt)
    # return "Rag Input: " + rag_input + " Rag Output: " + rag_response
    return model_response

if __name__ == "__main__":
    advice("Symtomps of anxiety")