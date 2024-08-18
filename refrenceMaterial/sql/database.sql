CREATE TABLE `Party Master` (
  `SupplierCode` CHAR,
  `PartyName` VARCHAR,
  `PartyAddress` VARCHAR
);

CREATE TABLE `Unit Master` (
  `PartNo` INT,
  `PartName` VARCHAR,
  `SingleDualOp` SMALLINT,
  `Threading` VARCHAR,
  `Length` SMALLINT,
  `ThreadingGoNoGo` CHAR,
  `NoLockNuts` SMALLINT,
  `NutThickness` FLOAT,
  `NutFlatAcross` FLOAT,
  `PinProtrusion` FLOAT,
  `CabelType` VARCHAR,
  `CableLength` SMALLINT,
  `Connector1` VARCHAR,
  `Connector2` VARCHAR,
  `UpperResistance` FLOAT,
  `LowerResistance` FLOAT,
  `UpperVoltage` FLOAT,
  `LowerVoltage` FLOAT,
  `UpperInductance` FLOAT,
  `LowerInductance` FLOAT,
  `FREQUENCY` FLOAT
);

CREATE TABLE `Party 1` (
  `TcNo` VARCHAR,
  `TcDate` VARCHAR,
  `PartNo` INTEGER,
  `PartName` CHAR,
  `PartyName` VARCHAR,
  `SupplierCode` CHAR,
  `BatchNo` CHAR,
  `ChallanQuantity` SMALLINT,
  `ChallanDate` DATE,
  `Resistance1Value` FLOAT,
  `Resistance1Status` FLOAT,
  `Resistance2Value` FLOAT,
  `Resistance2Status` FLOAT,
  `Inductance1Value` FLOAT,
  `Inductance1Status` FLOAT,
  `Inductance2Value` FLOAT,
  `Inductance2Status` FLOAT,
  `Frequency1Value` FLOAT,
  `Frequency2Value` FLOAT,
  `Voltage1NoLoadValue` FLOAT,
  `Voltage1NoLoadStatus` FLOAT,
  `Voltage2NoLoadValue` FLOAT,
  `Voltage2NoLoadStatus` FLOAT,
  `Voltage1-10kLoadValue` FLOAT,
  `Voltage1-10kLoadStatus` FLOAT,
  `Voltage2-10kLoadValue` FLOAT,
  `Voltage2-10kLoadStatus` FLOAT,
  `Voltage1-3k3LoadValue` FLOAT,
  `Voltage1-3k3LoadStatus` FLOAT,
  `Voltage2-3k3LoadValue` FLOAT,
  `Voltage2-3k3Loadstatus` FLOAT,
  FOREIGN KEY (`PartyName`) REFERENCES `Party Master`(`PartyName`),
  FOREIGN KEY (`PartNo`) REFERENCES `Unit Master`(`PartNo`),
  FOREIGN KEY (`PartName`) REFERENCES `Unit Master`(`PartName`),
  FOREIGN KEY (`SupplierCode`) REFERENCES `Party Master`(`SupplierCode`)
);


