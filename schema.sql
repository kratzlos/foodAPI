create table foods (
  id integer primary key autoincrement,
  name text not null,
  amount integer not null,
  measure text not null,
  energy integer not null,
  carbs real,
  sugar real,
  protein real,
  fat real,
  description text
);