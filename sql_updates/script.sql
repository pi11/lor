insert into forum_lsmessage (user_id, avglen)  
(select user_id, sum(length(b.text))/count(*) as l  from forum_message a, forum_messagestore b where a.id=b.ms_id  group by user_id 
 having count(*)>500 order by l asc limit 100);


insert into forum_lsmessage (user_id, avglen)  
(select user_id, sum(length(b.text))/count(*) as l  from forum_message a, forum_messagestore b where a.id=b.ms_id  group by user_id 
 having count(*)>500 order by l desc limit 100);
