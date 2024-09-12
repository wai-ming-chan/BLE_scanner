from flask import Flask, render_template, request

app = Flask(__name__)

# Mock function to get item details and check results
def get_item_data(item_number, rack_location):
    # Replace this with actual data retrieval logic
    return {
        'barcodes_match': True,
        'qrcodes_match': False,
        'SoC': 85,  # State of Charge (mock data)
        'date': '2024-09-12',
        'time': '14:30:00',
        'PN': '987654',
        'MAC': '00:1A:2B:3C:4D:5F',
        'rack_soc': [[[85, 80, 75], [70, 65, 60], [55, 50, 45]],
                     [[40, 35, 30], [25, 20, 15], [10, 5, 0]]] * 6  # Mock SoC data for 3x3x12 grid
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    item_data = None
    rack_location = None
    if request.method == 'POST':
        item_number = request.form.get('item_number')
        # Get selected rack-row-device location from the 3x3x12 radio button grid
        rack_location = request.form.get('rack_location')
        if item_number and rack_location:
            item_data = get_item_data(item_number, rack_location)  # Query function
    
    return render_template('index.html', item_data=item_data)

if __name__ == '__main__':
    app.run(debug=True)
