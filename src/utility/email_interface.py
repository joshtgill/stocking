class EmailInterface:

    def __init__(self, dataInterface, fileInterface):
        self.dataInterface = dataInterface
        self.fileInterface = fileInterface


    def buildEmail(self, subject, body):
        # Clear email.txt of existing data
        self.fileInterface.wipe(self.dataInterface.settingsGet('stockingEmailPath'))

        # Build email in sendmail format
        emailFileText = 'Subject: {}'.format(subject)
        emailFileText += '\n\n'
        emailFileText += body

        # Write to email file
        self.fileInterface.write(self.dataInterface.settingsGet('stockingEmailPath'), emailFileText)
