import 'dart:io';
import 'package:flutter/foundation.dart';

class ApiConfig {
  static String get baseUrl {
    // Check if API_BASE_URL is provided via command line
    const apiUrl = String.fromEnvironment('API_BASE_URL');
    if (apiUrl.isNotEmpty) {
      return apiUrl;
    }
    
    // Platform-specific defaults
    if (kIsWeb) {
      // return 'http://127.0.0.1:8000'; // Web
      return 'http://192.168.1.7:8000'; // Web - your laptop's IP
    } else if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000'; // Android emulator
    } else if (Platform.isIOS) {
      return 'http://127.0.0.1:8000'; // iOS simulator
    } else {
      // return 'http://127.0.0.1:8000'; // Desktop/other
      return 'http://192.168.1.7:8000'; // Desktop/other - your laptop's IP
    }
  }
}
