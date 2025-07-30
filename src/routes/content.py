from flask import Blueprint, request, jsonify
from src.models.content import db, ContentRequest, Client
import openai
import os

content_bp = Blueprint('content', __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

@content_bp.route('/content-requests', methods=['POST'])
def create_content_request():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'content_type', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new content request
        content_request = ContentRequest(
            name=data['name'],
            email=data['email'],
            company=data.get('company', ''),
            content_type=data['content_type'],
            message=data['message']
        )
        
        db.session.add(content_request)
        db.session.commit()
        
        # Generate AI content
        try:
            ai_content = generate_ai_content(data['content_type'], data['message'])
            content_request.ai_generated_content = ai_content
            content_request.status = 'in_progress'
            db.session.commit()
        except Exception as e:
            print(f"AI generation error: {e}")
            # Continue without AI content for now
        
        return jsonify({
            'message': 'Content request submitted successfully',
            'request_id': content_request.id,
            'status': content_request.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-requests', methods=['GET'])
def get_content_requests():
    try:
        requests = ContentRequest.query.order_by(ContentRequest.created_at.desc()).all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-requests/<int:request_id>', methods=['GET'])
def get_content_request(request_id):
    try:
        content_request = ContentRequest.query.get_or_404(request_id)
        return jsonify(content_request.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-requests/<int:request_id>', methods=['PUT'])
def update_content_request(request_id):
    try:
        content_request = ContentRequest.query.get_or_404(request_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            content_request.status = data['status']
        if 'human_reviewed_content' in data:
            content_request.human_reviewed_content = data['human_reviewed_content']
        
        db.session.commit()
        return jsonify(content_request.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/clients', methods=['POST'])
def create_client():
    try:
        data = request.get_json()
        
        # Check if client already exists
        existing_client = Client.query.filter_by(email=data['email']).first()
        if existing_client:
            return jsonify({'error': 'Client with this email already exists'}), 400
        
        client = Client(
            name=data['name'],
            email=data['email'],
            company=data.get('company', ''),
            plan=data.get('plan', 'starter'),
            brand_voice=data.get('brand_voice', '')
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
    try:
        clients = Client.query.order_by(Client.created_at.desc()).all()
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_ai_content(content_type, message):
    """Generate AI content using OpenAI"""
    try:
        prompt = f"""
        Create high-quality {content_type} content based on the following requirements:
        
        {message}
        
        Please ensure the content is:
        - Engaging and well-written
        - Appropriate for the specified content type
        - Professional in tone
        - Ready for human review and refinement
        
        Content:
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional content writer specializing in creating high-quality, engaging content for businesses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"AI content generation temporarily unavailable. Content type: {content_type}. Requirements: {message}"

