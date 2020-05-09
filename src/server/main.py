from flask import Flask, jsonify
from src.core.knowledge_service import KnowledgeService
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/knowledge')
def get_knowledge():
    knowledge_service = KnowledgeService()
    knowledge = knowledge_service.list_knowledge()
    return jsonify([item.as_dict() for item in knowledge])
