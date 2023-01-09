import smtplib
from string import Template
import imghdr
from email.message import EmailMessage
from gizli import mailAdresim, sifre
from konu import mailKonusu



def alici(filename):
    """
    İletişime geçilecek insanların isim soyisim ve mail adreslerinin bulunduğu liste verilerek databasedeki
    bilgileri ayırıp sonrasında elde edilen isim bilgisi iletişime geçilecek kişiye özel mail gönderilmesini
    kolaylaştıran fonkiyon.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def mesaj(filename):
    """
    Message.txt dosyasında yer alan mesajımızı objeye çeviren fonksiyon.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    names, emails = alici(r"")  # Mycontact listesinin dosya yolunu yazınız.
    message_template = mesaj(r"")  # Göndereceğiniz mesaj dosayası(message.txt'nin) dosya yolunu yazınız.

    # SMTP Sunucusun konfigürasyon ayarları.
    smtpSunucu = smtplib.SMTP(host='smtp.gmail.com', port=587)  # 25, 465, 587 portları kullanılabilir.
    smtpSunucu.starttls() # Transport Layer Security, smtp serverla güvenli bağlantı oluşturmamızı sağlayan kod.
    smtpSunucu.login(mailAdresim, sifre) #gizli.py dosyasındaki kullanıcı adı ve şifre bilgilerimizi kullanarak login olmamızı sağlayan kod.

    # alıcı listesindeki kişi ve isim bilgilerini çeken for döngüsü:
    for name, email in zip(names, emails):
        msg = EmailMessage()

        # Mesaj şablonuna iletişim listesinden isim bilgisini çeken kod satırı.
        message = message_template.substitute(PERSON_NAME= name.title())


        # Maili atmadan önce bizim için ekrana yazdıran kod satırı.
        print(message)

        # Mailin parametreleri; kime gideceği, kimdein gideceği, mail konusu.
        msg['From'] = mailAdresim
        msg['To'] = email
        msg['Subject'] = mailKonusu

        # gönderilecek maile içerik kısmını ekleyen kod satırı.
        #msg.attach(MIMEText(message, 'plain'))

        msg.set_content(message, "plain")

        files = [''] # Attachment olarak ekleyeceğiniz dosyanın ismi. (dosya ismini eklemeden önce main.py ile aynı dizinde olduğundan emin olunuz.)
        for file in files:
            with open(file, 'rb') as f:
                image_data = f.read()
                image_type = imghdr.what(f.name)
                image_name = f.name
            msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        # mesajı smtp server aracılığıyla gönderen kod satırı.
        smtpSunucu.send_message(msg)
        del msg

    # Mail gönderildikten sonra SMTP bağlantısını sonlandıran kod satırı.
    smtpSunucu.quit()


if __name__ == '__main__':
    main()