#include "WiFi.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <Wire.h>
#include <Adafruit_BMP085.h>

#define BlueLed            2
#define Rele1              4
#define Rele2              15

#define WLAN_SSID       ""             // Your SSID
#define WLAN_PASS       ""        // Your password

Adafruit_BMP085 bmp;

/************************* Adafruit.io Setup *********************************/

#define AIO_SERVER      "io.adafruit.com" //Adafruit Server
#define AIO_SERVERPORT  1883                   
#define AIO_USERNAME 	"" 
#define AIO_KEY       ""

//WIFI CLIENT
WiFiClient client;

Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

Adafruit_MQTT_Subscribe Rele = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/Rele"); // Crie aqui sua variavel
Adafruit_MQTT_Subscribe Light = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/Light"); // a palavra feeds deve estar em todos
Adafruit_MQTT_Publish temperature = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Temp");


void MQTT_connect();

void setup() {
  Serial.begin(115200);

  pinMode(Rele1, OUTPUT);
  pinMode(BlueLed, OUTPUT);
  pinMode(Rele2, OUTPUT);

  if (!bmp.begin()) {
  Serial.println("Could not find a valid BMP085/BMP180 sensor, check wiring!");
  while (1) {}
  }
  
  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); 
  Serial.println(WiFi.localIP());
 
  mqtt.subscribe(&Rele);
  mqtt.subscribe(&Light);
}

void loop() {

 
  MQTT_connect();
  
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(20000))) {
    if (subscription == &Rele) {
      Serial.print(F("Got: "));
      Serial.println((char *)Rele.lastread);
      int Rele_State = atoi((char *)Rele.lastread);
      digitalWrite(Rele1, Rele_State);
      digitalWrite(BlueLed, Rele_State);
    }
    if (subscription == &Light) {
      Serial.print(F("Got: "));
      Serial.println((char *)Light.lastread);
      int Light_State = atoi((char *)Light.lastread);
      digitalWrite(Rele2, Light_State);
    }
  }
  
  if (!temperature.publish(bmp.readTemperature())) {
    Serial.println(F("Failed"));
  }
  else {
    Serial.println(F("OK!"));
  }
}

void MQTT_connect() {
  int8_t ret;

  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000); 
    retries--;
    if (retries == 0) {
      while (1);
    }
  }
  Serial.println("MQTT Connected!");
}
