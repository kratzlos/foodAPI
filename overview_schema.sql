create table overview (
  id integer primary key autoincrement,
  date text not null,
  day_number text not null,
  day text not null,
  breakfast_meal text not null,
  breakfast_loc text not null,
  lunch_meal text not null,
  lunch_loc text not null,
  dinner_meal text not null,
  dinner_loc text not null,
  cal_total real not null,
  carb_perc real not null,
  protein_perc real not null,
  fat_perc real not null
);