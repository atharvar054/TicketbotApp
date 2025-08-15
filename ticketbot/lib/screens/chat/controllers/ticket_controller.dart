import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../core/services/api_config.dart';
import '../models/ticket_model.dart';

class TicketController {
  Future<TicketResponse> fetchTicket(TicketRequest request) async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/ask');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(request.toJson()),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return TicketResponse.fromJson(data);
      } else {
        throw Exception('Failed to get ticket: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
