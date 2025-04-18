import config

def replace_sensitive_info():
    with open('index.html', 'r') as file:
        content = file.read()
    
    content = content.replace('[PHONE_NUMBER]', config.CONTACT_INFO['phone'])
    content = content.replace('[EMAIL_ADDRESS]', config.CONTACT_INFO['email'])
    
    with open('index.html', 'w') as file:
        file.write(content)

if __name__ == '__main__':
    replace_sensitive_info() 