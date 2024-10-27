# Semantic Chunking 

# Semantic chunking segments documents based on meaningful units like sentences or paragraphs. 
# It creates embeddings for each segment and combines them based on cosine similarity until a significant drop is detected, forming a new chunk.

import re 
from collections import Counter
import math 
from flask import Flask, render_template ,request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key= 'your_secret_key'

 
class cosine_similarity:                  # method now computes the cosine similarity between two vectors (no more return from __init__)
    
    def __init__(self, vec1, vec2):
        self.vec1= vec1
        self.vec2= vec2
    
    def compute_similarity(self):
        
        intersection = set(self.vec1.keys()) & set(self.vec2.keys())
        numerator= sum([self.vec1[x]* self.vec2[x] for x in intersection])
    
        sum1= sum([self.vec1[x]**2 for x in self.vec1.keys()])
        sum2= sum([self.vec2[x]**2 for x in self.vec2.keys()])
        denominator= math.sqrt(sum1) * math.sqrt(sum2)
    
        if not denominator:
            return 0.0
        return float(numerator) / denominator
    
 # func to create an embedding
 
def create_embedding(text):                     #function now properly creates word embeddings from text.
    words = re.findall(r'\w+', text.lower())
    return Counter(words)
    
class Semantingchunking:
    
    def __init__(self, text, similarity_threshold=0.5):
        self.text = text
        self.similarity_threshold= similarity_threshold
        
    def chunk_text(self):               #method handles the semantic chunking of the input text.
        
        sentences = re.split(r'(?<=[.!?])\s+', self.text)
        chunks = []
        current_chunk = sentences[0]
        current_embedding = create_embedding(current_chunk)
    
        for sentence in sentences[1:]:
            sentence_embedding = create_embedding(sentence)
            similarity = cosine_similarity(current_embedding, sentence_embedding).compute_similarity()
        
            if similarity >= self.similarity_threshold:
                current_chunk += " " + sentence
                current_embedding = create_embedding(current_chunk)
        
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
                current_embedding = sentence_embedding
            
        chunks.append(current_chunk)
        return chunks
    
# Define the route for the homepage
@app.route('/', methods= ['GET', 'POST'])
def index():
    text= None
    chunks = None
    
    if request.method=='POST':
        text= request.form.get("text")
        if text:
            semantic_chunker= Semantingchunking(text)     # semantic_chunking function is called properly, and the chunks are returned to the template.
            chunks = semantic_chunker.chunk_text()
        else:
            flash("Please enter some text!", "error")    #A flash message is triggered if no text is provided.
        
    return render_template('semantic_chunk.html', text= text, chunks= chunks)

if __name__=="__main__":
    app.run(debug= True)

# text = "This is a sample text. It demonstrates semantic chunking. We split based on meaning. New topics start new chunks."
# chunks = semantic_chunking(text)
# print(chunks)

