import 'package:flutter/material.dart';
import 'screens/chat/views/ticket_view.dart';

class AppRoutes {
  static const String home = '/';
  static const String chat = '/chat';
  static const String settings = '/settings';
  static const String history = '/history';

  static Map<String, WidgetBuilder> getRoutes() {
    return {
      home: (context) => const TicketView(),
      chat: (context) => const TicketView(),
      // Add more routes as needed
    };
  }
}
