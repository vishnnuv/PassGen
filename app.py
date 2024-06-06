from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(
    length,
    include_uppercase,
    include_lowercase,
    include_digits,
    include_special,
    special_characters,
    exclude_ambiguous,
    min_uppercase,
    min_lowercase,
    min_digits,
    min_special
):
    ambiguous_characters = 'il1Lo0O'
    all_characters = ''
    password = []
    
    if include_lowercase:
        lowercase = string.ascii_lowercase
        if exclude_ambiguous:
            lowercase = ''.join(c for c in lowercase if c not in ambiguous_characters)
        all_characters += lowercase
        password += random.choices(lowercase, k=min_lowercase)
    
    if include_uppercase:
        uppercase = string.ascii_uppercase
        if exclude_ambiguous:
            uppercase = ''.join(c for c in uppercase if c not in ambiguous_characters)
        all_characters += uppercase
        password += random.choices(uppercase, k=min_uppercase)
    
    if include_digits:
        digits = string.digits
        if exclude_ambiguous:
            digits = ''.join(c for c in digits if c not in ambiguous_characters)
        all_characters += digits
        password += random.choices(digits, k=min_digits)
    
    if include_special:
        if exclude_ambiguous:
            special_characters = ''.join(c for c in special_characters if c not in ambiguous_characters)
        all_characters += special_characters
        password += random.choices(special_characters, k=min_special)
    
    if len(password) > length:
        raise ValueError("Sum of minimum required characters exceeds the desired password length")
    
    remaining_length = length - len(password)
    password += random.choices(all_characters, k=remaining_length)
    random.shuffle(password)
    
    return ''.join(password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    data = request.json
    password = generate_password(
        length=data.get('length', 12),
        include_uppercase=data.get('include_uppercase', True),
        include_lowercase=data.get('include_lowercase', True),
        include_digits=data.get('include_digits', True),
        include_special=data.get('include_special', True),
        special_characters=data.get('special_characters', string.punctuation),
        exclude_ambiguous=data.get('exclude_ambiguous', True),
        min_uppercase=data.get('min_uppercase', 0),
        min_lowercase=data.get('min_lowercase', 0),
        min_digits=data.get('min_digits', 0),
        min_special=data.get('min_special', 0)
    )
    return jsonify(password=password)

if __name__ == '__main__':
    app.run(debug=True)
