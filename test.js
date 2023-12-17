
import { connect } from 'mqtt';

const mqttClient = connect('mqtt://broker.emqx.io');
const mqttTopic = "Hust/htn/test/esp"

mqttClient.on('connect', () => {
  console.log('Connected to MQTT broker!');
  mqttClient.subscribe(mqttTopic, (err) => {
    if (err) {
      console.log(err);
    }
  });
});

function pushMessage(topic, message) {
  mqttClient.publish(topic, message, (err) => {
    if (err) {
      console.error('Gửi tin nhắn thất bại', err);
    } else {
      console.log(`Đã gửi tin nhắn "${message}" lên chủ đề "${topic}"`);
    }

  });
}
pushMessage("Hust/htn/test", "tien su may")
console.log("pushed");