# queries.py

INSERT_URL_QUERY = """UPDATE User_Information SET URL = ? WHERE UserId = ?"""
GET_TASK_QUERY = """SELECT ti.*, ui.Email FROM Task_Information as ti
                             INNER JOIN User_Information as ui on ti.UserId = ui.UserId
                                 WHERE ti.UserId = ? AND ti.IsEmailSend = 0"""
INSERT_TASK_QUERY = """INSERT INTO Task_Information (UserId, Title, Summary, Published, Link) VALUES (?, ?, ?, ?, ?)"""
UPDATE_TASK_QUERY = """UPDATE Task_Information SET IsEmailSend = 1 WHERE Id = ? AND UserId = ?"""
CHECK_QUERY = """SELECT * FROM Task_Information WHERE UserId = ? AND Title = ? AND Published = ? AND Link = ?"""
SUBSCRIPTION_QUERY = """SELECT ui.IsSubscribed, si.SubscriptionStartDate, si.SubscriptionEndDate, ui.URL 
                            FROM User_Information as ui
                             INNER JOIN Subscription_Information as si on ui.UserId = si.UserId WHERE ui.UserId = ?"""
USER_QUERY = """SELECT * FROM User_Information WHERE UserId = ?"""


# database.py
CONNECTION_STRING = (
    "DRIVER={SQL Server}; SERVER=L3T2167; DATABASE=BoosterPro; Trusted_Connection=yes; uid=sa; pwd=Admin0011##")

