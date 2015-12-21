CREATE TABLE notifications (key number primary key, value string);
CREATE TABLE configuration (key string primary key, value string);
insert or replace into configuration (key, value) values ('locked','TRUE');
insert or replace into configuration (key, value) values ('android','FALSE');
insert or replace into configuration (key, value) values ('pre-lollipop','FALSE');
insert or replace into configuration (key, value) values ('bluetooth','');
