class TicketRequest {
  final String userInput;

  TicketRequest({required this.userInput});

  Map<String, dynamic> toJson() {
    return {
      'user_input': userInput,
    };
  }
}

class TicketResponse {
  final String finalAnswer;

  TicketResponse({required this.finalAnswer});

  factory TicketResponse.fromJson(Map<String, dynamic> json) {
    return TicketResponse(
      finalAnswer: json['final_answer'] ?? '',
    );
  }
}
