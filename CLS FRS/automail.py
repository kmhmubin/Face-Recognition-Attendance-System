import yagmail

receiver = "yourgmail.com"  # receiver email address
body = "Attendence File"  # email body
filename = "Attendance\Attendance_2019-08-16_01-06-17.csv"  # attach the file

#mail information
yag = yagmail.SMTP("yourgmail.com", "yourpass")

#sent the mail
yag.send(
    to=receiver,
    subject="Yagmail test with attachment",  # email subject
    contents=body,
    attachments=filename,
)

