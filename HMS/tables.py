from flask_table import Table, Col

class TotalRoomReport(Table):
    classes = ["table", "table-striped"]
    thead_classes = ["thead-dark"]
    room_num = Col('Room Number')
    beds = Col('Number of Beds')
    price = Col("Price")

class TotalStudentsReport(Table):
    classes = ["table", "table-striped"]
    thead_classes = ["thead-dark"]
    firstname = Col('FName')
    lastname = Col('LName')
    email = Col('Email')
    number = Col('Phone No')
    gender = Col('Gender')
    room_id = Col('Room No')
