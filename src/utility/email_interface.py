class EmailInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.emailPath = 'out/email.txt'


    def buildEmail(self, subject, body):
        # Clear email.txt of existing data
        self.fileInterface.clearFile(self.emailPath)

        # Build email in sendmail format
        emailFileText = 'Subject: {}'.format(subject)
        emailFileText += '\n\n'
        emailFileText += body

        # Write to email file
        self.fileInterface.write(self.emailPath, emailFileText)
