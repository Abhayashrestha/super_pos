import qrcode
import io
import base64


class ReceiptService:
    @staticmethod
    def generate_qr(receipt):
        data=str(receipt)
        qr=qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer=io.BytesIO()
        img.save(buffer, format="PNG")
        final=base64.b64encode(buffer.getvalue()).decode('utf-8')
        return final
