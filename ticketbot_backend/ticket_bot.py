from flask import Flask, request, render_template
from flask import jsonify
from flask_cors import CORS
import google.generativeai as genai
import requests
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
# Configure Gemini with the loaded API key
genai.configure(api_key=api_key)
# Set up Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
fares_json_path = os.path.join(BASE_DIR, 'fares.json')

with open(fares_json_path, 'r', encoding='utf-8') as f:
    fares_data_json = json.load(f)

# Convert nested format to flat dict: {(source, destination): {"first": X, "second": Y}}
fares_data = {}
for source, destinations in fares_data_json.items():
    for destination, fare in destinations.items():
        # Make sure fare is a dict and has keys '1' and '2'
        if isinstance(fare, dict) and '1' in fare and '2' in fare:
            fares_data[(source, destination)] = {
                "first": fare['1'],
                "second": fare['2']
            }

# Debug: Print some sample data to verify structure
print("DEBUG: Sample fares_data entries:")
sample_count = 0
for (src, dst), fare_info in fares_data.items():
    if sample_count < 5:
        print(f"  {src} -> {dst}: First={fare_info['first']}, Second={fare_info['second']}")
        sample_count += 1

# GEMINI: Extract all info from input
def get_gemini_response(user_input):
    prompt = f"""
तुम्ही एक हुशार तिकीट सहाय्यक आहात.

खालील वाक्यातून वापरकर्त्याची माहिती समजून घ्या:

1. **स्रोत स्थान (source)** आणि **गंतव्य स्थान (destination)** ओळखा.
2. वापरकर्ता किती प्रवासी आहेत हे तपासा. लक्षात ठेवा:
   - "चार लोकांसाठी", "दोन माणसे", "तीन प्रवासी", "एक व्यक्ती" अशा सर्व प्रकारच्या संख्या शोधा
   - जर दिले नसेल, तर "1 प्रवासी" गृहित धरा
   - फक्त संख्या शोधा, शब्दांच्या रूपावर अवलंबून राहू नका
3. वापरकर्ता परतीचं तिकीट मागत आहे का हे तपासा. जर काही सांगितले नसेल, तर एकमार्गचं (one-way) तिकीट गृहित धरा.
4. वाक्यात इंग्रजी आणि मराठी भाषा दोन्ही वापरल्या असल्या तरी अडचण नको.
5. जर स्रोत किंवा गंतव्य माहिती नसेल, तर "निश्चित नाही" लिहा आणि भाडंही "निश्चित नाही" असावं.

फक्त आणि फक्त खालील स्वरूपात मराठीत उत्तर द्या (नेहमीच या सहा ओळी असाव्यात):  

स्रोत स्थान: <source किंवा "निश्चित नाही">  
गंतव्य स्थान: <destination किंवा "निश्चित नाही">  
प्रवासी संख्या: <मराठीत संख्या>  
परतीचं तिकीट: <"होय" किंवा "नाही">  
एकूण भाडं (फर्स्ट क्लास): ₹८५  
एकूण भाडं (सेकंड क्लास): ₹१०

वाक्य: "{user_input}"
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# Converts Marathi station names to English
def gemini_conv_to_eng(source_mar, destination_mar):
    prompt = f"""
तुमच्याकडे खालील दोन स्थानांची नावे मराठीत दिली आहेत: "{source_mar}" आणि "{destination_mar}".
ती फक्त इंग्रजीत लिहा. लक्षात ठेवा:
- CSMT = CST = Chhatrapati Shivaji Maharaj Terminus
- सीएसटी = CSMT
- सीएसएमटी = CSMT
- खारघर = Khargar (not Kharghar)
- मुलुंड = Mulund
- दादर = Dadar
- बांद्रा = Bandra
- ठाणे = Thane
- पनवेल = Panvel
- कल्याण = Kalyan
- कुर्ला = Kurla
- चेंबूर = Chembur
- बोरीवली = Borivali
- बायकुल्ला = Byculla
- चर्चगेट = Churchgate
- मुंबई सेंट्रल = Mumbai Central

फक्त खालील स्वरूपात उत्तर द्या:

source_eng: <source_in_english>  
destination_eng: <destination_in_english>
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    source_eng, destination_eng = "", ""
    for line in text.split('\n'):
        if line.startswith("source_eng:"):
            source_eng = line.replace("source_eng:", "").strip()
        elif line.startswith("destination_eng:"):
            destination_eng = line.replace("destination_eng:", "").strip()
    
    # Additional mapping for common variations
    station_mapping = {
        'CST': 'CSMT',
        'Chhatrapati Shivaji Maharaj Terminus': 'CSMT',
        'Kharghar': 'Khargar',
        'Mumbai Central': 'Mumbai Central',
        'MumbaiCentral': 'Mumbai Central'
    }
    
    source_eng = station_mapping.get(source_eng, source_eng)
    destination_eng = station_mapping.get(destination_eng, destination_eng)
    
    return source_eng, destination_eng

# Converts English numbers to Marathi
def gemini_conv_from_eng(firstclass_fare_eng, secondclass_fare_eng):
    prompt = f"""
तुमच्याकडे दोन इंग्रजी अंक आहेत: "{firstclass_fare_eng}" आणि "{secondclass_fare_eng}".
त्यांना फक्त मराठी आकड्यांमध्ये लिहा.

firstclass_fare_mar: ₹<marathi_firstclass_fare>  
secondclass_fare_mar: ₹<marathi_secondclass_fare>
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    firstclass_fare_mar, secondclass_fare_mar = "", ""
    for line in text.split('\n'):
        if line.startswith("firstclass_fare_mar:"):
            firstclass_fare_mar = line.replace("firstclass_fare_mar:", "").strip()
        elif line.startswith("secondclass_fare_mar:"):
            secondclass_fare_mar = line.replace("secondclass_fare_mar:", "").strip()
    return firstclass_fare_mar, secondclass_fare_mar

def process_ticket_request(user_input):
    gemini_response = get_gemini_response(user_input)
    print("\nGEMINI RESPONSE:\n", gemini_response)

    # Parse Gemini response
    lines = gemini_response.strip().split('\n')
    source_mar, destination_mar = "", ""
    passenger_count = 1
    is_return = False

    for line in lines:
        if line.startswith("स्रोत स्थान:"):
            source_mar = line.replace("स्रोत स्थान:", "").strip()
        elif line.startswith("गंतव्य स्थान:"):
            destination_mar = line.replace("गंतव्य स्थान:", "").strip()
        elif line.startswith("प्रवासी संख्या:"):
            marathi_number = line.replace("प्रवासी संख्या:", "").strip()
            num_map = {
                'शून्य': 0, 'एक': 1, 'दोन': 2, 'तीन': 3, 'चार': 4, 'पाच': 5,
                'सहा': 6, 'सात': 7, 'आठ': 8, 'नऊ': 9, 'दहा': 10,
                'अकरा': 11, 'बारा': 12, 'तेरा': 13, 'चौदा': 14, 'पंधरा': 15
            }
            for word, num in num_map.items():
                if word in marathi_number:
                    passenger_count = num
                    break
            else:
                digits = re.findall(r'\d+', marathi_number)
                if digits:
                    passenger_count = int(digits[0])
                else:
                    passenger_count = 1
        elif line.startswith("परतीचं तिकीट:"):
            is_return = 'होय' in line

    # Fare calculation
    if source_mar == "निश्चित नाही" or destination_mar == "निश्चित नाही":
        firstclass_fare_mar = "निश्चित नाही"
        secondclass_fare_mar = "निश्चित नाही"
    else:
        source_eng, destination_eng = gemini_conv_to_eng(source_mar, destination_mar)
        print(f"\nDEBUG - Station Conversion: {source_mar} -> {source_eng}, {destination_mar} -> {destination_eng}")

        fares = fares_data.get((source_eng, destination_eng))
        reverse_fares = fares_data.get((destination_eng, source_eng))

        if fares:
            base_first = fares["first"]
            base_second = fares["second"]
        elif reverse_fares:
            base_first = reverse_fares["first"]
            base_second = reverse_fares["second"]
        else:
            base_first = base_second = 0

        multiplier = passenger_count * (2 if is_return else 1)
        total_first = base_first * multiplier
        total_second = base_second * multiplier

        firstclass_fare_mar, secondclass_fare_mar = gemini_conv_from_eng(str(total_first), str(total_second))

    # Convert passenger count & return ticket to Marathi
    num_map_reverse = {
        0: 'शून्य', 1: 'एक', 2: 'दोन', 3: 'तीन', 4: 'चार', 5: 'पाच',
        6: 'सहा', 7: 'सात', 8: 'आठ', 9: 'नऊ', 10: 'दहा',
        11: 'अकरा', 12: 'बारा', 13: 'तेरा', 14: 'चौदा', 15: 'पंधरा'
    }
    passenger_count_mar = num_map_reverse.get(passenger_count, str(passenger_count))
    return_ticket_mar = "होय" if is_return else "नाही"

    # Final answer string (for web)
    final_answer = f"""स्रोत स्थान: {source_mar}
    गंतव्य स्थान: {destination_mar}
    प्रवासी संख्या: {passenger_count_mar}  
    परतीचं तिकीट: {return_ticket_mar}  
    भाडं - फर्स्ट क्लास : {firstclass_fare_mar}
    भाडं - सेकंड क्लास : {secondclass_fare_mar}
    """

    return (
        final_answer,       # Full Marathi string
        source_mar,         # Source in Marathi
        destination_mar,    # Destination in Marathi
        passenger_count_mar,# Passenger count in Marathi
        return_ticket_mar,  # Return ticket in Marathi
        firstclass_fare_mar,# First class fare in Marathi
        secondclass_fare_mar# Second class fare in Marathi
    )


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ask', methods=["POST"])
def ask():
    user_input = request.form.get("user_input")
    final_answer, *_ = process_ticket_request(user_input)
    return render_template("index.html", user_input=user_input, answer=final_answer)

@app.route('/api/ask', methods=["POST"])
def api_ask():
    try:
        data = request.get_json()
        if not data or "user_input" not in data:
            return jsonify({"error": "Missing 'user_input' in request body"}), 400

        user_input = data["user_input"]
        (
            final_answer,
            source_mar,
            destination_mar,
            passenger_count_mar,
            return_ticket_mar,
            firstclass_fare_mar,
            secondclass_fare_mar
        ) = process_ticket_request(user_input)

        return jsonify({
            "source": source_mar,
            "destination": destination_mar,
            "passenger_count": passenger_count_mar,
            "return_ticket": return_ticket_mar,
            "first_class_fare": firstclass_fare_mar,
            "second_class_fare": secondclass_fare_mar,
            "final_answer": final_answer
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # Bind to all interfaces so real devices on the same network can reach it
    app.run(host="0.0.0.0", debug=True, port=8000)
