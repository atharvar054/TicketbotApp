# TicketBot App

A bilingual (English/Marathi) ticket booking chatbot for Mumbai local train services with Flutter frontend and Flask backend.

## 🚀 Features

- **Bilingual Support**: English and Marathi language processing
- **AI-Powered**: Google Gemini AI for natural language understanding
- **Real-time Fare Calculation**: First and second class ticket pricing
- **Cross-platform**: Android, iOS, Web, Desktop
- **Smart Parsing**: Extracts source, destination, passenger count, return preferences

## 📁 Project Structure

```
TicketbotApp/
├── ticketbot/                 # Flutter frontend
│   ├── lib/screens/chat/      # Main ticket interface (MVC pattern)
│   └── android/               # Android configuration
├── ticketbot_backend/         # Flask backend API
│   ├── ticket_bot.py          # Main application
│   ├── fares.json             # Fare database
│   └── requirements.txt       # Python dependencies
└── deployment/                # Docker deployment files
```

## 🛠️ Technology Stack

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

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run backend
python ticket_bot.py
```

### Frontend Setup
```bash
cd ticketbot
flutter pub get

# Run on different platforms
flutter run -d android                    # Android emulator
flutter run -d chrome                     # Web browser
flutter run -d <device-id>                # Real device
```

## 📱 Mobile App Usage

### Development (USB Connection)
```bash
# Find your laptop's IP
ipconfig

# Run with your IP
flutter run -d <device-id> --dart-define=API_BASE_URL=http://192.168.1.45:8000
```

### Permanent Installation
```bash
# Install permanently
flutter install -d <device-id> --dart-define=API_BASE_URL=http://192.168.1.45:8000

# Or build APK
flutter build apk --release --dart-define=API_BASE_URL=http://192.168.1.45:8000
```

## ☁️ Production Deployment

### Quick Deploy (Render.com)
1. Connect GitHub repo to Render
2. Create Web Service with:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -b 0.0.0.0:$PORT ticket_bot:app`
   - Environment: `GOOGLE_API_KEY=your_key`
3. Deploy and use the URL in your app

### Update App for Production
```bash
flutter build apk --release --dart-define=API_BASE_URL=https://your-app.onrender.com
```

## 🔍 API Usage

### Endpoint: `POST /api/ask`
```json
// Request
{
  "user_input": "Mumbai to Pune ticket for 2 people"
}

// Response
{
  "source": "मुंबई",
  "destination": "पुणे", 
  "passenger_count": "दोन",
  "return_ticket": "नाही",
  "first_class_fare": "₹१७०",
  "second_class_fare": "₹२०",
  "final_answer": "स्रोत स्थान: मुंबई\nगंतव्य स्थान: पुणे\n..."
}
```

## 🎯 Sample Queries

- "मुंबई ते पुणे तिकीट"
- "Dadar to Bandra return ticket for 2 passengers"
- "दादर ते बांद्रा परतीचं तिकीट"
- "Mumbai to Pune ticket for 3 people"

## 🔧 Configuration

### Network URLs
- **Android Emulator**: `http://10.0.2.2:8000`
- **Real Device**: `http://your-laptop-ip:8000`
- **Production**: `https://your-deployed-backend.com`

### Environment Variables
- `GOOGLE_API_KEY`: Google Gemini API key
- `API_BASE_URL`: Backend URL for Flutter app

## 🐛 Troubleshooting

**Backend Connection Failed:**
- Ensure backend runs on `0.0.0.0:8000`
- Check both devices on same WiFi network
- Verify firewall settings

**Mobile App Issues:**
- Enable USB debugging (Android)
- Trust computer (iOS)
- Check device permissions

**Build Issues:**
```bash
flutter clean && flutter pub get
```
