data = {
    "_id": {"$oid": "661374bdf382238bd186f8f8"},
    "email": "ajeshrandam@gmail.com",
    "biometric_data": {
        "face": [
            "student_face/ajeshrandam@gmail.com/image1.png",
            "student_face/ajeshrandam@gmail.com/image2.png",
            "student_face/ajeshrandam@gmail.com/image4.png",
            "student_face/ajeshrandam@gmail.com/image8.png",
        ],
        "Document": "student_document/ajeshrandam@gmail.com.pdf",
    },
    "dob": "2024-04-08",
    "gender": "female",
    "mobile": "9790887594",
    "name": {"first": "a", "last": "a", "middle": "a"},
    "password": None,
}


for i in data["biometric_data"]["face"]:
    print(i)
