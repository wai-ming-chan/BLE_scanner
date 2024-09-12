from flask import Flask, render_template, request
import Penguin_scanner as p_scanner  # Assuming this is your custom module

app = Flask(__name__)

# Helper function to clean and extract the scanned string
def clean_input(input_string):
    return input_string.replace('\n', '').strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract and clean inputs
        box_barcode = clean_input(request.form.get('box_barcode'))
        box_qr = clean_input(request.form.get('box_qr'))
        device_barcode = clean_input(request.form.get('device_barcode'))
        device_qr = clean_input(request.form.get('device_qr'))

        # Call p_scanner on the first QR code (box QR code)
        input_address = box_qr
        try:
            mac, pn, soc = p_scanner.run_scanner(input_address)
        except Exception as e:
            return render_template('index.html', error=str(e))

        # Check if MAC matches
        mac_match = (mac == box_qr == device_qr)

        # Check if PN matches
        pn_match = (pn == box_barcode == device_barcode)

        # Pass results to the template
        return render_template(
            'index.html',
            mac=mac,
            pn=pn,
            soc=soc,
            mac_match=mac_match,
            pn_match=pn_match,
            box_barcode=box_barcode,
            box_qr=box_qr,
            device_barcode=device_barcode,
            device_qr=device_qr
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
