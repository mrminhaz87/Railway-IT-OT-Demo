DROP TABLE IF EXISTS sensorsState;
DROP TABLE IF EXISTS signalState;

CREATE TABLE sensorsState (
    evtId INTEGER PRIMARY KEY NOT NULL,
    sensorTrack TEXT,
    updateT TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
    sensorData TEXT,
);

CREATE TABLE signalState (
    evtId INTEGER PRIMARY KEY NOT NULL,
    signalTrack TEXT,
    updateT TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
    signalData TEXT,
);

