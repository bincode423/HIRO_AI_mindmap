from flask import Flask, render_template, request, jsonify
import json
import os
from ollama import chat

app = Flask(__name__)

def generate_subkeywords_from_ollama(option: str, size: int, deep: bool = False):
    # try:
    if not deep:
        keywords = set()       
        while len(keywords) < size:
            prompt = f'When I give you a keyword, return exactly {size} unique sub-keywords related to it, separated by spaces. Do not include any explanations or extra text. Match the language of the input keyword.'
            stream = chat(model="exaone3.5:7.8b", messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": option}
            ], stream=True)
            
            rt = ''
            for chunk in stream:
                rt += chunk.message.content
            new_keywords = set(rt.split())
            keywords = keywords.union(new_keywords)
        return list(keywords)[:size]
    else:
        keywords = {}
        size = size * 10
        while len(keywords) < size:
            prompt = f'When I give you a keyword, return exactly {size} unique sub-keywords related to it, separated by spaces. Do not include any explanations or extra text. Match the language of the input keyword.'
            stream = chat(model="exaone3.5:7.8b", messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": option}
            ], stream=True)
            rt = ''
            for chunk in stream:
                rt += chunk.message.content
            
            new_keywords = list(rt.split())
            for k in new_keywords:
                if k not in keywords:
                    keywords[k] = 0
                keywords[k] += 1
        new_key = list(keywords.items())
        sorted_keywords = []
        for tp in new_key:
            sorted_keywords.append((tp[1],tp[0]))
        sorted_keywords.sort()
        return [tp[1] for tp in sorted_keywords[:size//10]]
        
    # except Exception as e:
    #     print(f"Ollama error")
    #     return ['AI 키워드 생성 실패']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-subkeywords', methods=['POST'])
def generate_subkeywords():
    try:
        data = request.get_json() or {}
        keyword = data.get('keyword', '').strip()
        size = data.get('size', 5)  # Default to 5 if not provided
        deep = bool(data.get('deep', False))
        
        print(f"Received request: keyword='{keyword}', size={size}")  # Debug log
        
        if not keyword:
            return jsonify({"error": "No keyword provided"}), 400
        
        if size < 1 or size > 10:
            return jsonify({"error": "Size must be between 1 and 10"}), 400
            
        subkeys = generate_subkeywords_from_ollama(keyword, size, deep)
        print(f"Generated subkeys: {subkeys}")  # Debug log
        
        if not subkeys:
            return jsonify({"error": "Failed to generate keywords"}), 500
            
        return jsonify({"subkeywords": subkeys})
    
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/load-map/<name>', methods=['GET'])
def load_map(name):
    fname = os.path.join('saved_maps', name + '.json')
    if not os.path.exists(fname):
        return jsonify({"error": "not found"}), 404
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
