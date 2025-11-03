import google.generativeai as genai
from PIL import Image

def generate_rag_response(query, retrieved_chunks, image_paths=None):
    model = genai.GenerativeModel("gemini-2.5-pro")  # Supports images

    context = "\n".join(retrieved_chunks)
    prompt = f"""Answer the question based on the provided context and image(s) if any.

    Context:
    {context}

    Question:
    {query}
    """

    inputs = [prompt]

    if image_paths:
        for img_path in image_paths:
            try:
                img = Image.open(img_path)
                inputs.append(img)
            except Exception:
                pass  # Ignore corrupted or unreadable images

    response = model.generate_content(inputs)
    return response.text
