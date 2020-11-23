create index CONCURRENTLY lor_forum_date on forum_message 
       (date_part('year', publication_date at time zone 'Europe/Moscow'),
       date_part('month', publication_date at time zone 'Europe/Moscow'),		 
       date_part('day', publication_date at time zone 'Europe/Moscow'));