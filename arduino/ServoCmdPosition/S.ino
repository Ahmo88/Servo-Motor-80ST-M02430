 /*  cmdMessenger.feedinSerialData();    // OVAJ KOD JE  ZA DUGME AKO HOCU DA IDE UVIJEK NA NULU SA BILO KOJE POZICIJE
    delay(50);
    int j = 0;
    int i = 0;

    result = node.readHoldingRegisters(387, 2);
    if (result == node.ku8MBSuccess)
    {

      j = node.getResponseBuffer(0); //low bit
      i = node.getResponseBuffer(1); //high bit
    }

    cmdMessenger.sendCmd(trenutnaPozicija, i);
    cmdMessenger.sendCmd(trenutnaPozicija2, j);

    if ( digitalRead (buttonPin) == LOW )

    {
    result = node.writeSingleRegister(120, -i);
    delay(50);
    result = node.writeSingleRegister(121, -j);
    delay(250);
    triger();
  */
