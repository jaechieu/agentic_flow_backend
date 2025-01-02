import base64
import pdfplumber
import json
import openai


# Helper: Standard CORS headers
def get_cors_headers(event):
    origin = event.get("headers", {}).get("origin", "http://localhost:3000")
    return {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    }


# Helper: Centralized response generation
def create_response(event, status_code, body):
    headers = {**get_cors_headers(event), "Content-Type": "application/json"}
    return {"statusCode": status_code, "headers": headers, "body": json.dumps(body)}


# Handle GET requests
def handle_get_request(event):
    data = [
        {"id": "Prompt", "name": "Prompt Node"},
        {"id": "LLM", "name": "LLM Node"},
        {"id": "Tool", "name": "Tool Node"},
        {"id": "Chain", "name": "Chain Node"},
    ]
    return create_response(event, 200, data)


# Parse POST payload
def parse_post_payload(event):
    try:
        body = json.loads(event.get("body", "{}"))
        pdf_base64 = body.get("pdf_base64")
        number_of_people = body.get("number_of_people")
        number_of_breakout_rooms = body.get("number_of_breakout_rooms")
        number_of_nights = body.get("number_of_nights")

        if not pdf_base64:
            raise ValueError("No PDF file provided in the payload")

        return pdf_base64, number_of_people, number_of_breakout_rooms, number_of_nights
    except Exception as e:
        raise ValueError(f"Invalid request: {str(e)}")


# Decode and save Base64 PDF
def decode_pdf(pdf_base64, output_path):
    with open(output_path, "wb") as file:
        file.write(base64.b64decode(pdf_base64))


# Extract text from PDF
def extract_pdf_text(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text += f"Page {i + 1}:\n{page.extract_text()}\n\n"
        return text
    except Exception as e:
        raise ValueError(f"Error processing the PDF: {str(e)}")


# Generate GPT response
def generate_gpt_response(text):
    prompt = f"""
    You are a helpful assistant. I have extracted text and data from a PDF document. Please process the following:

    I need the following information extracted from the document, formatted as valid JSON with no extra explanation or comments:

    {{
        "meeting_room_cost_per_person": double,
        "sleeping_room_cost_per_night": double,
        "breakout_room_cost_per_person": double
    }}

    Replace 'double' with the appropriate numeric values extracted from the document. If there is tax or additional fees included, factor them in as well. Make sure your output is valid JSON with no extra special characters.

    Document Content:
    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.0,
    )
    return json.loads(response["choices"][0]["message"]["content"].strip())


# Calculate quotes
def calculate_quotes(
    data, number_of_people, number_of_breakout_rooms, number_of_nights
):
    data["meeting_room_quote"] = (
        number_of_people
        * data["meeting_room_cost_per_person"]
        * number_of_breakout_rooms
    )
    data["sleeping_room_quote"] = (
        number_of_people * number_of_nights * data["sleeping_room_cost_per_night"]
    )
    data["total_quote"] = data["meeting_room_quote"] + data["sleeping_room_quote"]
    return data


# Handle POST requests
def handle_post_request(event):
    input_path = "/tmp/input.pdf"

    try:
        pdf_base64, number_of_people, number_of_breakout_rooms, number_of_nights = (
            parse_post_payload(event)
        )
        decode_pdf(pdf_base64, input_path)
        text = extract_pdf_text(input_path)
        gpt_response = generate_gpt_response(text)
        quotes = calculate_quotes(
            gpt_response, number_of_people, number_of_breakout_rooms, number_of_nights
        )
        return create_response(
            event, 200, {"message": "Processing complete.", "data": quotes}
        )
    except Exception as e:
        return create_response(event, 400, {"error": str(e)})


# Lambda Handler
def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "").upper()

    if method == "OPTIONS":
        return create_response(event, 200, "")

    if method == "GET":
        return handle_get_request(event)

    if method == "POST":
        return handle_post_request(event)

    return create_response(event, 405, {"error": "Method Not Allowed"})
