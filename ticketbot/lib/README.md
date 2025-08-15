# Ticket Bot Flutter App - Code Structure

## Overview
This is a Flutter application for a ticket booking chatbot. The app allows users to interact with a backend API to get ticket information and booking assistance.

## Folder Structure

### `/lib` - Main Application Code

#### `/core` - Core Services and Configuration
- **`/services/api_config.dart`** - API configuration and base URL settings
  - Contains `ApiConfig` class with base URL configuration
  - Supports different environments (Android emulator, iOS simulator, real device)
  - Uses environment variables for flexible deployment

#### `/screens` - UI Screens Organized by Feature
Each screen follows the **Model-View-Controller (MVC)** pattern:

##### `/chat` - Chat/Ticket Booking Feature
- **`/controllers/ticket_controller.dart`** - Business Logic
  - Handles API communication with the backend
  - Manages ticket requests and responses
  - Error handling and data processing

- **`/models/ticket_model.dart`** - Data Models
  - `TicketRequest` - Represents user input for ticket queries
  - `TicketResponse` - Represents API response with ticket information
  - JSON serialization/deserialization methods

- **`/views/ticket_view.dart`** - User Interface
  - Main chat interface for ticket queries
  - Text input field for user questions
  - Displays API responses
  - Loading states and error handling

##### `/language_select` - Language Selection Feature
- **`/controllers/`** - Language selection logic
- **`/models/`** - Language data models
- **`/views/`** - Language selection UI

##### `/settings` - App Settings Feature
- **`/controllers/`** - Settings management logic
- **`/models/`** - Settings data models
- **`/views/`** - Settings UI

##### `/ticket_history` - Ticket History Feature
- **`/controllers/`** - History management logic
- **`/models/`** - History data models
- **`/views/`** - History display UI

#### Root Files
- **`main.dart`** - Application entry point
  - Initializes the Flutter app
  - Sets up theme and navigation
  - Currently points to TicketView as the home screen

- **`routes.dart`** - Navigation configuration
  - Defines app routes and navigation structure
  - Maps route names to screen widgets

## Architecture Patterns

### MVC (Model-View-Controller)
- **Models**: Data structures and business logic
- **Views**: User interface components
- **Controllers**: Handle user interactions and coordinate between models and views

### Service Layer
- API communication is abstracted through service classes
- Configuration is centralized in the core services

## Key Features

1. **API Integration**: Communicates with backend ticket bot API
2. **Error Handling**: Comprehensive error handling for network requests
3. **Loading States**: UI feedback during API calls
4. **Responsive Design**: Works across different screen sizes
5. **Modular Architecture**: Easy to extend and maintain

## Dependencies
- `http`: For API communication
- `flutter`: Core Flutter framework
- `cupertino_icons`: iOS-style icons

## Configuration
The app uses environment variables for API configuration:
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://127.0.0.1:8000`
- Real Device: Use your computer's IP address

## Usage
1. Enter your ticket query in the text field
2. Press "Get Ticket" button
3. View the response from the ticket bot API
4. The app handles loading states and errors automatically 