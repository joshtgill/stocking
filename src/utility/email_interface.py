import os


class EmailInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface


    def sendEmail(self, address, subject, body):
        emailPath = 'out/email.txt'

        # Empty email.txt of existing data
        self.fileInterface.clearFile(emailPath)

        # Write contents of email in expected sendmail format
        emailFileText = 'Subject: {}'.format(subject)
        emailFileText += '\n'
        emailFileText += body
        self.fileInterface.write(emailPath, emailFileText)

        # Run linux command to send email
        sendMailCommand = 'sendmail {} < {}'.format(address, emailPath)
        os.system(sendMailCommand)
