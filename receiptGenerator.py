import csv
from datetime import date
from tkinter import *
from tkinter.filedialog import askopenfilename

# Constants
# fileName = "membershipdatabase.csv"
fileName = askopenfilename(title="Select membership CSV")
outputfileName = "misreport.csv"
membershipDict = {}
membershipDictNo = {}

def initializeDict():
    # Dictionaries holding values
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            MembershipNo = row[3]
            Contact = row[16]
            currentUser = {
                'MembershipNo': row[3],
                'Name': row[0] + " " + row[1] + " " + row[2],
                'Designation': row[5],
                'Organization': row[6],
                'Address': row[7] + " " + row[8] + ", " + row[10] + "- " + row[9],
                'email': row[12],
                'Contact': row[16],
                'tel': row[17],
                'Subrecdupto': row[18],
                'Subdue': row[19],
                'SubdueAmt': row[20]
            }
            membershipDict[MembershipNo] = currentUser
            membershipDictNo[Contact] = currentUser
    return membershipDict

def writetoCSV(dict):
    with open(outputfileName, 'a', encoding="utf-8-sig", newline='') as f:
        header = ['Date','Category','MembershipNo','Name','Designation','Organization', 'Address','OnAccountof','PaymentMode','Amount','Contact','Remarks']
        writer = csv.DictWriter(f, fieldnames = header, extrasaction='ignore')
        writer.writerow(dict)

def registerMember(currentDetails):

    def tempDest():
        thirdScreen.destroy()

    thirdScreen = Tk()
    thirdScreen.title("Dues")
    thirdScreen.geometry('480x480')
    Label(thirdScreen, text='Current Membership Number: ' + currentDetails['MembershipNo']).pack()
    Label(thirdScreen, text='Subscription received upto: ' + currentDetails['Subrecdupto']).pack()
    Label(thirdScreen, text='Subscription due for: ' + currentDetails['Subdue']).pack()
    Label(thirdScreen, text='Subscription due amount: ' + currentDetails['SubdueAmt']).pack()
    Button(thirdScreen, text="Okay", command= tempDest).pack()

    secondScreen = Tk()
    secondScreen.title("Personal details")
    secondScreen.geometry('480x480')
    frame = Frame(secondScreen)

    modex = StringVar()
    modex.set('Cash')
    oAcc = StringVar()
    oAcc.set('Subscription - 2020')

    def capturevalues():
        finalRow = {}
        finalRow['Date'] = date.today().strftime('%d-%m-%Y')
        finalRow['Category'] = "Member"
        finalRow['MembershipNo'] = str(currentDetails['MembershipNo'])
        finalRow['Name'] = name.get()
        finalRow['Designation'] = designation.get()
        finalRow['Organization'] = organization.get()
        finalRow['Address'] = address.get()
        finalRow['OnAccountof'] = oAcc.get()
        finalRow['PaymentMode'] = modex.get()
        finalRow['Amount'] = amount.get()
        finalRow['Contact'] = contact.get()
        finalRow['Remarks'] = remarks.get()
        print(finalRow)
        writetoCSV(finalRow)
        box = Tk()
        box.title("Successful")
        box.geometry("100x100")
        Label(box, text = "Registration successful").grid(row = 0, column = 0)
        Button(box, text="Okay", command= lambda: Tk.destroy(box)).grid(row = 1, column = 0)
        
        Tk.destroy(secondScreen)

    Label(frame, text='Name (<First><Last>): ').grid(row = 0, column = 0)
    name = Entry(frame)
    name.insert(0, currentDetails['Name'])
    name.grid(row = 0, column = 1)

    Label(frame, text='Designation: ').grid(row = 1, column = 0)
    designation = Entry(frame)
    designation.insert(0, currentDetails['Designation'])
    designation.grid(row = 1, column = 1)

    Label(frame, text='Organization: ').grid(row = 2, column = 0)
    organization = Entry(frame)
    organization.insert(0, currentDetails['Organization'])
    organization.grid(row = 2, column = 1)

    Label(frame, text='Address: ').grid(row = 3, column = 0)
    address = Entry(frame)
    address.insert(0, currentDetails['Address'])
    organization.grid(row = 3, column = 1)

    Label(frame, text='On account of: ').grid(row = 4, column = 0)
    onAccof = OptionMenu(frame, oAcc, "Subscription - 2020", "Subscription - 2021", "Subscription - 2022", "Subscription - 2023", "Subscription - 2024", "Reimbursements for Meals", "Reimbursements for Stay", "Subscription - 2022 with Initiation", "Other")
    onAccof.grid(row = 4, column = 1)

    Label(frame, text='Mode of payment: ').grid(row = 5, column = 0)
    o = OptionMenu(frame, modex, "NEFT", "Cash", "Cheque", "Card", "PayTM", "Other")
    o.grid(row = 5, column=1)
    # b1 = Radiobutton(frame, text='NEFT', command= lambda: modex.set('NEFT'))
    # b1.grid(row = 4, column = 1)
    # b2 = Radiobutton(frame, text='Cash', command= lambda: modex.set('Cash'))
    # b2.grid(row = 4, column = 2)
    # b3 = Radiobutton(frame, text='Cheque', command= lambda: modex.set('Cheque'))
    # b3.grid(row = 4, column = 3)
    # b4 = Radiobutton(frame, text='Card', command= lambda: modex.set('Card'))
    # b4.grid(row = 4, column = 4)

    Label(frame, text='Amount: ').grid(row = 6, column = 0)
    amount = Entry(frame)
    amount.grid(row = 6, column = 1)

    Label(frame, text='Contact: ').grid(row = 7, column = 0)
    contact = Entry(frame)
    contact.insert(0, currentDetails['Contact'])
    contact.grid(row = 7, column = 1)

    Label(frame, text='Remarks: ').grid(row = 8, column = 0)
    remarks = Entry(frame)
    remarks.grid(row = 8, column = 1)

    Button(frame, text="Submit", command= capturevalues).grid(row = 9, column = 0)
    Button(frame, text="Quit", command= secondScreen.destroy).grid(row = 9, column = 1)

    frame.pack(expand=1)
    secondScreen.mainloop()

def isMember():

    secondScreen = Tk()
    secondScreen.title("Extract")
    secondScreen.geometry('480x480')
    frame = Frame(secondScreen)

    modex = StringVar()
    modex.set(' ')

    def checkMemberMid():
        if mID.get() not in membershipDict:
            box1 = Tk()
            box1.title("Error")
            box1.geometry("300x100")
            Label(box1, text = "Membership ID not found. Please try again.").grid(row = 0, column = 0)
            Button(box1, text="Okay", command= lambda: Tk.destroy(box1)).grid(row = 1, column = 0)

        else:
            currentID = mID.get()
            Tk.destroy(secondScreen)
            registerMember(membershipDict[currentID])

    def checkMemberMNo():
        if mNo.get() not in membershipDictNo:
            box1 = Tk()
            box1.title("Error")
            box1.geometry("300x100")
            Label(box1, text = "Mob Number not found. Please try again.").grid(row = 0, column = 0)
            Button(box1, text="Okay", command= lambda: Tk.destroy(box1)).grid(row = 1, column = 0)

        else:
            currentID = mNo.get()
            Tk.destroy(secondScreen)
            registerMember(membershipDictNo[currentID])

    Label(frame, text="Membership ID: ").grid(row = 0, column = 0)
    mID = Entry(frame)
    mID.grid(row = 0, column = 1)
    Button(frame, text = 'Submit', command = checkMemberMid).grid(row = 0, column = 2)

    Label(frame, text="OR").grid(row=1, column=1)

    Label(frame, text="Mob No: ").grid(row = 2, column = 0)
    mNo = Entry(frame)
    mNo.grid(row = 2, column = 1)
    Button(frame, text = 'Submit', command = checkMemberMNo).grid(row = 2, column = 2)

    frame.pack(expand=1)
    secondScreen.mainloop()

def isNotMember():

    secondScreen = Tk()
    secondScreen.title("Personal details")
    secondScreen.geometry('480x480')
    frame = Frame(secondScreen)

    modex = StringVar()
    modex.set("Cash")
    oAcc = StringVar()
    oAcc.set("Subscription - 2020")

    def capturevalues():
        finalRow = {}
        finalRow['Date'] = date.today().strftime('%d-%m-%Y')
        finalRow['Category'] = "Non Member"
        finalRow['Membership No'] = "Non Member"
        finalRow['Name'] = name.get()
        finalRow['Designation'] = designation.get()
        finalRow['Organization'] = organization.get()
        finalRow['Address'] = address.get()
        finalRow['OnAccountof'] = oAcc.get()
        finalRow['Payment Mode'] = modex.get()
        finalRow['Amount'] = amount.get()
        finalRow['Contact'] = contact.get()
        finalRow['Remarks'] = remarks.get()
        print(finalRow)
        writetoCSV(finalRow)
        box = Tk()
        box.title("Successful")
        box.geometry("100x100")
        Label(box, text = "Registration successful").grid(row = 0, column = 0)
        Button(box, text="Okay", command= lambda: Tk.destroy(box)).grid(row = 1, column = 0)
        Tk.destroy(secondScreen)

    Label(frame, text='Name (<First><Last>): ').grid(row = 0, column = 0)
    name = Entry(frame)
    name.grid(row = 0, column = 1)

    Label(frame, text='Designation: ').grid(row = 1, column = 0)
    designation = Entry(frame)
    designation.grid(row = 1, column = 1)

    Label(frame, text='Address: ').grid(row = 2, column = 0)
    address = Entry(frame)
    address.grid(row = 2, column = 1)

    Label(frame, text='Organization: ').grid(row = 3, column = 0)
    organization = Entry(frame)
    organization.grid(row = 3, column = 1)

    Label(frame, text='On account of: ').grid(row = 4, column = 0)
    onAccof = OptionMenu(frame, oAcc, "Subscription - 2020", "Subscription - 2021", "Subscription - 2022", "Subscription - 2023", "Subscription - 2024", "Reimbursements for Meals", "Reimbursements for Stay", "Subscription - 2022 with Initiation", "Other")
    onAccof.grid(row = 4, column = 1)

    Label(frame, text='Mode of payment: ').grid(row = 5, column = 0)
    o = OptionMenu(frame, modex, "NEFT", "Cash", "Cheque", "Card", "PayTM", "Other")
    o.grid(row = 5, column=1)
    # b1 = Radiobutton(frame, text='NEFT', command= lambda: modex.set('NEFT'))
    # b1.grid(row = 4, column = 1)
    # b2 = Radiobutton(frame, text='Cash', command= lambda: modex.set('Cash'))
    # b2.grid(row = 4, column = 2)
    # b3 = Radiobutton(frame, text='Cheque', command= lambda: modex.set('Cheque'))
    # b3.grid(row = 4, column = 3)
    # b4 = Radiobutton(frame, text='Card', command= lambda: modex.set('Card'))
    # b4.grid(row = 4, column = 4)

    Label(frame, text='Amount: ').grid(row = 6, column = 0)
    amount = Entry(frame)
    amount.grid(row = 6, column = 1)

    Label(frame, text='Contact: ').grid(row = 7, column = 0)
    contact = Entry(frame)
    contact.grid(row = 7, column = 1)

    Label(frame, text='Remarks: ').grid(row = 8, column = 0)
    remarks = Entry(frame)
    remarks.grid(row = 8, column = 1)

    Button(frame, text="Submit", command= capturevalues).grid(row = 9, column = 0)
    Button(frame, text="Quit", command= secondScreen.destroy).grid(row = 9, column = 1)

    frame.pack(expand=1)
    secondScreen.mainloop()


if __name__ == "__main__":
    membershipDict = initializeDict()
    initial = Tk()
    initial.title("Welcome to the seminar")
    initial.geometry('300x300')
    newFrame = Frame(initial)
    Label(newFrame, text = "Are you a member?").grid(row = 0, column=1)
    Button(newFrame, text="Yes", command = isMember).grid(row = 2, column = 0)
    Button(newFrame, text="No", command = isNotMember).grid(row = 2, column = 2)
    Button(newFrame, text="Quit", command= initial.destroy).grid(row = 3, column = 1)
    newFrame.pack(expand=1)
    initial.mainloop()
