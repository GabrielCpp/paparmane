# Paparmane 🏠👴👩‍🎓

**Connecting Generations Through Shared Living**

Paparmane is an innovative startup prototype that facilitates intergenerational cohabitation by intelligently matching elderly individuals with students. Our AI-powered platform creates meaningful connections that benefit both generations - students find affordable housing while seniors enjoy companionship and support.

## 🌟 Vision

Breaking down generational barriers through shared living spaces, fostering mutual support, cultural exchange, and community building between seniors and young adults.

## ✨ Features

### 🤖 AI-Powered Matching
- Uses advanced language models (Mistral-7B) to analyze compatibility
- Evaluates personality traits, lifestyle preferences, and living habits
- Provides detailed explanations for match recommendations

### 🔄 Real-time Synchronization
- WordPress integration for user profile management
- Automatic profile synchronization and updates
- Cloud-based data storage with Google Firestore

### 🎯 Smart Scheduling
- Batch processing for efficient matching operations
- Queue-based task management with Google Cloud Tasks
- Automated match generation and scheduling

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker
- Poetry (for dependency management)
- Google Cloud SDK (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd paparmane
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Download the AI model**
   ```bash
   # Create models directory and download Mistral-7B model
   mkdir models
   # Download mistral-7b-instruct-v0.1.Q5_K_M.gguf to models/
   ```

5. **Run the development server**
   ```bash
   poetry run python uvicorn_entry.py
   ```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build the image
make build

# Deploy to Google Cloud Run
make deploy
```

## 📚 API Endpoints

### User Management
- `POST /users/sync` - Synchronize user profiles from WordPress
- `POST /users/make_matchs` - Generate matches for all users
- `POST /users/register_match` - Register a match between two profiles

### Matching
- `POST /matchs/spot_check_match` - Test compatibility between two custom profiles

### Example Request
```json
{
  "profileA": {
    "user_id": 1,
    "name": "Marie Dubois",
    "questions": {
      "Age": "72 years old",
      "Living situation": "Lives alone, seeking companionship",
      "Interests": "Gardening, reading, cooking"
    }
  },
  "profileB": {
    "user_id": 2,
    "name": "Alex Student",
    "questions": {
      "Age": "22 years old",
      "Looking for": "Affordable housing near university",
      "Interests": "Sports, technology, helping others"
    }
  }
}
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WordPress     │    │   Paparmane API  │    │  Google Cloud   │
│   (User Mgmt)   │◄──►│   (Matching)     │◄──►│  (Storage/Tasks)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Mistral-7B     │
                       │   (AI Matching)  │
                       └──────────────────┘
```

### Technology Stack
- **Backend**: Python, Litestar, FastAPI-style routing
- **AI/ML**: Llama-cpp-python, Mistral-7B language model  
- **Database**: Google Firestore (NoSQL)
- **Task Queue**: Google Cloud Tasks
- **Integration**: WordPress REST API
- **Deployment**: Docker, Kubernetes (Helm), Google Cloud Run

## 🔧 Configuration

### Environment Variables
```bash
WORDPRESS_TOKEN=your_wordpress_api_token
PROJECT_ID=your_gcp_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
PORT=8000
```

### Model Configuration
The AI matching engine uses Mistral-7B with optimized parameters:
- Temperature: 0.1 (focused responses)
- Top-p: 0.2 (nucleus sampling)
- Context window: 2500 tokens
- Multi-threading support

## 🚢 Deployment

### Google Cloud Run
```bash
make deploy
```

