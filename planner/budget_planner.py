"""
Lehigh Student Academic Marketplace
Comprehensive marketplace with smart features
"""

import json
import os
import re
from datetime import datetime, timedelta


class BudgetPlanner:
    """Manages Lehigh marketplace and academic planning"""
    
    # Lehigh-specific categories
    CATEGORIES = {
        'textbooks': {
            'name': 'Textbooks',
            'subcategories': ['New', 'Used', 'Rentals', 'PDFs/Links', 'Previous Editions', 'Instructor Notes']
        },
        'supplies': {
            'name': 'School Supplies',
            'subcategories': ['Calculators', 'Lab Goggles', 'Clickers', 'Notebooks', 'Binders', 'Index Cards']
        },
        'electronics': {
            'name': 'Academic Electronics',
            'subcategories': ['Laptops', 'Tablets', 'Headphones', 'Chargers', 'Keyboards', 'USB Drives']
        },
        'class-required': {
            'name': 'Class-Required Items',
            'subcategories': ['Lab Coats', 'Scrubs', 'Equipment Kits', 'Studio Art Supplies']
        },
        'dorm': {
            'name': 'Dorm & Student Life',
            'subcategories': ['Microwaves', 'Mini-Fridges', 'Fans', 'Lamps', 'Desks', 'Bike Locks']
        }
    }
    
    # Common Lehigh classes with textbook mappings
    LEHIGH_CLASSES = {
        'EECS 183': {
            'name': 'Introduction to Computer Science',
            'textbooks': ['Starting Out with Python', 'Python Programming: An Introduction to Computer Science'],
            'supplies': ['Calculator', 'USB Drive'],
            'electronics': []
        },
        'BIO 120': {
            'name': 'General Biology',
            'textbooks': ['Campbell Biology', 'Biology: The Unity and Diversity of Life'],
            'supplies': ['Lab Goggles', 'Lab Coat', 'Clicker'],
            'electronics': []
        },
        'CHEM 101': {
            'name': 'General Chemistry',
            'textbooks': ['Chemistry: The Central Science', 'General Chemistry: Principles and Modern Applications'],
            'supplies': ['Lab Goggles', 'Lab Coat', 'Calculator'],
            'electronics': []
        },
        'MATH 021': {
            'name': 'Calculus I',
            'textbooks': ['Calculus: Early Transcendentals', 'Thomas\' Calculus'],
            'supplies': ['Calculator', 'Notebooks'],
            'electronics': []
        }
    }
    
    def __init__(self):
        self.data_dir = 'data'
        self.listings_file = os.path.join(self.data_dir, 'listings.json')
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.bookmarks_file = os.path.join(self.data_dir, 'bookmarks.json')
        self.messages_file = os.path.join(self.data_dir, 'messages.json')
        self.classes_file = os.path.join(self.data_dir, 'classes.json')
        self.conversations_file = os.path.join(self.data_dir, 'conversations.json')
        self.blocks_file = os.path.join(self.data_dir, 'blocks.json')
        self.reports_file = os.path.join(self.data_dir, 'reports.json')
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize data files"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        for file_path in [self.listings_file, self.users_file, self.bookmarks_file, 
                         self.messages_file, self.classes_file, self.conversations_file,
                         self.blocks_file, self.reports_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
        
        # Populate with sample listings if empty
        if os.path.exists(self.listings_file):
            try:
                with open(self.listings_file, 'r') as f:
                    existing = json.load(f)
                    if len(existing) == 0:
                        self._populate_sample_listings()
            except:
                self._populate_sample_listings()
    
    # User Management
    def get_or_create_user(self, email, nickname=None):
        """Get or create a user"""
        users = self._load_json(self.users_file)
        user = next((u for u in users if u['email'] == email), None)
        
        if not user:
            user = {
                'email': email,
                'nickname': nickname or email.split('@')[0],
                'created_at': datetime.now().isoformat(),
                'classes': [],
                'major': ''
            }
            users.append(user)
        else:
            # Update nickname if provided
            if nickname and nickname != user.get('nickname'):
                user['nickname'] = nickname
                user['updated_at'] = datetime.now().isoformat()
        
        self._save_json(self.users_file, users)
        return user
    
    def validate_nickname(self, nickname):
        """Validate nickname appropriateness"""
        if not nickname or len(nickname.strip()) < 2:
            return {'valid': False, 'error': 'Nickname must be at least 2 characters long'}
        
        if len(nickname) > 30:
            return {'valid': False, 'error': 'Nickname must be 30 characters or less'}
        
        # Comprehensive list of offensive words
        inappropriate_words = [
            # Swear words
            'arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'ass hole',
            'bastard', 'bitch', 'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit',
            'child-fucker', 'cock', 'cocksucker', 'crap', 'cunt',
            'dammit', 'damn', 'damned', 'damn it', 'dick', 'dick-head', 'dickhead', 'dumb ass', 'dumb-ass', 'dumbass', 'dyke',
            'fag', 'faggot', 'father-fucker', 'fatherfucker', 'fuck', 'fucked', 'fucker', 'fucking',
            'god dammit', 'goddammit', 'god damn', 'goddamn', 'goddamned', 'goddamnit', 'godsdamn',
            'hell', 'holy shit', 'horseshit',
            'jackarse', 'jack-ass', 'jackass', 'jesus christ', 'jesus fuck', 'jesus harold christ', 'jesus h. christ', 'jesus wept',
            'kike',
            'mental',
            'mother fucker', 'mother-fucker', 'motherfucker',
            'nigger', 'nigga', 'nigra',  # n-word and variants
            'pigfucker', 'piss', 'prick', 'pussy',
            'shit', 'shit ass', 'shite', 'sibling fucker', 'sisterfuck', 'sisterfucker', 'slut', 'son of a bitch', 'son of a whore', 'spastic', 'sweet jesus',
            'tranny', 'twat',
            'wanker',
            # Additional offensive terms
            'admin', 'administrator', 'moderator', 'mod', 'root',
            'nazi', 'hitler', 'kill', 'death', 'murder', 'hate'
        ]
        
        nickname_lower = nickname.lower()
        # Create a version with numbers removed to catch leetspeak variants
        nickname_stripped = re.sub(r'[0-9]', '', nickname_lower)
        
        # Check for inappropriate words
        for word in inappropriate_words:
            # Check if word appears in nickname directly
            if word in nickname_lower:
                return {'valid': False, 'error': 'Nickname contains inappropriate content'}
            # Also check with numbers stripped (catches n1gger, n1gga, etc.)
            if word in nickname_stripped:
                return {'valid': False, 'error': 'Nickname contains inappropriate content'}
        
        # Additional check for common leetspeak variants of offensive words
        # Replace numbers with letters that sound similar and check again
        leetspeak_replacements = [
            (r'[1!]', 'i'),
            (r'[3]', 'e'),
            (r'[4]', 'a'),
            (r'[5]', 's'),
            (r'[7]', 't'),
            (r'[0]', 'o'),
        ]
        
        nickname_leetspeak = nickname_lower
        for pattern, replacement in leetspeak_replacements:
            nickname_leetspeak = re.sub(pattern, replacement, nickname_leetspeak)
        
        for word in inappropriate_words:
            if word in nickname_leetspeak:
                return {'valid': False, 'error': 'Nickname contains inappropriate content'}
        
        # Check pattern
        if not re.match(r'^[A-Za-z0-9\s\.\-_]+$', nickname):
            return {'valid': False, 'error': 'Nickname can only contain letters, numbers, spaces, dots, dashes, and underscores'}
        
        return {'valid': True}
    
    def validate_captcha(self, challenge, correct_indices, answer):
        """Validate CAPTCHA answer against correct indices (server-side validation)"""
        # Strict validation - answer must match correct indices exactly
        try:
            if not answer or not challenge:
                return False
            
            if not correct_indices:
                return False
            
            # Convert answer from comma-separated string to list of ints
            answer_str = str(answer).strip()
            if not answer_str:
                return False
            
            # Parse indices from answer
            user_indices = []
            for idx_str in answer_str.split(','):
                idx_str = idx_str.strip()
                if idx_str.isdigit():
                    user_indices.append(int(idx_str))
            
            if not user_indices:
                return False
            
            # Sort both for comparison
            user_indices_sorted = sorted(user_indices)
            correct_indices_sorted = sorted([int(x) for x in correct_indices])
            
            # Must match exactly
            return user_indices_sorted == correct_indices_sorted
        except:
            return False
    
    # Marketplace Listings
    def get_marketplace_listings(self, category='', class_code='', search='', 
                                 min_price='', max_price='', condition='', page='explore'):
        """Get marketplace listings with filters"""
        listings = self._load_json(self.listings_file)
        
        # Filter by status
        if page == 'my-listings':
            # Filter by user email would go here
            pass
        elif page == 'saved':
            # Filter by bookmarks would go here
            pass
        else:
            listings = [l for l in listings if l.get('status') == 'active']
        
        # Apply filters
        if category:
            listings = [l for l in listings if l.get('category') == category]
        
        if class_code:
            listings = [l for l in listings if class_code.upper() in l.get('class_tags', [])]
        
        if search:
            search_lower = search.lower()
            listings = [l for l in listings if 
                       search_lower in l.get('title', '').lower() or 
                       search_lower in l.get('description', '').lower()]
        
        if min_price:
            try:
                min_p = float(min_price)
                listings = [l for l in listings if float(l.get('price', 0)) >= min_p]
            except:
                pass
        
        if max_price:
            try:
                max_p = float(max_price)
                listings = [l for l in listings if float(l.get('price', 0)) <= max_p]
            except:
                pass
        
        if condition:
            listings = [l for l in listings if l.get('condition') == condition]
        
        # Sort by date (newest first)
        listings.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return listings
    
    def create_marketplace_listing(self, data):
        """Create a new marketplace listing"""
        listings = self._load_json(self.listings_file)
        
        new_listing = {
            'id': f"listing_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'price': float(data.get('price', 0)),
            'condition': data.get('condition', 'Good'),
            'category': data.get('category', 'textbooks'),
            'subcategory': data.get('subcategory', ''),
            'class_tags': data.get('class_tags', []),
            'seller_email': data.get('seller_email', ''),
            'seller_name': data.get('seller_name', ''),
            'contact': data.get('contact', ''),
            'image_url': data.get('image_url', ''),
            'isbn': data.get('isbn', ''),
            'edition': data.get('edition', ''),
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'views': 0,
            'bookmarks': 0
        }
        
        listings.append(new_listing)
        self._save_json(self.listings_file, listings)
        
        return new_listing
    
    def get_listing(self, listing_id):
        """Get a single listing"""
        listings = self._load_json(self.listings_file)
        return next((l for l in listings if l['id'] == listing_id), None)
    
    def update_listing(self, listing_id, data):
        """Update a listing"""
        listings = self._load_json(self.listings_file)
        for i, listing in enumerate(listings):
            if listing['id'] == listing_id:
                listings[i].update(data)
                listings[i]['updated_at'] = datetime.now().isoformat()
                break
        self._save_json(self.listings_file, listings)
        return next((l for l in listings if l['id'] == listing_id), None)
    
    def delete_listing(self, listing_id):
        """Delete a listing"""
        listings = self._load_json(self.listings_file)
        listings = [l for l in listings if l['id'] != listing_id]
        self._save_json(self.listings_file, listings)
    
    def mark_listing_sold(self, listing_id):
        """Mark a listing as sold"""
        listings = self._load_json(self.listings_file)
        for listing in listings:
            if listing['id'] == listing_id:
                listing['status'] = 'sold'
                listing['sold_at'] = datetime.now().isoformat()
                break
        self._save_json(self.listings_file, listings)
    
    # Bookmarks
    def get_bookmarks(self, email):
        """Get user's bookmarked listings"""
        bookmarks = self._load_json(self.bookmarks_file)
        user_bookmarks = [b for b in bookmarks if b.get('email') == email]
        listing_ids = [b['listing_id'] for b in user_bookmarks]
        
        listings = self._load_json(self.listings_file)
        return [l for l in listings if l['id'] in listing_ids]
    
    def toggle_bookmark(self, listing_id, email):
        """Toggle bookmark on a listing"""
        bookmarks = self._load_json(self.bookmarks_file)
        
        # Check if already bookmarked
        existing = next((b for b in bookmarks if b.get('listing_id') == listing_id and b.get('email') == email), None)
        
        if existing:
            bookmarks = [b for b in bookmarks if not (b.get('listing_id') == listing_id and b.get('email') == email)]
            bookmarked = False
        else:
            bookmarks.append({
                'listing_id': listing_id,
                'email': email,
                'created_at': datetime.now().isoformat()
            })
            bookmarked = True
        
        self._save_json(self.bookmarks_file, bookmarks)
        
        # Update listing bookmark count
        listings = self._load_json(self.listings_file)
        for listing in listings:
            if listing['id'] == listing_id:
                listing['bookmarks'] = len([b for b in bookmarks if b.get('listing_id') == listing_id])
                break
        self._save_json(self.listings_file, listings)
        
        return bookmarked
    
    # Syllabus Parsing (Mocked)
    def parse_syllabus(self, filepath):
        """Parse syllabus to extract required materials"""
        # Mock extraction - in real app would use OCR/NLP
        extracted = {
            'class_code': 'EECS 183',
            'class_name': 'Introduction to Computer Science',
            'textbooks': [
                {'title': 'Starting Out with Python', 'isbn': '9780135929032', 'required': True},
                {'title': 'Python Programming: An Introduction to Computer Science', 'isbn': '9781590282755', 'required': False}
            ],
            'supplies': ['Calculator', 'USB Drive'],
            'instructor_notes': 'Previous editions acceptable'
        }
        return extracted
    
    # Price Comparison (Mocked)
    def compare_prices(self, title='', isbn='', author=''):
        """Compare prices across platforms"""
        base_price = 120.00  # Mock base price
        
        comparison = {
            'title': title or 'Textbook',
            'isbn': isbn,
            'sources': [
                {
                    'platform': 'Amazon Used',
                    'price': round(base_price * 0.6, 2),
                    'condition': 'Good',
                    'link': '#',
                    'availability': 'In Stock'
                },
                {
                    'platform': 'Chegg Rental',
                    'price': round(base_price * 0.3, 2),
                    'condition': 'New',
                    'link': '#',
                    'availability': 'Available',
                    'duration': 'Semester'
                },
                {
                    'platform': 'ThriftBooks',
                    'price': round(base_price * 0.5, 2),
                    'condition': 'Very Good',
                    'link': '#',
                    'availability': 'In Stock'
                },
                {
                    'platform': 'Lehigh Marketplace',
                    'price': round(base_price * 0.55, 2),
                    'condition': 'Like New',
                    'link': '#',
                    'availability': '3 listings available'
                }
            ],
            'best_deal': {
                'platform': 'Chegg Rental',
                'price': round(base_price * 0.3, 2),
                'savings': round(base_price * 0.7, 2)
            }
        }
        
        return comparison
    
    # AI Price Suggestion (Mocked)
    def suggest_price(self, data):
        """Suggest fair price based on condition, edition, demand"""
        base_price = float(data.get('retail_price', 100))
        condition = data.get('condition', 'Good')
        edition = data.get('edition', 'current')
        class_code = data.get('class_code', '')
        
        # Condition multipliers
        condition_mult = {
            'New': 0.9,
            'Like New': 0.75,
            'Good': 0.6,
            'Fair': 0.4
        }
        
        # Edition multipliers
        edition_mult = {
            'current': 1.0,
            'previous': 0.7,
            'older': 0.5
        }
        
        # Demand multiplier (based on class popularity)
        demand_mult = 1.0
        if class_code in self.LEHIGH_CLASSES:
            demand_mult = 1.1  # Popular class = higher demand
        
        suggested = base_price * condition_mult.get(condition, 0.6) * edition_mult.get(edition, 1.0) * demand_mult
        
        suggestion = {
            'suggested_price': round(suggested, 2),
            'price_range': {
                'min': round(suggested * 0.9, 2),
                'max': round(suggested * 1.1, 2)
            },
            'reasoning': f"Based on {condition} condition, {edition} edition, and class demand",
            'market_average': round(suggested * 0.95, 2)
        }
        
        return suggestion
    
    # Class Recommendations
    def get_class_recommendations(self, class_code):
        """Get recommended items for a class"""
        class_code = class_code.upper()
        class_info = self.LEHIGH_CLASSES.get(class_code, {})
        
        if not class_info:
            return {
                'class_code': class_code,
                'recommendations': []
            }
        
        recommendations = {
            'class_code': class_code,
            'class_name': class_info.get('name', ''),
            'textbooks': [],
            'supplies': [],
            'electronics': []
        }
        
        # Get marketplace listings for recommended items
        listings = self._load_json(self.listings_file)
        active_listings = [l for l in listings if l.get('status') == 'active']
        
        for textbook in class_info.get('textbooks', []):
            # Find listings for this textbook
            matching = [l for l in active_listings if textbook.lower() in l.get('title', '').lower()]
            avg_price = sum([l['price'] for l in matching]) / len(matching) if matching else 0
            
            recommendations['textbooks'].append({
                'title': textbook,
                'required': True,
                'average_price': round(avg_price, 2),
                'listings_available': len(matching)
            })
        
        for supply in class_info.get('supplies', []):
            recommendations['supplies'].append({
                'name': supply,
                'required': True
            })
        
        return recommendations
    
    # Messaging
    def get_messages(self, email):
        """Get user's messages"""
        messages = self._load_json(self.messages_file)
        return [m for m in messages if m.get('to_email') == email or m.get('from_email') == email]
    
    def send_message(self, data):
        """Send a message with moderation and conversation management"""
        sender_email = data.get('sender_email', '')
        recipient_email = data.get('recipient_email', '')
        listing_id = data.get('listing_id', '')
        content = data.get('content', '')
        reply_to = data.get('reply_to')
        
        # Prevent self-messaging
        if sender_email == recipient_email:
            return {'error': 'You cannot send messages to yourself', 'status': 400}
        
        # Check if sender is blocked
        if self._is_blocked(sender_email, recipient_email):
            return {'error': 'You have been blocked by this user', 'status': 403}
        
        # Content moderation
        moderation_result = self._moderate_content(content)
        if not moderation_result['allowed']:
            return {'error': f'Message blocked: {moderation_result["reason"]}', 'status': 400}
        
        # Get or create conversation
        conversation = self._get_or_create_conversation(sender_email, recipient_email, listing_id)
        
        # Create message
        messages = self._load_json(self.messages_file)
        timestamp = datetime.now().isoformat()
        
        new_message = {
            'id': f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'conversation_id': conversation['id'],
            'sender_email': sender_email,
            'content': content,
            'timestamp': timestamp,
            'reactions': [],
            'reply_to': reply_to,
            'read': False
        }
        
        messages.append(new_message)
        self._save_json(self.messages_file, messages)
        
        # Update conversation last_message
        conversations = self._load_json(self.conversations_file)
        for conv in conversations:
            if conv['id'] == conversation['id']:
                conv['last_message'] = content[:50]
                conv['last_message_time'] = timestamp
                break
        self._save_json(self.conversations_file, conversations)
        
        return new_message
    
    def get_conversations(self, email):
        """Get all conversations for a user"""
        conversations = self._load_json(self.conversations_file)
        messages = self._load_json(self.messages_file)
        users = self._load_json(self.users_file)
        listings = self._load_json(self.listings_file)
        
        user_conversations = []
        for conv in conversations:
            if email in conv['participants']:
                # Get other participant (skip if same user twice - edge case)
                other_participants = [p for p in conv['participants'] if p != email]
                if not other_participants:
                    # Skip conversations where user is talking to themselves
                    continue
                other_email = other_participants[0]
                
                # Try to get user from users table first
                other_user = next((u for u in users if u['email'] == other_email), None)
                
                # Get listing info (need it to potentially get seller name)
                listing = None
                if conv.get('listing_id'):
                    listing = next((l for l in listings if l['id'] == conv['listing_id']), None)
                
                # Determine nickname - prefer user table, fallback to listing seller name
                other_nickname = 'Unknown'
                if other_user:
                    other_nickname = other_user.get('nickname', 'Unknown')
                elif listing and listing.get('contact') == other_email:
                    # User not in users table, but they're the seller in the listing
                    other_nickname = listing.get('seller_name', 'Unknown')
                
                # Count unread messages
                unread = len([m for m in messages if m['conversation_id'] == conv['id'] 
                             and m['sender_email'] != email and not m.get('read', False)])
                
                listing_data = None
                if listing:
                    # Get first image from image_urls array or legacy image_url
                    image_url = ''
                    if listing.get('image_urls') and len(listing['image_urls']) > 0:
                        image_url = listing['image_urls'][0]
                    elif listing.get('image_url'):
                        image_url = listing['image_url']
                    
                    listing_data = {
                        'id': listing['id'],
                        'title': listing['title'],
                        'image_url': image_url
                    }
                
                user_conversations.append({
                    'id': conv['id'],
                    'other_user': {
                        'email': other_email,
                        'nickname': other_nickname
                    },
                    'listing': listing_data,
                    'last_message': conv.get('last_message', ''),
                    'last_message_time': conv.get('last_message_time', conv['created_at']),
                    'unread_count': unread
                })
        
        # Sort by last message time
        user_conversations.sort(key=lambda x: x['last_message_time'], reverse=True)
        return user_conversations
    
    def get_conversation_messages(self, conversation_id, email):
        """Get all messages in a conversation"""
        conversations = self._load_json(self.conversations_file)
        conversation = next((c for c in conversations if c['id'] == conversation_id), None)
        
        if not conversation:
            return {'error': 'Conversation not found', 'status': 404}
        
        # Verify user is participant
        if email not in conversation['participants']:
            return {'error': 'Unauthorized', 'status': 403}
        
        # Get messages
        messages = self._load_json(self.messages_file)
        conv_messages = [m for m in messages if m['conversation_id'] == conversation_id]
        conv_messages.sort(key=lambda x: x['timestamp'])
        
        # Mark messages as read
        for msg in conv_messages:
            if msg['sender_email'] != email and not msg.get('read', False):
                msg['read'] = True
        self._save_json(self.messages_file, messages)
        
        return conv_messages
    
    def react_to_message(self, message_id, email, reaction):
        """Add or remove a reaction to a message"""
        messages = self._load_json(self.messages_file)
        message = next((m for m in messages if m['id'] == message_id), None)
        
        if not message:
            return {'error': 'Message not found', 'status': 404}
        
        # Verify user is in conversation
        conversations = self._load_json(self.conversations_file)
        conversation = next((c for c in conversations if c['id'] == message['conversation_id']), None)
        if not conversation or email not in conversation['participants']:
            return {'error': 'Unauthorized', 'status': 403}
        
        # Toggle reaction
        reactions = message.get('reactions', [])
        existing = next((r for r in reactions if r['user'] == email), None)
        
        if existing:
            if existing['type'] == reaction:
                # Remove reaction
                reactions = [r for r in reactions if r['user'] != email]
            else:
                # Update reaction
                existing['type'] = reaction
        else:
            # Add new reaction
            reactions.append({'user': email, 'type': reaction})
        
        message['reactions'] = reactions
        self._save_json(self.messages_file, messages)
        
        return {'success': True, 'reactions': reactions}
    
    def report_message(self, message_id, reporter_email, reason):
        """Report a message for moderation"""
        messages = self._load_json(self.messages_file)
        message = next((m for m in messages if m['id'] == message_id), None)
        
        if not message:
            return {'error': 'Message not found', 'status': 404}
        
        # Create report
        reports = self._load_json(self.reports_file)
        new_report = {
            'id': f"report_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'message_id': message_id,
            'reporter_email': reporter_email,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        reports.append(new_report)
        self._save_json(self.reports_file, reports)
        
        # Auto-hide message if multiple reports
        message_reports = [r for r in reports if r['message_id'] == message_id]
        if len(message_reports) >= 3:
            message['hidden'] = True
            self._save_json(self.messages_file, messages)
        
        return {'success': True, 'report': new_report}
    
    def block_user(self, blocker_email, blocked_email):
        """Block a user from sending messages"""
        blocks = self._load_json(self.blocks_file)
        
        # Check if already blocked
        existing = next((b for b in blocks if b['blocker'] == blocker_email and b['blocked'] == blocked_email), None)
        if existing:
            return {'success': True, 'message': 'User already blocked'}
        
        new_block = {
            'id': f"block_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'blocker': blocker_email,
            'blocked': blocked_email,
            'timestamp': datetime.now().isoformat()
        }
        
        blocks.append(new_block)
        self._save_json(self.blocks_file, blocks)
        
        return {'success': True, 'block': new_block}
    
    def get_blocked_users(self, email):
        """Get list of users blocked by this user"""
        blocks = self._load_json(self.blocks_file)
        blocked = [b['blocked'] for b in blocks if b['blocker'] == email]
        return blocked
    
    def delete_conversation(self, user_email, conversation_id):
        """Delete a conversation for a user"""
        conversations = self._load_json(self.conversations_file)
        
        # Find conversation
        conv = next((c for c in conversations if c['id'] == conversation_id), None)
        if not conv:
            return {'error': 'Conversation not found', 'status': 404}
        
        # Check if user is participant
        if user_email not in conv['participants']:
            return {'error': 'Unauthorized', 'status': 403}
        
        # Delete all messages in this conversation
        messages = self._load_json(self.messages_file)
        messages = [m for m in messages if m.get('conversation_id') != conversation_id]
        self._save_json(self.messages_file, messages)
        
        # Delete the conversation
        conversations = [c for c in conversations if c['id'] != conversation_id]
        self._save_json(self.conversations_file, conversations)
        
        return {'success': True, 'message': 'Conversation deleted'}
    
    def _get_or_create_conversation(self, email1, email2, listing_id=None):
        """Get existing conversation or create new one"""
        conversations = self._load_json(self.conversations_file)
        
        # Check for existing conversation
        participants = sorted([email1, email2])
        existing = next((c for c in conversations if sorted(c['participants']) == participants 
                        and c.get('listing_id') == listing_id), None)
        
        if existing:
            return existing
        
        # Create new conversation
        new_conversation = {
            'id': f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'participants': participants,
            'listing_id': listing_id,
            'created_at': datetime.now().isoformat(),
            'last_message': '',
            'last_message_time': datetime.now().isoformat()
        }
        
        conversations.append(new_conversation)
        self._save_json(self.conversations_file, conversations)
        
        return new_conversation
    
    def _is_blocked(self, sender_email, recipient_email):
        """Check if sender is blocked by recipient"""
        blocks = self._load_json(self.blocks_file)
        return any(b['blocker'] == recipient_email and b['blocked'] == sender_email for b in blocks)
    
    def _moderate_content(self, content):
        """Check content for inappropriate material"""
        # Profanity filter
        profanity_list = [
            'fuck', 'shit', 'ass', 'bitch', 'damn', 'crap', 'hell',
            'bastard', 'dick', 'pussy', 'cock', 'slut', 'whore'
        ]
        
        content_lower = content.lower()
        for word in profanity_list:
            if word in content_lower:
                return {'allowed': False, 'reason': 'Inappropriate language detected'}
        
        # Spam detection (too many repeated characters or all caps)
        if len(content) > 20:
            if content.isupper():
                return {'allowed': False, 'reason': 'Please do not use all caps'}
            
            # Check for excessive character repetition
            for i in range(len(content) - 5):
                if len(set(content[i:i+6])) == 1:
                    return {'allowed': False, 'reason': 'Spam detected'}
        
        # Detect potential scam patterns
        scam_patterns = [
            r'venmo.*\$\d+',
            r'paypal.*\$\d+',
            r'cash.*app',
            r'send.*money',
            r'bitcoin',
            r'cryptocurrency'
        ]
        
        for pattern in scam_patterns:
            if re.search(pattern, content_lower):
                return {'allowed': False, 'reason': 'Suspicious content detected. Please use safe payment methods.'}
        
        return {'allowed': True, 'reason': ''}
    
    # Budget Estimation
    def estimate_semester_budget(self, data):
        """Estimate semester budget"""
        classes = data.get('classes', [])
        estimated_budget = data.get('estimated_budget', 0)
        
        total_estimated = 0
        breakdown = {
            'textbooks': 0,
            'supplies': 0,
            'electronics': 0,
            'other': 0
        }
        
        for class_code in classes:
            recommendations = self.get_class_recommendations(class_code)
            for textbook in recommendations.get('textbooks', []):
                breakdown['textbooks'] += textbook.get('average_price', 0)
                total_estimated += textbook.get('average_price', 0)
        
        # Add estimated supplies cost
        breakdown['supplies'] = len(classes) * 50  # $50 per class estimate
        total_estimated += breakdown['supplies']
        
        potential_savings = total_estimated * 0.4  # 40% savings with marketplace
        
        return {
            'estimated_total': round(total_estimated, 2),
            'breakdown': breakdown,
            'potential_savings': round(potential_savings, 2),
            'optimized_total': round(total_estimated - potential_savings, 2),
            'budget_remaining': round(estimated_budget - total_estimated, 2) if estimated_budget > 0 else None
        }
    
    def _populate_sample_listings(self):
        """Populate marketplace with sample listings"""
        import random
        
        sample_listings = [
            # Textbooks
            {
                'title': 'Starting Out with Python (5th Edition)',
                'description': 'Used textbook for EECS 183. Good condition, some highlighting in first few chapters. Previous edition but content is the same.',
                'price': 45.00,
                'condition': 'Good',
                'category': 'textbooks',
                'subcategory': 'Used',
                'class_tags': ['EECS 183'],
                'isbn': '9780135929032',
                'edition': 'previous',
                'seller_name': 'Alex M.',
                'seller_email': 'alex.m@lehigh.edu',
                'contact': 'alex.m@lehigh.edu'
            },
            {
                'title': 'Campbell Biology (12th Edition)',
                'description': 'Required for BIO 120. Like new condition, no writing or highlighting. Comes with access code.',
                'price': 120.00,
                'condition': 'Like New',
                'category': 'textbooks',
                'subcategory': 'Used',
                'class_tags': ['BIO 120'],
                'isbn': '9780135188743',
                'edition': 'current',
                'seller_name': 'Sarah K.',
                'seller_email': 'sarah.k@lehigh.edu',
                'contact': 'sarah.k@lehigh.edu'
            },
            {
                'title': 'Chemistry: The Central Science (15th Edition)',
                'description': 'Textbook for CHEM 101. Good condition, minor wear on cover. All pages intact.',
                'price': 85.00,
                'condition': 'Good',
                'category': 'textbooks',
                'subcategory': 'Used',
                'class_tags': ['CHEM 101'],
                'isbn': '9780134414232',
                'edition': 'current',
                'seller_name': 'Mike T.',
                'seller_email': 'mike.t@lehigh.edu',
                'contact': 'mike.t@lehigh.edu'
            },
            {
                'title': 'Calculus: Early Transcendentals (8th Edition)',
                'description': 'MATH 021 textbook. Fair condition, some notes in margins but still very usable.',
                'price': 60.00,
                'condition': 'Fair',
                'category': 'textbooks',
                'subcategory': 'Used',
                'class_tags': ['MATH 021'],
                'isbn': '9781285741550',
                'edition': 'previous',
                'seller_name': 'Jordan L.',
                'seller_email': 'jordan.l@lehigh.edu',
                'contact': 'jordan.l@lehigh.edu'
            },
            {
                'title': 'Python Programming PDF - EECS 183',
                'description': 'Digital PDF version of Python Programming textbook. Instant download, no physical book needed.',
                'price': 25.00,
                'condition': 'New',
                'category': 'textbooks',
                'subcategory': 'PDFs/Links',
                'class_tags': ['EECS 183'],
                'isbn': '',
                'edition': 'current',
                'seller_name': 'Digital Books Co.',
                'seller_email': 'digital@example.com',
                'contact': 'digital@example.com'
            },
            {
                'title': 'Introduction to Algorithms (4th Edition)',
                'description': 'Computer science textbook. Excellent condition, barely used. Perfect for advanced CS courses.',
                'price': 95.00,
                'condition': 'Like New',
                'category': 'textbooks',
                'subcategory': 'Used',
                'class_tags': ['EECS 183'],
                'isbn': '9780262046305',
                'edition': 'current',
                'seller_name': 'Chris R.',
                'seller_email': 'chris.r@lehigh.edu',
                'contact': 'chris.r@lehigh.edu'
            },
            # School Supplies
            {
                'title': 'TI-84 Plus CE Graphing Calculator',
                'description': 'Used calculator for math and science classes. Works perfectly, includes case and charger.',
                'price': 75.00,
                'condition': 'Good',
                'category': 'supplies',
                'subcategory': 'Calculators',
                'class_tags': ['MATH 021', 'CHEM 101'],
                'isbn': '',
                'edition': '',
                'seller_name': 'Emma W.',
                'seller_email': 'emma.w@lehigh.edu',
                'contact': 'emma.w@lehigh.edu'
            },
            {
                'title': 'Lab Safety Goggles - BIO 120',
                'description': 'Brand new lab goggles, never used. Required for biology lab. Still in original packaging.',
                'price': 12.00,
                'condition': 'New',
                'category': 'supplies',
                'subcategory': 'Lab Goggles',
                'class_tags': ['BIO 120', 'CHEM 101'],
                'isbn': '',
                'edition': '',
                'seller_name': 'Ryan B.',
                'seller_email': 'ryan.b@lehigh.edu',
                'contact': 'ryan.b@lehigh.edu'
            },
            {
                'title': 'iClicker 2 Student Remote',
                'description': 'Used iClicker for class participation. Works great, includes battery. Used for one semester.',
                'price': 35.00,
                'condition': 'Good',
                'category': 'supplies',
                'subcategory': 'Clickers',
                'class_tags': ['BIO 120'],
                'isbn': '',
                'edition': '',
                'seller_name': 'Maya P.',
                'seller_email': 'maya.p@lehigh.edu',
                'contact': 'maya.p@lehigh.edu'
            },
            {
                'title': '5-Subject Notebooks (Set of 3)',
                'description': 'College-ruled notebooks, perfect for taking notes. Brand new, never opened.',
                'price': 8.00,
                'condition': 'New',
                'category': 'supplies',
                'subcategory': 'Notebooks',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Sam D.',
                'seller_email': 'sam.d@lehigh.edu',
                'contact': 'sam.d@lehigh.edu'
            },
            {
                'title': '3-Ring Binders (Set of 2)',
                'description': '1.5 inch binders, great for organizing class materials. Like new condition.',
                'price': 10.00,
                'condition': 'Like New',
                'category': 'supplies',
                'subcategory': 'Binders',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Taylor H.',
                'seller_email': 'taylor.h@lehigh.edu',
                'contact': 'taylor.h@lehigh.edu'
            },
            # Academic Electronics
            {
                'title': 'MacBook Air M1 (2020) - 256GB',
                'description': 'Excellent condition MacBook Air. Perfect for students. Includes charger. Battery health 95%.',
                'price': 650.00,
                'condition': 'Like New',
                'category': 'electronics',
                'subcategory': 'Laptops',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'David C.',
                'seller_email': 'david.c@lehigh.edu',
                'contact': 'david.c@lehigh.edu'
            },
            {
                'title': 'iPad Air (4th Gen) with Apple Pencil',
                'description': 'Great for note-taking and studying. Includes Apple Pencil and case. Excellent condition.',
                'price': 450.00,
                'condition': 'Good',
                'category': 'electronics',
                'subcategory': 'Tablets',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Olivia M.',
                'seller_email': 'olivia.m@lehigh.edu',
                'contact': 'olivia.m@lehigh.edu'
            },
            {
                'title': 'Sony WH-1000XM4 Noise Cancelling Headphones',
                'description': 'Premium headphones, perfect for studying in noisy dorms. Excellent condition, includes case and cable.',
                'price': 220.00,
                'condition': 'Like New',
                'category': 'electronics',
                'subcategory': 'Headphones',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Noah S.',
                'seller_email': 'noah.s@lehigh.edu',
                'contact': 'noah.s@lehigh.edu'
            },
            {
                'title': 'USB-C Charger Cable (Set of 2)',
                'description': 'Fast charging cables for MacBook, iPad, iPhone. Brand new, 6ft length.',
                'price': 15.00,
                'condition': 'New',
                'category': 'electronics',
                'subcategory': 'Chargers',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Ava J.',
                'seller_email': 'ava.j@lehigh.edu',
                'contact': 'ava.j@lehigh.edu'
            },
            {
                'title': 'Mechanical Keyboard - RGB Backlit',
                'description': 'Gaming/typing keyboard. Great for coding and writing papers. Used but works perfectly.',
                'price': 55.00,
                'condition': 'Good',
                'category': 'electronics',
                'subcategory': 'Keyboards',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Lucas G.',
                'seller_email': 'lucas.g@lehigh.edu',
                'contact': 'lucas.g@lehigh.edu'
            },
            {
                'title': '128GB USB 3.0 Flash Drive',
                'description': 'Fast USB drive for storing projects and files. Brand new, still sealed.',
                'price': 18.00,
                'condition': 'New',
                'category': 'electronics',
                'subcategory': 'USB Drives',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Sophia F.',
                'seller_email': 'sophia.f@lehigh.edu',
                'contact': 'sophia.f@lehigh.edu'
            },
            # Class-Required Items
            {
                'title': 'Lab Coat - Size Medium',
                'description': 'Required for chemistry and biology labs. Good condition, clean. Size M fits most students.',
                'price': 20.00,
                'condition': 'Good',
                'category': 'class-required',
                'subcategory': 'Lab Coats',
                'class_tags': ['CHEM 101', 'BIO 120'],
                'isbn': '',
                'edition': '',
                'seller_name': 'Isabella N.',
                'seller_email': 'isabella.n@lehigh.edu',
                'contact': 'isabella.n@lehigh.edu'
            },
            {
                'title': 'Medical Scrubs - Navy Blue (Set of 2)',
                'description': 'Nursing/health sciences scrubs. Size small, like new condition. Barely worn.',
                'price': 25.00,
                'condition': 'Like New',
                'category': 'class-required',
                'subcategory': 'Scrubs',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Ethan Z.',
                'seller_email': 'ethan.z@lehigh.edu',
                'contact': 'ethan.z@lehigh.edu'
            },
            {
                'title': 'Engineering Drawing Kit',
                'description': 'Complete engineering drawing kit with compass, protractor, rulers. Required for engineering courses.',
                'price': 35.00,
                'condition': 'Good',
                'category': 'class-required',
                'subcategory': 'Equipment Kits',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Mia Y.',
                'seller_email': 'mia.y@lehigh.edu',
                'contact': 'mia.y@lehigh.edu'
            },
            {
                'title': 'Art Supplies Kit - Studio Art',
                'description': 'Complete art supplies including paints, brushes, canvas. Great for studio art classes.',
                'price': 45.00,
                'condition': 'Good',
                'category': 'class-required',
                'subcategory': 'Studio Art Supplies',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'James X.',
                'seller_email': 'james.x@lehigh.edu',
                'contact': 'james.x@lehigh.edu'
            },
            # Dorm & Student Life
            {
                'title': 'Mini Fridge - 3.2 cu ft',
                'description': 'Perfect for dorm room. Works great, clean inside and out. Includes freezer compartment.',
                'price': 80.00,
                'condition': 'Good',
                'category': 'dorm',
                'subcategory': 'Mini-Fridges',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Charlotte V.',
                'seller_email': 'charlotte.v@lehigh.edu',
                'contact': 'charlotte.v@lehigh.edu'
            },
            {
                'title': 'Microwave - Compact',
                'description': 'Small microwave perfect for dorm. 700W, works perfectly. Clean and ready to use.',
                'price': 40.00,
                'condition': 'Good',
                'category': 'dorm',
                'subcategory': 'Microwaves',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Benjamin U.',
                'seller_email': 'benjamin.u@lehigh.edu',
                'contact': 'benjamin.u@lehigh.edu'
            },
            {
                'title': 'Desk Lamp with USB Port',
                'description': 'LED desk lamp with USB charging port. Perfect for studying. Like new condition.',
                'price': 22.00,
                'condition': 'Like New',
                'category': 'dorm',
                'subcategory': 'Lamps',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Amelia T.',
                'seller_email': 'amelia.t@lehigh.edu',
                'contact': 'amelia.t@lehigh.edu'
            },
            {
                'title': 'Tower Fan - 3 Speed',
                'description': 'Oscillating tower fan. Great for hot dorm rooms. Works perfectly, clean.',
                'price': 30.00,
                'condition': 'Good',
                'category': 'dorm',
                'subcategory': 'Fans',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Henry S.',
                'seller_email': 'henry.s@lehigh.edu',
                'contact': 'henry.s@lehigh.edu'
            },
            {
                'title': 'U-Lock Bike Lock',
                'description': 'Heavy duty bike lock. Perfect for campus. Key included, excellent condition.',
                'price': 25.00,
                'condition': 'Good',
                'category': 'dorm',
                'subcategory': 'Bike Locks',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Harper R.',
                'seller_email': 'harper.r@lehigh.edu',
                'contact': 'harper.r@lehigh.edu'
            },
            {
                'title': 'Study Desk with Drawer',
                'description': 'Compact desk perfect for small dorm rooms. Good condition, some minor scratches.',
                'price': 50.00,
                'condition': 'Fair',
                'category': 'dorm',
                'subcategory': 'Desks',
                'class_tags': [],
                'isbn': '',
                'edition': '',
                'seller_name': 'Alexander Q.',
                'seller_email': 'alexander.q@lehigh.edu',
                'contact': 'alexander.q@lehigh.edu'
            }
        ]
        
        listings = []
        base_time = datetime.now()
        
        for i, listing_data in enumerate(sample_listings):
            listing = {
                'id': f"listing_{base_time.strftime('%Y%m%d')}_{str(i+1).zfill(3)}",
                'title': listing_data['title'],
                'description': listing_data['description'],
                'price': listing_data['price'],
                'condition': listing_data['condition'],
                'category': listing_data['category'],
                'subcategory': listing_data.get('subcategory', ''),
                'class_tags': listing_data.get('class_tags', []),
                'seller_email': listing_data['seller_email'],
                'seller_name': listing_data['seller_name'],
                'contact': listing_data['contact'],
                'image_url': self._generate_placeholder_image(listing_data),
                'isbn': listing_data.get('isbn', ''),
                'edition': listing_data.get('edition', ''),
                'created_at': (base_time - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).isoformat(),
                'status': 'active',
                'views': random.randint(5, 150),
                'bookmarks': random.randint(0, 10)
            }
            listings.append(listing)
        
        self._save_json(self.listings_file, listings)
    
    # Helper methods
    def _load_json(self, filepath):
        """Load JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _generate_placeholder_image(self, listing_data):
        """Generate placeholder image URL based on category"""
        category = listing_data.get('category', 'textbooks')
        title = listing_data.get('title', 'Item')
        
        # Use placeholder.com service with category-specific colors
        category_colors = {
            'textbooks': '4A90E2',  # Blue
            'supplies': '50C878',   # Green
            'electronics': 'FF6B6B', # Red
            'class-required': 'FFA500', # Orange
            'dorm': '9B59B6'        # Purple
        }
        
        color = category_colors.get(category, 'CCCCCC')
        # Create a placeholder image URL
        # Using placeholder.com service
        text = title[:20].replace(' ', '%20')  # URL encode first 20 chars
        return f"https://via.placeholder.com/400x300/{color}/FFFFFF?text={text}"
    
    def _save_json(self, filepath, data):
        """Save JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
