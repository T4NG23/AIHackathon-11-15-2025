# DormDealz

**DormDealz: Study Hard. Spend Smart.**

A Facebook Marketplace-style platform designed exclusively for Lehigh University students. Buy and sell textbooks, electronics, dorm essentials, and class-required items directly with fellow Mountain Hawks in a secure, monitored environment.

## Overview

DormDealz is a comprehensive student-to-student marketplace that makes it easy to find affordable textbooks, supplies, and dorm items while connecting with the Lehigh community. With features like secure in-app messaging, content moderation, smart filtering, and Lehigh-branded design, students can safely buy and sell everything they need for college life.

## Key Features

### Marketplace
- **Browse & Search** - Clean, Facebook Marketplace-inspired interface with grid view
- **Smart Filters** - Dynamic filtering by category, condition, price range, and search keywords (auto-applies as you type)
- **Collapsible Sidebar** - Organized categories and filters that collapse to save space
- **Detailed Listings** - Multi-image galleries with thumbnail navigation, condition tags, and seller information
- **Save Items** - Bookmark your favorite listings for later
- **My Listings** - Manage all your active listings in one place

### Secure Messaging System
- **In-App Chat** - Private, secure messaging between buyers and sellers
- **Real-Time Communication** - Send and receive messages instantly
- **Message Reactions** - React to messages with emojis (👍❤️😂😮😢)
- **Threaded Replies** - Reply to specific messages for better context
- **Content Moderation** - AI-powered monitoring for inappropriate behavior
- **User Safety** - Block and report users with confirmation dialogs
- **Conversation Management** - Delete conversations, view message history
- **Three-Dot Menus** - Quick access to block, report, and delete actions

### Categories
- **Textbooks** - New, used, rentals, PDFs, previous editions
- **School Supplies** - Calculators, lab equipment, notebooks, clickers
- **Electronics** - Laptops, tablets, headphones, chargers, USB drives
- **Class Items** - Lab coats, art supplies, equipment kits
- **Dorm & Living** - Mini-fridges, microwaves, fans, lamps, furniture, bikes

### Design & UX
- **Lehigh Branding** - Brown (#653819) and gold (#FFD700) color scheme
- **DormDealz Logo** - Custom logo with dynamic sizing (shrinks on scroll)
- **Responsive Layout** - Works seamlessly on desktop and mobile
- **Sticky Navigation** - Easy access to all pages with active state indicators
- **Smooth Transitions** - Polished animations and hover effects

### Safety & Moderation
- **Content Monitoring** - Automated detection of inappropriate messages
- **Block Users** - Prevent unwanted users from contacting you
- **Report System** - Flag problematic users or content with detailed reasons
- **Owner Controls** - Delete your own listings anytime
- **Secure Login** - Simple email-based authentication

## Functionalities

### For Buyers
1. **Explore Listings** - Browse all available items on the main marketplace page
2. **Filter & Search** - Use dynamic filters and search to find exactly what you need
3. **View Details** - Click any listing to see full description, images, and seller info
4. **Message Sellers** - Contact sellers directly through secure in-app messaging
5. **Save Favorites** - Bookmark items to review later
6. **Manage Messages** - View all conversations, delete unwanted chats, block/report users

### For Sellers
1. **Create Listings** - Click "Sell" to post items with title, description, price, images, and category
2. **Upload Images** - Add multiple photos to showcase your items
3. **Set Condition** - Tag items as New, Like New, Good, or Fair
4. **Manage Listings** - View and delete your own listings from "My Listings" or the detail page
5. **Respond to Buyers** - Answer questions and coordinate sales via messaging
6. **Mark as Sold** - Update listings when items sell

### Messaging Features
- **Start Conversations** - Click "Contact Seller" on any listing
- **Send Messages** - Type and send messages in real-time
- **React & Reply** - Add reactions or reply to specific messages
- **Three-Dot Menus**:
  - **Conversation List**: Delete conversation, block user, report user
  - **Chat Header**: Block user, report user
- **View History** - Access all past conversations from the Messages page

### Admin/Moderation
- **Automated Monitoring** - System flags messages with inappropriate content
- **User Reports** - Receive and review user-submitted reports
- **Content Flags** - Track violations and take action on problematic accounts

## Tech Stack

**Backend:**
- Flask (Python web framework)
- BudgetPlanner class for data management
- JSON file-based storage (listings, users, messages, conversations, bookmarks, reports)
- RESTful API endpoints for CRUD operations

**Frontend:**
- Jinja2 templating engine
- Vanilla JavaScript (no frameworks)
- HTML5 semantic markup
- CSS3 with custom properties

**Styling:**
- Custom CSS with Lehigh colors
- Facebook Marketplace-inspired layout
- Responsive design patterns
- Smooth transitions and animations

**Storage:**
- `data/listings.json` - All marketplace listings
- `data/users.json` - User accounts and profiles
- `data/messages.json` - Chat messages
- `data/conversations.json` - Conversation metadata
- `data/bookmarks.json` - Saved listings
- `data/reports.json` - User reports
- `data/blocks.json` - Blocked user relationships

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/T4NG23/AIHackathon-11-15-2025.git
   cd AIHackathon-11-15-2025
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage Guide

### Getting Started

1. **Login** - Click "Login" in the navbar and enter your email
2. **Browse** - Explore listings on the main marketplace page
3. **Filter** - Use the sidebar to filter by category, condition, price, or search keywords
4. **View Listing** - Click any item to see full details and image gallery

### Buying Items

1. Navigate to any listing that interests you
2. View all images using the thumbnail gallery
3. Check condition, price, and description
4. Click "Contact Seller" to start a conversation
5. Send a message to ask questions or arrange pickup
6. Click the bookmark icon to save for later

### Selling Items

1. Click "Sell" in the navigation bar
2. Fill in the listing form:
   - **Title** - Clear, descriptive name
   - **Description** - Detailed information about the item
   - **Price** - Set your asking price
   - **Category** - Choose the appropriate category
   - **Condition** - Select New, Like New, Good, or Fair
   - **Images** - Upload multiple photos (optional)
3. Add your contact email
4. Click "Create Listing"
5. View your listing in "My Listings"
6. Delete anytime by clicking the delete button on your listing

### Messaging

1. **Start a Chat** - Click "Contact Seller" on any listing
2. **Send Messages** - Type in the message box and press Enter or click Send
3. **React to Messages** - Hover over any message and click a reaction emoji
4. **Reply to Messages** - Click the reply icon to quote a specific message
5. **Manage Conversations**:
   - Click three dots (⋮) next to a conversation to delete, block, or report
   - Click three dots in chat header to block or report the user
6. **View All Messages** - Navigate to "Messages" page to see all conversations

### Safety Features

- **Block Users** - Prevents them from messaging you (accessible via three-dot menu)
- **Report Users** - Submit a report with a reason (harassment, spam, scam, inappropriate, other)
- **Delete Conversations** - Remove unwanted chats from your message list
- **Content Moderation** - System monitors messages for inappropriate content

## Project Structure

```
/
├── app.py                          # Main Flask application & API routes
├── README.md                       # Documentation (this file)
├── requirements.txt                # Python dependencies
│
├── planner/                        # Backend Logic
│   ├── __init__.py
│   └── budget_planner.py          # Core marketplace & messaging logic
│
├── templates/                      # HTML Templates (Jinja2)
│   ├── base.html                  # Base template with navbar & footer
│   ├── index.html                 # Homepage (redirects to marketplace)
│   ├── marketplace.html           # Main marketplace listing grid
│   ├── listing_detail.html        # Individual listing view & chat
│   ├── sell.html                  # Create new listing form
│   ├── messages.html              # Messages page with conversations
│   ├── planner.html               # Budget planner page
│   └── study_plan.html            # Study planner page
│
├── static/                         # Static Assets
│   ├── css/
│   │   └── style.css              # All styles (Lehigh colors, marketplace layout)
│   ├── js/
│   │   └── main.js               # Common JavaScript functions
│   └── images/
│       └── logo.png              # DormDealz logo
│
└── data/                          # JSON Data Storage
    ├── listings.json              # Marketplace listings
    ├── users.json                 # User accounts
    ├── messages.json              # Chat messages
    ├── conversations.json         # Conversation metadata
    ├── bookmarks.json             # Saved/favorited listings
    ├── blocks.json                # Blocked user relationships
    ├── reports.json               # User reports
    └── classes.json               # User's enrolled classes
```

## API Endpoints

### Listings
- `GET /api/listings` - Get all listings
- `POST /api/listings` - Create new listing
- `DELETE /api/listings/<id>` - Delete a listing (owner only)

### Messaging
- `GET /api/messages/conversations` - Get user's conversations
- `GET /api/messages/conversations/<id>` - Get messages in a conversation
- `POST /api/messages` - Send a message
- `DELETE /api/messages/conversations/<id>` - Delete a conversation
- `POST /api/messages/<id>/react` - Add reaction to a message
- `POST /api/messages/<id>/reply` - Reply to a message

### User Actions
- `POST /api/block` - Block a user
- `POST /api/report` - Report a user
- `POST /api/bookmarks` - Save/unsave a listing

## Features in Detail

### Dynamic Filtering
- Filters auto-apply as you type (500ms debounce)
- Combines category, condition, price range, and search
- Real-time listing updates without page reload
- Collapsible filter sections to save space

### Secure Messaging
- One conversation per listing pair (buyer-seller)
- Message reactions: 👍 ❤️ 😂 😮 😢
- Threaded replies for better context
- Automated content moderation
- Block/report functionality with confirmations
- Conversation deletion with cascade (removes all messages)

### Image Gallery
- Multi-image upload support
- Thumbnail navigation
- Previous/Next buttons
- Smooth fade transitions
- Keyboard navigation (arrow keys)
- Touch/swipe gestures on mobile

### User Safety
- Block prevents future messages
- Report system with categorized reasons
- Content flagging for inappropriate messages
- Owner-only deletion of listings
- Confirmation dialogs for destructive actions

## Customization

### Adding Categories
Edit `CATEGORIES` in `planner/budget_planner.py`:
```python
CATEGORIES = [
    "Textbooks",
    "School Supplies",
    "Electronics",
    "Your New Category"
]
```

### Changing Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --brand-brown: #653819;  /* Lehigh brown */
    --brand-gold: #FFD700;   /* Lehigh gold */
}
```

### Adding Report Reasons
Edit the report prompt in `templates/messages.html` or `listing_detail.html`:
```javascript
const reason = prompt("Reason: harassment, spam, scam, inappropriate, other");
```

## Future Enhancements

- Payment processing integration
- Email notifications for new messages
- Advanced search with filters for classes/courses
- Seller ratings and reviews
- Price history tracking
- Image compression and CDN hosting
- Mobile app (React Native or Flutter)
- Admin dashboard for moderation
- Automated listing expiration
- Integration with Lehigh course catalog

## Credits

**DormDealz** - Built for Lehigh University students by students

- Designed with Facebook Marketplace-inspired UI/UX
- Powered by Flask and modern web technologies
- Lehigh brown and gold branding
- Secure, monitored messaging system

## License

Open source - Available for educational and non-commercial use

---

**DormDealz: Study Hard. Spend Smart.**

*Your trusted marketplace for Lehigh University students*
