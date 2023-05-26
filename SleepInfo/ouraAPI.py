import requests
activity = 'https://api.ouraring.com/v2/usercollection/daily_activity'
sleep = 'https://api.ouraring.com/v1/sleep?start=YYYY-MM-DD&end=YYYY-MM-DD'
hr = 'https://api.ouraring.com/v2/usercollection/heartrate'
readiness ='https://api.ouraring.com/v1/sleep?start=2022-08-01&end=2022-08-02'


params={
    'start_date': '2022-07-01',
    'end_date': '2022-08-01'
}
headers = {
  'Authorization': 'Bearer 4SRRVIKPASRJX73BV42NBCFTWGNMX45W'
}
response = requests.request('GET', sleep, headers=headers, params=params)
print(response.text)