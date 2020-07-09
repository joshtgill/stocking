class EmailInterface:

    def __init__(self, configInterface, fileInterface):
        self.configInterface = configInterface
        self.fileInterface = fileInterface


    def buildEmail(self, subject, body):
        # Clear email.txt of existing data
        self.fileInterface.wipe(self.configInterface.settingsGet('stockingEmailPath'))

        # Build email in sendmail format
        emailFileText = 'Subject: {}'.format(subject)
        emailFileText += '\n\n'
        emailFileText += body

        # Write to email file
        self.fileInterface.write(self.configInterface.settingsGet('stockingEmailPath'), emailFileText)
