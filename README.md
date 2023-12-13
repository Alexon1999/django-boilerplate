# Real Time Notification With Websocket

![wbesocket_workflow](./doc/assets/img/notification_system_workflow.png)

To achieve the real time communication with client and server, We use **django-channels** (websocket implementation).

### Usage of Websocket to get Notifications in Real time


```javascript

const socket = new WebSocket(
      "ws://localhost:8000/ws/notification/" +
        "?token=" +
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3MDMzMTg3LCJpYXQiOjE2OTcwMjk1ODcsImp0aSI6ImYzMDlmNGI1ZTM1ZTQxZGU5YjEzN2ZhNjg2OWQ1YjlkIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImdyb3VwcyI6W3siaWQiOjMsIm5hbWUiOiJBRE1JTiJ9XX0.3jvaqGEFhaMLTarG1QMNWTSuJ6vraZA14qcitHx5apU"
    );

socket.onmessage = function (event) {
  console.log(event.data); // string
  console.log(JSON.parse(event.data)); // object
};

// on logout, close the websocket
// socket.close();
```