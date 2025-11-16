"""
Lehigh Student Academic Marketplace
A comprehensive marketplace for textbooks, supplies, and academic essentials
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime

from planner.budget_planner import BudgetPlanner

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lehigh-marketplace-2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('uploads/syllabi', exist_ok=True)
os.makedirs('uploads/listings', exist_ok=True)

# Initialize planner
budget_planner = BudgetPlanner()


@app.route('/')
def index():
    """Main marketplace page"""
    return render_template('marketplace.html', page='explore')


@app.route('/for-your-classes')
def for_your_classes():
    """For Your Classes page"""
    return render_template('marketplace.html', page='for-your-classes')


@app.route('/sell')
def sell_page():
    """Sell Something page"""
    return render_template('sell.html')


@app.route('/my-listings')
def my_listings():
    """My Listings page"""
    return render_template('marketplace.html', page='my-listings')


@app.route('/saved')
def saved():
    """Saved/Bookmarked listings"""
    return render_template('marketplace.html', page='saved')


@app.route('/listing/<listing_id>')
def listing_detail(listing_id):
    """Individual listing detail page"""
    return render_template('listing_detail.html', listing_id=listing_id)


@app.route('/messages')
def messages_page():
    """Messages inbox page"""
    return render_template('messages.html')


# Serve uploaded listing images
@app.route('/uploads/listings/<filename>')
def uploaded_listing_image(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'listings'), filename)


@app.route('/api/marketplace/upload_image', methods=['POST'])
def upload_listing_image():
    """Upload an image for a listing and return its public URL"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        dest = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', filename)
        file.save(dest)

        public_url = f"/uploads/listings/{filename}"
        return jsonify({'success': True, 'url': public_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Generate and store CAPTCHA challenge
@app.route('/api/auth/captcha', methods=['POST'])
def generate_captcha_challenge():
    """Generate a CAPTCHA challenge and store it server-side"""
    try:
        data = request.json
        challenge = data.get('challenge', '')
        correct_indices = data.get('correctIndices', [])
        
        # Store CAPTCHA challenge in session
        session['current_captcha'] = {
            'challenge': challenge,
            'correctIndices': correct_indices
        }
        session.modified = True
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Authentication with nickname and validation
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with email, nickname, and validation"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        nickname = data.get('nickname', '').strip()
        captcha_answer = data.get('captcha_answer')
        captcha_question = data.get('captcha_question', '')
        
        # Validate email
        if not email or '@' not in email:
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400
        
        # Require Lehigh email
        if not email.endswith('@lehigh.edu'):
            return jsonify({'success': False, 'error': 'Please use a Lehigh email address (@lehigh.edu)'}), 400
        
        # Validate nickname
        if not nickname:
            return jsonify({'success': False, 'error': 'Nickname is required'}), 400
        
        nickname_validation = budget_planner.validate_nickname(nickname)
        if not nickname_validation['valid']:
            return jsonify({'success': False, 'error': nickname_validation['error']}), 400
        
        # Server-side CAPTCHA validation - STRICT: Must pass to login
        if captcha_answer is None or not captcha_question:
            return jsonify({'success': False, 'error': 'CAPTCHA verification is required'}), 400
        
        # Get stored CAPTCHA data from session
        stored_captcha = session.get('current_captcha')
        if not stored_captcha:
            return jsonify({'success': False, 'error': 'CAPTCHA session expired. Please refresh and try again.'}), 400
        
        # Validate CAPTCHA using stored challenge and answer
        captcha_valid = budget_planner.validate_captcha(
            stored_captcha.get('challenge'),
            stored_captcha.get('correctIndices'),
            captcha_answer
        )
        if not captcha_valid:
            return jsonify({'success': False, 'error': 'CAPTCHA verification failed. Please solve the challenge correctly.'}), 400
        
        # Clear CAPTCHA from session after successful validation
        session.pop('current_captcha', None)
        
        # Create or get user
        user = budget_planner.get_or_create_user(email, nickname)
        return jsonify({
            'success': True, 
            'user': {
                'email': user['email'],
                'nickname': user.get('nickname', nickname)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Marketplace Listings
@app.route('/api/marketplace/listings', methods=['GET'])
def get_listings():
    """Get marketplace listings with filters"""
    try:
        category = request.args.get('category', '')
        class_code = request.args.get('class', '')
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', '')
        max_price = request.args.get('max_price', '')
        condition = request.args.get('condition', '')
        page = request.args.get('page', 'explore')
        
        listings = budget_planner.get_marketplace_listings(
            category=category,
            class_code=class_code,
            search=search,
            min_price=min_price,
            max_price=max_price,
            condition=condition,
            page=page
        )
        return jsonify({'success': True, 'listings': listings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/listings', methods=['POST'])
def create_listing():
    """Create a new marketplace listing"""
    try:
        data = request.json
        listing = budget_planner.create_marketplace_listing(data)
        return jsonify({'success': True, 'listing': listing})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get a single listing"""
    try:
        listing = budget_planner.get_listing(listing_id)
        if listing:
            return jsonify({'success': True, 'listing': listing})
        return jsonify({'success': False, 'error': 'Listing not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    """Update a listing"""
    try:
        data = request.json
        listing = budget_planner.update_listing(listing_id, data)
        return jsonify({'success': True, 'listing': listing})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    """Delete a listing"""
    try:
        budget_planner.delete_listing(listing_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/listings/<listing_id>/sold', methods=['POST'])
def mark_sold(listing_id):
    """Mark a listing as sold"""
    try:
        budget_planner.mark_listing_sold(listing_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Bookmarks/Saved
@app.route('/api/marketplace/bookmarks', methods=['GET'])
def get_bookmarks():
    """Get user's bookmarked listings"""
    try:
        email = request.args.get('email', '')
        bookmarks = budget_planner.get_bookmarks(email)
        return jsonify({'success': True, 'bookmarks': bookmarks})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/marketplace/bookmarks', methods=['POST'])
def toggle_bookmark():
    """Toggle bookmark on a listing"""
    try:
        data = request.json
        result = budget_planner.toggle_bookmark(data.get('listing_id'), data.get('email'))
        return jsonify({'success': True, 'bookmarked': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Syllabus Upload & Parsing
@app.route('/api/syllabus/upload', methods=['POST'])
def upload_syllabus():
    """Upload syllabus for auto-extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'syllabi', filename)
        file.save(filepath)
        
        # Parse syllabus (mocked)
        extracted = budget_planner.parse_syllabus(filepath)
        
        return jsonify({
            'success': True,
            'extracted': extracted
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Price Comparison
@app.route('/api/price/compare', methods=['POST'])
def compare_prices():
    """Compare prices across platforms"""
    try:
        data = request.json
        comparison = budget_planner.compare_prices(
            title=data.get('title', ''),
            isbn=data.get('isbn', ''),
            author=data.get('author', '')
        )
        return jsonify({'success': True, 'comparison': comparison})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# AI Price Suggestion
@app.route('/api/price/suggest', methods=['POST'])
def suggest_price():
    """Get AI-suggested price"""
    try:
        data = request.json
        suggestion = budget_planner.suggest_price(data)
        return jsonify({'success': True, 'suggestion': suggestion})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Class Recommendations
@app.route('/api/classes/recommendations', methods=['POST'])
def get_class_recommendations():
    """Get recommended items for a class"""
    try:
        data = request.json
        class_code = data.get('class_code', '')
        recommendations = budget_planner.get_class_recommendations(class_code)
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Messaging
@app.route('/api/messages/conversations', methods=['GET'])
def get_conversations():
    """Get user's conversations"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'success': False, 'error': 'Email required'}), 400
        conversations = budget_planner.get_conversations(email)
        return jsonify(conversations)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/messages/conversation/<conversation_id>', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Get messages in a conversation"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        messages = budget_planner.get_conversation_messages(conversation_id, email)
        if isinstance(messages, dict) and 'error' in messages:
            return jsonify(messages), messages.get('status', 500)
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/messages', methods=['POST'])
def send_message():
    """Send a message with content moderation"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        data = request.json
        message = budget_planner.send_message(data)
        if isinstance(message, dict) and 'error' in message:
            return jsonify(message), message.get('status', 400)
        return jsonify(message)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/messages/<message_id>/react', methods=['POST'])
def react_to_message(message_id):
    """Add reaction to a message"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        data = request.json
        result = budget_planner.react_to_message(message_id, email, data.get('reaction'))
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/messages/<message_id>/report', methods=['POST'])
def report_message(message_id):
    """Report a message for moderation"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        data = request.json
        result = budget_planner.report_message(message_id, email, data.get('reason'))
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/users/block', methods=['POST'])
def block_user():
    """Block a user"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        data = request.json
        result = budget_planner.block_user(email, data.get('blocked_email'))
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/messages/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        result = budget_planner.delete_conversation(email, conversation_id)
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/api/users/blocked', methods=['GET'])
def get_blocked_users():
    """Get list of blocked users"""
    try:
        email = request.headers.get('X-User-Email', '')
        if not email:
            return jsonify({'error': 'Email required', 'status': 400}), 400
        blocked = budget_planner.get_blocked_users(email)
        return jsonify(blocked)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500


# Budget Estimator
@app.route('/api/budget/estimate', methods=['POST'])
def estimate_budget():
    """Estimate semester budget"""
    try:
        data = request.json
        estimate = budget_planner.estimate_semester_budget(data)
        return jsonify({'success': True, 'estimate': estimate})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Lehigh Student Academic Marketplace")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:5000")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
