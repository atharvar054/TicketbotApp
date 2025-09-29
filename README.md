# TicketBot App (Flutter + Flask)

A bilingual (English/Marathi) ticket assistant for Mumbai local trains.
- Flutter frontend (mobile/web)
- Flask backend (fares + AI + speech-to-text)

## Features
- Bilingual input (EN/MR)
- Fare calculation (1st/2nd class)
- Voice input on web (Record → Transcribe → Auto-search)
- Simple MVC in Flutter

## Project Structure
```
TicketbotApp/
├─ ticketbot/                # Flutter app
│  └─ lib/screens/chat/      # Ticket UI (MVC)
├─ ticketbot_backend/        # Flask backend API
│  ├─ ticket_bot.py          # Main API + /api/transcribe
│  ├─ transcribe_audio.py    # CLI speech->text helpers
│  └─ fares.json             # Fare data
└─ deployment/               # (optional) Docker files
```

## Prerequisites
- Flutter 3.8+
- Python 3.11+
- Google Gemini API key
- Google Cloud Speech-to-Text enabled + service account JSON
- ffmpeg installed (for webm→wav on backend)

### Frontend
- **Flutter**: Cross-platform UI framework
- **Dart**: Programming language
- **HTTP**: API communication
- **Material Design**: UI components

### Backend
- **Flask**: Python web framework
- **Google Gemini AI**: Natural language processing
- **CORS**: Cross-origin resource sharing
- **Gunicorn**: Production WSGI server

## 📋 Prerequisites
- **Flutter SDK** (3.8.1 or higher)
- **Python 3.11** or higher
- **Google Gemini API Key**
- **Git**

## 🔧 Setup Instructions
### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd TicketbotApp
```
### 2. Backend Setup
#### Install Python Dependencies
```bash
cd ticketbot_backend
pip install -r requirements.txt
# .env should contain GOOGLE_API_KEY=... (Gemini)
# ticket_bot.py points GOOGLE_APPLICATION_CREDENTIALS to your service account JSON
python ticket_bot.py
# Runs at http://127.0.0.1:8000
```

Notes
- Voice recording uses /api/transcribe
- If testing over LAN (http://192.168.x.x:8000), mic requires HTTPS or dev flag; easiest is an https tunnel (e.g., ngrok)

## Flutter Setup
```bash
cd ticketbot
flutter pub get
# Web local
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8000
# Android emulator
flutter run -d android --dart-define=API_BASE_URL=http://10.0.2.2:8000
# Real device (LAN): replace with your PC IP
flutter run -d <device-id> --dart-define=API_BASE_URL=http://192.168.1.45:8000
```

## Web Voice Flow (Backend Page)
- Open backend home page (GET /)
- Click "Start Recording" → speak → click again
- Backend:
  - Receives audio at /api/transcribe
  - Converts to 16kHz mono WAV
  - Transcribes with Google Speech
  - Auto-fills the "user_input" field
  - Submits the form to /ask
  - Renders fare answer inside the assistant window
  - Shows transcript below the mic button

## Minimal API Endpoints
- POST `/api/ask`
  - Body: `{ "user_input": "Dadar to CSMT" }`
  - Returns JSON with parsed fields + `final_answer`
- POST `/api/transcribe`
  - FormData with `file` (audio/webm)
  - Returns `{ transcript, final_answer }` (used by backend page)

