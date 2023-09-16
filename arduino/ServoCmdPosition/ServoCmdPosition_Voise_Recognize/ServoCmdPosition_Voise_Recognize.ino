
#include <ModbusMaster.h>

byte com = 0; //reply from voice recognition 

static uint32_t i;
uint8_t j, result;
uint16_t data[6];
boolean st = false;
int a = 0;
int b = 0;
int x;


int limitPrekidac = 24;
int buttonPin = 2;
int buttonGore = 3;
 
int lampa = 13;
boolean prosloStanje=false;

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
  cmdMessenger.attach(gasenjeServa,ugasiServo);
  cmdMessenger.attach(brzina1, brzinaPrva);
  cmdMessenger.attach(brzina2, brzinaDruga);
  cmdMessenger.attach(brzina3, brzinaTreca);
  cmdMessenger.attach(manualBrzina,podesiBrzinu); 
  cmdMessenger.attach(pozicija1, pozicijaPrva); // pozicija iz visuala poziva void u arduinu
  cmdMessenger.attach(pozicija2, pozicijaDruga); 
  cmdMessenger.attach(homePozicija, homeKreni);
  cmdMessenger.attach(idi, triger);  
  cmdMessenger.attach(parametar, parametar1);
  cmdMessenger.attach(parametar2, vrijednost);
  cmdMessenger.attach(okidacTrenutnePozicije,trPozicija);
  cmdMessenger.attach(stani,Stop);
}


void setup()
{
// vezano za voice recognition
delay(1000);
Serial2.write(0xAA);
Serial2.write(0x37);
delay(1000);
Serial2.write(0xAA);
Serial2.write(0x21);
  
  
  pinMode(limitPrekidac, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonGore, INPUT);
  pinMode(lampa, OUTPUT);
 
  // use Serial (port 0); initialize Modbus communication baud rate
  Serial2.begin(9600);
  Serial1.begin(9600, SERIAL_8N2);
  cmdMessenger.printLfCr();
  attachCommandCallbacks();

  // communicate with Modbus slave ID 2 over Serial (port 0)
  node.begin(2, Serial1);  // Ime motora

}

void loop()
{

 int j = 0;
 int i =0;
 delay (100);
 result = node.readHoldingRegisters(387,2);
 
 if (result == node.ku8MBSuccess)
  { 
    j= node.getResponseBuffer(0); //low bit
    i= node.getResponseBuffer(1); //high bit
  }
  
 cmdMessenger.sendCmd(trenutnaPozicija,i);
 cmdMessenger.sendCmd(trenutnaPozicija2,j); 
 cmdMessenger.feedinSerialData();
 delay(50);

if ( digitalRead (buttonGore) ==  LOW )  // za dugme
 {   
  prosloStanje=true;
  result = node.writeSingleRegister(120, -100);
  delay(50);
  result = node.writeSingleRegister(71, 4095);
  delay(50);
  result = node.writeSingleRegister(71, 3071);  
 }
  else
  if (prosloStanje == true)
  {
 
  result = node.writeSingleRegister(71, 2047);
  prosloStanje = false;   

}
   
 if (digitalRead (limitPrekidac)== LOW)  // za limit switch
{

result = node.writeSingleRegister(3, 0);
delay (50);
result = node.writeSingleRegister(3, 1);



}

  if ( digitalRead (buttonPin) ==  LOW )
  {
    triger();
    }
while(Serial2.available())
{
com = Serial2.parseInt();


switch(com)
{
case 11:

digitalWrite(lampa, HIGH);
Serial2.println("krkan");

break;

case 12:
digitalWrite(lampa, LOW);
Serial2.println("krkan2");
break;

case 13:

Serial2.print ("Ahmo i Sabit ce sad igrat kantera");

}
}












}
void paliServo()
{
cmdMessenger.feedinSerialData();
  delay(50);
result = node.writeSingleRegister(3, 1);

}

void ugasiServo()
{

cmdMessenger.feedinSerialData();
delay(50);
result = node.writeSingleRegister(3, 0);
delay(50);
result = node.writeSingleRegister(8, 300);
delay(50);
result = node.writeSingleRegister(9, -300);
  
}

void brzinaPrva()
{
 cmdMessenger.feedinSerialData();
  delay(50);
  result = node.writeSingleRegister(128, 300);
 
}

void brzinaDruga()
{
  cmdMessenger.feedinSerialData();
  delay(50);
  result = node.writeSingleRegister(128, 1500);
  
}
void brzinaTreca()
{
cmdMessenger.feedinSerialData();
  delay(50);
   result = node.writeSingleRegister(128, 3000);
  
}

void podesiBrzinu()

{
  cmdMessenger.feedinSerialData();
  delay(50);
   
   a = cmdMessenger.readInt32Arg();
 
  result = node.writeSingleRegister(128, a);
  
  }

void pozicijaPrva()  // manji broj krugova registar 120
{
cmdMessenger.feedinSerialData();
  delay(50);
  a = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(120, a); 
   delay(50);

}

void pozicijaDruga()  // veci broj krugova registar 121
{
cmdMessenger.feedinSerialData();
  delay(50);
  a = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(121, a); 
   

}

void homeKreni()

{
  cmdMessenger.feedinSerialData();
  delay(50);
  
  result = node.writeSingleRegister(9, -10);
  delay(50);
  result = node.writeSingleRegister(120, -100);
  delay(50);
  result = node.writeSingleRegister(71, 4095);
  delay(50);
  result = node.writeSingleRegister(71, 3071);
  
}

void triger()
{
  cmdMessenger.feedinSerialData();
  delay(50);
  result = node.writeSingleRegister(71, 4095);
  delay(50);
  result = node.writeSingleRegister(71, 3071);
  
}

void Stop()
{
  cmdMessenger.feedinSerialData();
  delay(50);
 
  result = node.writeSingleRegister(71, 2047);
  
}
void parametar1()
{
cmdMessenger.feedinSerialData();
  delay(50);
  x = cmdMessenger.readInt32Arg();


}
void vrijednost()
{
 cmdMessenger.feedinSerialData();
  delay(50);
  
  int y;

  y = cmdMessenger.readInt32Arg();
  result = node.writeSingleRegister(x, y);
}
void trPozicija()
{
 
}

