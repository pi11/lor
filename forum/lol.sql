select user_id from forum_message
                         where date_part('year', publication_date at time zone 'Europe/Moscow') = 2014
                         and date_part('month', publication_date at time zone 'Europe/Moscow') = 1
group by user_id having count(*) > 10;
