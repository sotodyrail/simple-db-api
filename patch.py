import requests
patient_url = 'http://64.227.121.66:8080/patient/'
mark_url = 'http://64.227.121.66:8080/mark/'

#Создание пациента
patient = {
    "data": {
        "attributes": {
            "birth_date": "1965-10-02",
            "contact_phone": "89000011123",
            "date_hospitalization": "2021-01-05",
            "discharged": False,
            "medical_policy": "121234522",
            "p_name": "АНАЛЬНЫЙ",
            "p_patronymic": "Алексеевич",
            "p_surname": "Безруков",
            "type_hospitalization": "Плановая"
        },
        "type": "Patient"
    }
}
result = requests.post(patient_url, json=patient)
patient_id = result.json()['data']['id']

#Создание отметки
mark = {
  "data": {
    "attributes": {
      "identifier": patient_id,
      "switch": False,
      "patient_id": int(patient_id)
    },
    "type": "Mark"
  }
}
result = requests.post(mark_url, json=mark)
mark_id = result.json()['data']['id']

#Удаление отметки и пациента
requests.delete('{url}/{id}'.format(url=mark_url, id=mark_id))
requests.delete('{url}/{id}'.format(url=patient_url, id=patient_id))


