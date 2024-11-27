import smtplib
import random
import string
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

def generate_code(length=6):
    """Gera um código de verificação de 6 caracteres."""
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

def send_verification_code(email):
    """Envia um código de verificação para o e-mail especificado."""
    try:
        # Validar o e-mail
        valid = validate_email(email)
        email = valid.email

        # Gerar o código de verificação
        code = generate_code()

        # Configurações do servidor SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'seu_email@gmail.com'
        smtp_password = 'sua_senha'

        # Criar a mensagem do e-mail
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = 'Código de Verificação'

        body = f'Seu código de verificação é: {code}'
        msg.attach(MIMEText(body, 'plain'))

        # Enviar o e-mail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, email, text)
        server.quit()

        print(f'Código de verificação enviado para {email}')
        return code

    except EmailNotValidError as e:
        print(str(e))
        return None

@app.route('/')
def index():
    return render_template('recuperar_senha.html')

@app.route('/recuperar', methods=['POST'])
def recuperar():
    data = request.form
    email = data.get('email')
    print(email)
    send_verification_code(email)
    return 'E-mail enviado! Verifique sua caixa de entrada.'

@app.route('/verificar', methods=['POST'])
def verificar():
    data = request.form
    code = data.get('code')
    print(code)
    return 'Código verificado com sucesso!'
if __name__ == '__main__':
    app.run(debug=True)
