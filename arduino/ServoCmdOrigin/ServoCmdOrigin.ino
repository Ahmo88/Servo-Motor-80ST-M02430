
#include <ModbusMaster.h>

static uint32_t i;
uint8_t j, result;
uint16_t data[6];
boolean st = false;
int a = 0;
int x;
int parametar120 = 0;
int parametar121 = 0;
int parametar120stari = 0;
int parametar121stari = 0;

int limitPrekidac = 24;
int buttonPin = 2;
int buttonPinUp = 2;
int lampa = 13;
// instantiate ModbusMaster object
ModbusMaster node;
#include <CmdMessenger.h>
CmdMessenger cmdMessenger = CmdMessenger(Serial);
enum
{
  paljenjeServa,
  gasenjeServa,
  brzina1,
  brzina2,
  brzina3,
  manualBrzina,
  pozicija1,
  pozicija2,
  idi,
  buttonUp,
  homePozicija,
  parametar,
  parametar2,
  trenutnaPozicija,
  okidacTrenutnePozicije,
  trenutnaPozicija2,
  stani,

};
void attachCommandCallbacks()
{
  cmdMessenger.attach(paljenjeServa, paliServo);
  cmdMessenger.attach(gasenjeServa, ugasiServo);
  cmdMessenger.attach(brzina1, brzinaPrva);
  cmdMessenger.attach(brzina2, brzinaDruga);
  cmdMessenger.attach(brzina3, brzinaTreca);
  cmdMessenger.attach(manualBrzina, podesiBrzinu);
  cmdMessenger.attach(pozicija1, pozicijaPrva); // pozicija iz visuala poziva void u arduinu
  cmdMessenger.attach(pozicija2, pozicijaDruga);
  cmdMessenger.attach(idi, triger);
  cmdMessenger.attach(buttonUp, idiGore);
  cmdMessenger.attach(homePozicija, homeKreni);
  cmdMessenger.attach(parametar, parametar1);
  cmdMessenger.attach(parametar2, vrijednost);
  cmdMessenger.attach(trenutnaPozicija, Stop);
  cmdMessenger.attach(okidacTrenutnePozicije, trPozicija);
  cmdMessenger.attach(trenutnaPozicija2, Stop);
  cmdMessenger.attach(stani, Stop);
}

void setup()
{

  pinMode(limitPrekidac, INPUT);
  pinMode(buttonPin, INPUT);
  pinMode(buttonPinUp, INPUT);
  pinMode(lampa, OUTPUT);

  // use Serial (port 0); initialize Modbus communication baud rate
  Serial.begin(9600);
  Serial1.begin(9600, SERIAL_8N2);
  cmdMessenger.printLfCr();
  attachCommandCallbacks();

  // communicate with Modbus slave ID 2 over Serial (port 0)
  node.begin(2, Serial1); // Ime motora
}

void loop()
{

  cmdMessenger.feedinSerialData();

  /* if ( digitalRead (buttonPin) == LOW )  // za dugme
    {

  triger();
    }
   */

  if (digitalRead(limitPrekidac) == LOW) // za limit switch
  {

    result = node.writeSingleRegister(71, 255);
    delay(100);
    result = node.writeSingleRegister(36, 5);
    delay(100);
    result = node.writeSingleRegister(71, 191);
  }
}
void paliServo()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(33, 1);
  delay(100);
  result = node.writeSingleRegister(34, 4);
  delay(100);
  result = node.writeSingleRegister(35, 2);
  delay(100);
  result = node.writeSingleRegister(3, 1);
  result = node.writeSingleRegister(40, 10000);
  delay(100);
  result = node.writeSingleRegister(41, 10000);
  delay(100);
}

void ugasiServo()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(3, 0);
}

void brzinaPrva()
{
  cmdMessenger.feedinSerialData();
  delay(100);

  result = node.writeSingleRegister(38, 0);
  delay(100);
  result = node.writeSingleRegister(39, 300);
}

void brzinaDruga()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(38, 0);
  delay(100);
  result = node.writeSingleRegister(39, 1500);
}

void brzinaTreca()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(38, 0);
  delay(100);
  result = node.writeSingleRegister(39, 3000);
}

void podesiBrzinu()

{

  cmdMessenger.feedinSerialData();
  delay(100);
  a = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(38, a);
  delay(100);
  result = node.writeSingleRegister(39, a);
}

void pozicijaPrva()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  a = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(36, a);
}

void pozicijaDruga()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  a = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(37, a);
}
void homeKreni()

{
  cmdMessenger.feedinSerialData();
  delay(100);

  result = node.writeSingleRegister(38, 200);
  delay(100);
  result = node.writeSingleRegister(39, 200);
  delay(100);
  result = node.writeSingleRegister(36, -100);
  delay(100);
  result = node.writeSingleRegister(71, 255);
  delay(100);
  result = node.writeSingleRegister(71, 191);
}

void triger()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(71, 255);
  delay(100);
  result = node.writeSingleRegister(71, 191);
}

void idiGore()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(38, -100);
  delay(50);
}

void Stop()
{

  cmdMessenger.feedinSerialData();
  delay(100);
  result = node.writeSingleRegister(71, 255);
}
void parametar1()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  x = cmdMessenger.readInt32Arg();
}
void vrijednost()
{

  cmdMessenger.feedinSerialData();
  delay(100);
  int y;

  y = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(x, y);
}
void trPozicija()
{
  cmdMessenger.feedinSerialData();
  delay(100);
  int j = 0;
  int i = 0;

  result = node.readHoldingRegisters(387, 2);
  if (result == node.ku8MBSuccess)
  {

    j = node.getResponseBuffer(0); // low bit
    i = node.getResponseBuffer(1); // high bit
  }

  cmdMessenger.sendCmd(trenutnaPozicija, i);
  cmdMessenger.sendCmd(trenutnaPozicija2, j);
}
