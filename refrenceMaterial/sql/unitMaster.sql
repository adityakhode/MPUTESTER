--fthrth
;
CREATE TABLE IF NOT EXISTS "UnitMaster" (
  "PartNo"             INT,
  "PartName"       VARCHAR,
  "SingleDualOp"  SMALLINT,
  "Threading"      VARCHAR,
  "Lengths"       SMALLINT,
  "ThreadingGoNoGo"   CHAR,
  "NoLockNuts"    SMALLINT,
  "NutThickness"     FLOAT,
  "NutFlatAcross"    FLOAT,
  "PinProtrusion"    FLOAT,
  "CabelType"      VARCHAR,
  "CableLength"   SMALLINT,
  "Connector1"     VARCHAR,
  "Connector2"     VARCHAR,
  "UpperResistance"  FLOAT,
  "LowerResistance"  FLOAT,
  "UpperVoltage"     FLOAT,
  "LowerVoltage"     FLOAT,
  "UpperInductance"  FLOAT,
  "LowerInductance"  FLOAT,
  "FREQUENCY"        FLOAT
);
--dvgdraesgf
/*
INSERT INTO UnitMaster (PartNo, PartName, SingleDualOp, Threading, Length ,ThreadingGoNoGo, NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion, CabelType, CableLength, Connector1, Connector2, UpperResistance, LowerResistance, UpperVoltage, LowerVoltage, UpperInductance, LowerInductance, FREQUENCY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
*/
-- stored procedure
DELIMITER $$

CREATE PROCEDURE insertUnitMaster(
    IN PartNo              INT,
    IN PartName   VARCHAR(255),  -- Adjust size based on your requirements
    IN SingleDualOp   SMALLINT,
    IN Threading  VARCHAR(255),
    IN Lengths        SMALLINT,
    IN ThreadingGoNoGo CHAR(1),
    IN NoLockNuts     SMALLINT,
    IN NutThickness      FLOAT,
    IN NutFlatAcross     FLOAT,
    IN PinProtrusion     FLOAT,
    IN CabelType  VARCHAR(255),
    IN CableLength    SMALLINT,
    IN Connector1 VARCHAR(255),
    IN Connector2 VARCHAR(255),
    IN UpperResistance   FLOAT,
    IN LowerResistance   FLOAT,
    IN UpperVoltage      FLOAT,
    IN LowerVoltage      FLOAT,
    IN UpperInductance   FLOAT,
    IN LowerInductance   FLOAT,
    IN FREQUENCY         FLOAT
)
BEGIN
    INSERT INTO UnitMaster (
        PartNo, PartName, SingleDualOp, Threading, Lengths, ThreadingGoNoGo, 
        NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion, CabelType, 
        CableLength, Connector1, Connector2, UpperResistance, LowerResistance, 
        UpperVoltage, LowerVoltage, UpperInductance, LowerInductance, FREQUENCY
    ) 
    VALUES (
        PartNo, PartName, SingleDualOp, Threading, Lengths, ThreadingGoNoGo, 
        NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion, CabelType, 
        CableLength, Connector1, Connector2, UpperResistance, LowerResistance, 
        UpperVoltage, LowerVoltage, UpperInductance, LowerInductance, FREQUENCY
    );
END $$

DELIMITER ;
