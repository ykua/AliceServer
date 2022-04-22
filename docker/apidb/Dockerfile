FROM mysql:8.0

ENV MYSQL_DATABASE=alice_daq \
  MYSQL_USER=alice \
  MYSQL_PASSWORD=a1icedb% \
  MYSQL_ROOT_PASSWORD=a1icer00t% \
  TZ=Asia/Tokyo

COPY ./my.cnf /etc/mysql/conf.d/my.cnf
RUN chmod 644 /etc/mysql/conf.d/my.cnf