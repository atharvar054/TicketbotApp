import 'package:flutter/material.dart';
import '../controllers/ticket_controller.dart';
import '../models/ticket_model.dart';

class TicketView extends StatefulWidget {
  const TicketView({super.key});

  @override
  State<TicketView> createState() => _TicketViewState();
}

class _TicketViewState extends State<TicketView> {
  final _controller = TicketController();
  final _inputController = TextEditingController();
  String _result = '';
  bool _loading = false;

  Future<void> _sendRequest() async {
    setState(() => _loading = true);

    try {
      final request = TicketRequest(userInput: _inputController.text);
      final response = await _controller.fetchTicket(request);
      setState(() => _result = response.finalAnswer);
    } catch (e) {
      setState(() => _result = 'Error: $e');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ticket Bot')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _inputController,
              decoration: const InputDecoration(
                labelText: 'Enter your query',
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _loading ? null : _sendRequest,
              child: _loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Get Ticket'),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Text(_result),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
