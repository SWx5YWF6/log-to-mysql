CREATE TABLE log.ssh (
          id INT AUTO_INCREMENT,
          time DATETIME NOT NULL,
          username VARCHAR(100),
          srcIp VARCHAR(45),
          srcIpType VARCHAR(4), 
          srcCountry VARCHAR(2),
          dstServer VARCHAR(4),
          dstCountry VARCHAR(2),
          PRIMARY KEY(id)
);
