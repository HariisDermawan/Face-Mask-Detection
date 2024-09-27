#define ledHijau 2
#define ledMerah 3
#define buzzer 4

int volume = 128;  // Nilai volume dari 0 (paling kecil) hingga 255 (paling besar)

void setup() {
  // Inisialisasi pin sebagai OUTPUT
  pinMode(ledHijau, OUTPUT);
  pinMode(ledMerah, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  // Inisialisasi komunikasi serial
  Serial.begin(9600);
}

void loop() {
  // Jika ada data serial yang diterima
  if (Serial.available() > 0) {
    char data = Serial.read();  // Membaca data yang dikirim dari Python
    
    if (data == '1') {
      // Masker terdeteksi
      digitalWrite(ledHijau, HIGH);  // LED hijau ON
      analogWrite(buzzer, volume);   // Buzzer ON dengan volume yang diatur
      delay(100);                    // Buzzer aktif selama 100 ms
      analogWrite(buzzer, 5);        // Buzzer OFF
      digitalWrite(ledHijau, LOW);   // LED hijau OFF
    } 
    else if (data == '2') {
      // Masker tidak terdeteksi
      digitalWrite(ledMerah, HIGH);  // LED merah ON
      analogWrite(buzzer, volume);   // Buzzer ON dengan volume yang diatur
      delay(100);                    // Buzzer aktif selama 100 ms
      analogWrite(buzzer, 5);        // Buzzer OFF
      digitalWrite(ledMerah, LOW);   // LED merah OFF
    } 
    else if (data == '+') {
      // Meningkatkan volume (maksimal 255)
      if (volume < 255) {
        volume += 25;
      }
      Serial.print("Volume: ");
      Serial.println(volume);
    } 
    else if (data == '-') {
      // Menurunkan volume (minimal 0)
      if (volume > 0) {
        volume -= 25;
      }
      Serial.print("Volume: ");
      Serial.println(volume);
    }
  }
}
