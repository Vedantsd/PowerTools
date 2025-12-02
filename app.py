import io
import base64
from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/qr-generator', methods=['GET', 'POST'])
def qr_generator():
    qr_data_base64 = None
    
    if request.method == 'POST':
        data_to_encode = request.form.get('data')
        
        if data_to_encode:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_to_encode)
            qr.make(fit=True)

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                fill_color="black",
                back_color="white",
            )
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            qr_data_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return render_template('qr-generator.html', qr_data_base64=qr_data_base64)

if __name__ == '__main__':
    app.run(debug=True)