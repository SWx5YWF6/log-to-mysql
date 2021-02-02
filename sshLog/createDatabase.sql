CREATE TABLE log.ssh (
  id INT AUTO_INCREMENT,
  time DATETIME NOT NULL,
  username VARCHAR(100),
  srcIp VARCHAR(15),
  country VARCHAR(2),
  PRIMARY KEY(id)
);