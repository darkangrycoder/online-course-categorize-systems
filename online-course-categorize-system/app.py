import gradio as gr
import onnxruntime as rt
from transformers import AutoTokenizer
import torch
import json

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

# Load genre types from a JSON file
try:
    with open("genre_types_encoded.json", "r") as fp:
        encode_genre_types = json.load(fp)
except FileNotFoundError:
    print("Error: 'genre_types_encoded.json' not found. Make sure the file exists.")
    exit(1)

# Extract genres from the loaded data
genres = list(encode_genre_types.keys())

# Load the ONNX inference session
try:
    inf_session = rt.InferenceSession('udemy-classifier-quantized.onnx')
    input_name = inf_session.get_inputs()[0].name
    output_name = inf_session.get_outputs()[0].name
except FileNotFoundError:
    print("Error: 'udemy-classifier-quantized.onnx' not found. Make sure the file exists.")
    exit(1)

# Define the function for classifying courses' genres
def classify_courses_genre(description):
    input_ids = tokenizer(description, truncation=True, padding=True, return_tensors="pt")['input_ids'][:,:512]
    logits = inf_session.run([output_name], {input_name: input_ids.cpu().numpy()})[0]
    logits = torch.FloatTensor(logits)
    probs = torch.sigmoid(logits)[0]
    return dict(zip(genres, map(float, probs)))

# Create the Gradio interface
iface = gr.Interface(fn=classify_courses_genre, inputs="text", outputs=gr.components.Label(num_top_classes=5))

# Launch the Gradio interface
iface.launch(inline = False)
