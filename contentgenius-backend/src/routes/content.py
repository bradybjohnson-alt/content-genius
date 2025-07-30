from flask import Blueprint, request, jsonify
from src.models.content import db, ContentRequest, Client
import openai
import os

content_bp = Blueprint('content', __name__)

# AI Content Generation using OpenAI
def generate_ai_content(content_type, title, description, keywords, tone, target_audience, word_count):
    """Generate content using OpenAI API"""
    try:
        # Construct the prompt based on parameters
        prompt = f"""
        Create a {content_type} with the following specifications:
        
        Title: {title}
        Description: {description}
        Keywords to include: {keywords}
        Tone: {tone}
        Target Audience: {target_audience}
        Approximate word count: {word_count}
        
        Please create high-quality, engaging content that meets these requirements.
        """
        
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional content writer specializing in creating high-quality, engaging content for businesses. Always provide well-structured, original content that meets the specified requirements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=min(4000, word_count * 2) if word_count else 2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI content: {str(e)}")
        return None

@content_bp.route('/content-request', methods=['POST'])
def create_content_request():
    """Create a new content request"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['client_name', 'client_email', 'content_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new content request
        content_request = ContentRequest(
            client_name=data['client_name'],
            client_email=data['client_email'],
            company=data.get('company'),
            content_type=data['content_type'],
            title=data.get('title'),
            description=data.get('description'),
            keywords=data.get('keywords'),
            tone=data.get('tone', 'professional'),
            target_audience=data.get('target_audience'),
            word_count=data.get('word_count', 500)
        )
        
        db.session.add(content_request)
        db.session.commit()
        
        # Generate AI content if we have enough information
        if content_request.title and content_request.description:
            ai_content = generate_ai_content(
                content_request.content_type,
                content_request.title,
                content_request.description,
                content_request.keywords,
                content_request.tone,
                content_request.target_audience,
                content_request.word_count
            )
            
            if ai_content:
                content_request.ai_generated_content = ai_content
                content_request.status = 'review'
                db.session.commit()
        
        return jsonify({
            'message': 'Content request created successfully',
            'request_id': content_request.id,
            'status': content_request.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-requests', methods=['GET'])
def get_content_requests():
    """Get all content requests"""
    try:
        requests = ContentRequest.query.order_by(ContentRequest.created_at.desc()).all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-request/<int:request_id>', methods=['GET'])
def get_content_request(request_id):
    """Get a specific content request"""
    try:
        content_request = ContentRequest.query.get_or_404(request_id)
        result = content_request.to_dict()
        
        # Include AI generated content if available
        if content_request.ai_generated_content:
            result['ai_generated_content'] = content_request.ai_generated_content
        if content_request.final_content:
            result['final_content'] = content_request.final_content
            
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-request/<int:request_id>/status', methods=['PUT'])
def update_content_status(request_id):
    """Update content request status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['pending', 'in_progress', 'review', 'completed', 'delivered']:
            return jsonify({'error': 'Invalid status'}), 400
        
        content_request = ContentRequest.query.get_or_404(request_id)
        content_request.status = status
        
        # If final content is provided, update it
        if 'final_content' in data:
            content_request.final_content = data['final_content']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Status updated successfully',
            'status': content_request.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/clients', methods=['POST'])
def create_client():
    """Create a new client"""
    try:
        data = request.get_json()
        
        # Check if client already exists
        existing_client = Client.query.filter_by(email=data['email']).first()
        if existing_client:
            return jsonify({'error': 'Client with this email already exists'}), 400
        
        client = Client(
            name=data['name'],
            email=data['email'],
            company=data.get('company'),
            phone=data.get('phone'),
            subscription_plan=data.get('subscription_plan', 'starter')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'message': 'Client created successfully',
            'client_id': client.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/clients', methods=['GET'])
def get_clients():
    """Get all clients"""
    try:
        clients = Client.query.order_by(Client.created_at.desc()).all()
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/generate-content', methods=['POST'])
def generate_content_endpoint():
    """Generate content using AI (standalone endpoint for testing)"""
    try:
        data = request.get_json()
        
        required_fields = ['content_type', 'title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        ai_content = generate_ai_content(
            data['content_type'],
            data['title'],
            data['description'],
            data.get('keywords', ''),
            data.get('tone', 'professional'),
            data.get('target_audience', ''),
            data.get('word_count', 500)
        )
        
        if ai_content:
            return jsonify({
                'generated_content': ai_content,
                'status': 'success'
            }), 200
        else:
            return jsonify({'error': 'Failed to generate content'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

