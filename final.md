# WealthPlay - Final Project Documentation

## Project Overview

WealthPlay is a Django-based financial literacy learning platform that combines interactive courses with AI-powered mentors. The platform uses a conversational learning approach with two AI mentors (Wise and Nex) and integrates Ollama LLM for intelligent responses.

## Project Structure

### Root Directory Files

- **`manage.py`**: Django's command-line utility for administrative tasks
- **`requirements.txt`**: Python dependencies for the project
- **`financial_course.json`**: Main course data source with topics, lessons, and fixed Q&A
- **`scenarios.json`**: Scenario data for the financial simulator
- **`db.sqlite3`**: SQLite database file (development)

### Django Apps

#### 1. **`wealthplay/`** - Main Project Configuration
- **`settings.py`**: Django project settings including installed apps, middleware, database config, REST framework, CORS, Channels
- **`urls.py`**: Root URL routing configuration
- **`wsgi.py`** / **`asgi.py`**: WSGI/ASGI application entry points
- **`views.py`**: Landing page view

#### 2. **`courses/`** - Course Management App
- **`models.py`**: Django models for Course, Topic, Lesson, Message, Progress
- **`views.py`**: View functions for course pages and authentication
- **`course_views.py`**: JSON API endpoints for serving course data from `financial_course.json`
- **`urls.py`**: URL routing for course pages and API endpoints
- **`serializers.py`**: DRF serializers for course data
- **`admin.py`**: Django admin configuration
- **`management/commands/`**: Custom management commands
  - **`import_course_data.py`**: Command to populate courses from JSON

**Key Features**:
- Serves course data from JSON file
- Transforms topics/lessons structure to course/modules format
- Provides REST API endpoints for course data
- Handles course detail pages with chat interface

#### 3. **`chat/`** - Chat & AI Mentor App
- **`models.py`**: ChatMessage and Attachment models
- **`views.py`**: API endpoints for mentor responses
  - `mentor_respond()`: Course-specific mentor (fixed Q&A + Ollama)
  - `mentor_respond_rag()`: RAG-based mentor (vector DB)
  - `general_inquiry()`: General inquiry endpoint (Ollama only)
- **`urls.py`**: Chat API routing
- **`serializers.py`**: Chat message serializers
- **`consumers.py`**: WebSocket consumers for real-time chat (if using Channels)

**Key Features**:
- Two-layer response system: fixed Q&A → Ollama LLM
- Integration with Ollama for LLM responses
- Course context injection for better responses

#### 4. **`mentor_engine/`** - AI Mentor Engine
- **`course_mentor.py`**: Core mentor logic
  - `mentor_respond()`: Main mentor response function
  - `generate_ollama_response()`: Ollama LLM integration
  - `fuzzy_match_q()`: Fixed Q&A matching
  - `find_course()` / `find_module()`: Course data retrieval
- **`mentor.py`**: RAG-based mentor using vector DB (ChromaDB)
- **`test_mentor.py`**: Testing utilities

**Key Features**:
- Fixed Q&A fuzzy matching for instant authoritative answers
- Ollama LLM integration with course context
- Few-shot learning using fixed Q&A examples

#### 5. **`cursor/`** - Nex Mentor Integration
- **`mentor_engine.py`**: Nex mentor engine implementation
- **`views.py`**: API endpoints for Nex mentor
- **`urls.py`**: URL routing
- **`INTEGRATION_EXAMPLE.html`**: Frontend integration example

#### 6. **`simulator/`** - Financial Scenario Simulator
- **`models.py`**: Scenario, DecisionOption, UserScenarioLog models
- **`views.py`**: Scenario game engine views
- **`urls.py`**: Scenario page routing
- **`templates/scenario_play.html`**: Scenario game interface
- **`management/commands/import_scenarios.py`**: Import scenarios from JSON

**Key Features**:
- Interactive financial decision scenarios
- Decision tracking and logging
- Branching scenario paths

#### 7. **`users/`** - User Management
- **`models.py`**: UserProgress, QuizAttempt models
- **`views.py`**: User progress and quiz tracking
- **`serializers.py`**: User data serializers

#### 8. **`uploads/`** - File Upload Management
- **`models.py`**: UploadedFile model
- **`views.py`**: File upload handling

### Templates

- **`templates/landing.html`**: Landing page with black background and course/scenario links
- **`templates/courses/course_home.html`**: Course listing page (redirects to first course)
- **`templates/courses/course_detail.html`**: Main course chat interface with sidebar navigation

### Static Files

- **`static/js/mentor_widget.js`**: Floating chatbot widget for landing page
- **`static/js/nex_mentor.js`**: Nex mentor frontend integration
- **`static/css/nex_mentor.css`**: Nex mentor styling

### Data Files

- **`financial_course.json`**: Structured course data with topics, lessons, and fixed Q&A
- **`scenarios.json`**: Financial scenario data for simulator
- **`mentor_content/`**: Additional mentor content (lessons, frameworks, FAQs)

### Vector Database

- **`vector_db/`**: ChromaDB vector database for RAG-based mentor
  - Stores embeddings of course content
  - Used for semantic search and retrieval

## How It Works

### Course Flow

1. User visits `/course/` → redirects to first course
2. Course data loaded from `financial_course.json`
3. Topics displayed in sidebar navigation
4. Selected topic shows chat interface with modules
5. User can ask questions or click Overview/Explain buttons
6. Two-layer response system:
   - First checks fixed Q&A for instant answers
   - If no match, uses Ollama LLM with course context

### AI Mentor System

1. **Fixed Q&A Layer**: Fuzzy matching against pre-defined Q&A pairs
2. **Ollama LLM Layer**: 
   - Loads course/module context
   - Adds fixed Q&A as few-shot examples
   - Sends to Ollama with system prompt
   - Returns generated response

### Authentication

- Session-based authentication using Django's built-in auth
- Login/signup modals for non-authenticated users
- Logout button for authenticated users

## Future Implementations

### High Priority

1. **User Progress Tracking**
   - Save user progress across courses
   - Track completed modules
   - Quiz scores and achievements

2. **Enhanced AI Features**
   - Conversation memory across sessions
   - Personalized learning paths
   - Adaptive difficulty based on user performance

3. **Course Management**
   - Admin interface for course creation/editing
   - Version control for course content
   - A/B testing for course effectiveness

### Medium Priority

4. **Social Features**
   - Group sessions (mentioned in UI)
   - User discussions and forums
   - Peer learning groups

5. **Analytics Dashboard**
   - User engagement metrics
   - Course completion rates
   - AI response quality metrics

6. **Mobile App**
   - React Native mobile app
   - Offline course access
   - Push notifications

### Low Priority

7. **Advanced Features**
   - Video lessons integration
   - Interactive calculators and tools
   - Portfolio simulation integration
   - Certificate generation

8. **Integrations**
   - Payment gateway for premium courses
   - Email marketing integration
   - Analytics platform integration

## Development Notes

- **Database**: Currently using SQLite for development. Migrate to PostgreSQL for production.
- **Vector DB**: ChromaDB used for RAG. Consider Pinecone/Milvus for production scaling.
- **Ollama**: Runs locally. For production, consider cloud LLM APIs or self-hosted Ollama server.
- **Authentication**: Currently basic Django auth. Consider adding OAuth2, JWT tokens for API.

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Configure production static file serving
- [ ] Set up SSL certificates
- [ ] Configure production Ollama server
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Load testing and optimization

