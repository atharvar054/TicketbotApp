class ApiConfig {
  // For Android emulator use http://10.0.2.2:8000
  // For iOS simulator use http://127.0.0.1:8000
  // For a real phone on same Wi-Fi use your laptop IP, e.g. http://192.168.1.50:8000
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
}
