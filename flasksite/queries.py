#query naming convention is function name underscore descriptive name, e.g. q_home_total_members


#queries for home
home_total_members = """select
                        round(
                          (count(phone_number)
                          +
                          (select count(*) from mailchimp_sub ))
                          *.905) as total
                        from
                        mobile_users
                        where status = 'Active Subscriber' """

home_net_members_daily = "select date as x, net as y from list_tracking"

home_gross_mobile_new_members = "select date as x, mobile_created as y from list_tracking"

home_gross_mail_new_members = "select date as x, mail_created as y from list_tracking"

home_gross_mobile_optedout_members = "select date as x, mobile_opt_out as y from list_tracking"

home_gross_mail_optedout_members = "select date as x, mail_opt_out as y from list_tracking"


#getCausesdata

getCausesdata_causes = """
  select 'Sex+Relationships' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Sex',"Relationships")
  union all
  select 'Homelessness+Poverty' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Homelessness',"Poverty")
  union all
  select 'Bullying+Violence' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Bullying',"Violence")
  union all
  select 'Mental Health+Physical Health' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Mental Health',"Physical Health")
  union all
  select cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause not in ('Bullying',"Violence",'Mental Health',"Physical Health",'Homelessness',"Poverty",'Sex',"Relationships") group by cause
  """
#causeStaffPicks

causeStaffPicks_formatted_causes = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" and cause in (%s) and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc'

causeStaffPicks_causes = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" order by sign_ups desc'

#monthly

monthly_stats = 'select date_format(date, "%M %Y") as date, new_members_last_12_percent as new, engaged_members_last_12_percent as engaged, active_members_last_12_percent as active, verified_members_last_12_percent as verified from members.bod_2014 order by date_format(date, "%Y-%m-%d")'

#getSpecificCampaign

getSpecificCampaign_campaign_info = 'select is_sms, staff_pick from {0}.campaign_info'

getSpecificCampaign_overall = "select sign_ups, new_members, report_backs, all_traffic, average_daily_traffic, concat(round(avg_gate_conversion*100,2),'%') as average_gate_conversion from overall.overall where campaign = '{0}' "

getSpecificCampaign_staff_sign_up = """
  select w.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w left join {0}.mobile_sign_ups m on w.date=m.date
  union
  select m.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w right join {0}.mobile_sign_ups m on w.date=m.date
  order by date
  """

getSpecificCampaign_staff_new_members = """
  select w.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w left join {0}.mobile_new_members m on w.date=m.date
  union
  select m.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w right join {0}.mobile_new_members m on w.date=m.date
  order by date
  """

getSpecificCampaign_nonstaff_sign_up = "select date, web_sign_ups as web from {0}.web_sign_ups"

getSpecificCampaign_nonstaff_new_members = "select date, web_new_members as web from {0}.web_new_members"

getSpecificCampaign_staff_sources = "select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 500  )"

getSpecificCampaign_nonstaff_sources = "select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 50  )"

getSpecificCampaign_traffic_regular = "select t.date, t.unq_visits, ifnull(s.web_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_sign_ups s on t.date=s.date"

getSpecificCampaign_traffic_sms = "select t.date, t.unq_visits, ifnull(a.alpha_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_alphas a on t.date=a.date"

kpisActive = "select date as x, average_active as y, days_in_month from active_by_month order by date"

kpisVerifiedAll_S = "select date as x, average_verified_sms as y, days_in_month from verified_by_month order by date"

kpisVerifiedAll_W = "select date as x, average_verified_web as y, days_in_month from verified_by_month order by date"

kpisNew = "select date as x, average_new as y, days_in_month from new_by_month order by date"

kpiText = """select k.box_id, replace(replace(all_text, '|', "'"),'%^&','"') as all_text from dashboards.kpi_content k
          join ( select box_id, max(timestamp) as timestamp from dashboards.kpi_content group by box_id ) t
          on k.box_id=t.box_id and k.timestamp=t.timestamp
          group by box_id"""

kpiTextInsert = "insert into dashboards.kpi_content (timestamp, all_text, box_id) values ('%s','%s', '%s')"

# campaign metadata endpoint query
campaignDataEnpoint_basic_campaign_metadata = "select campaign, sign_ups, new_members, report_backs, all_traffic, start_date, end_date  from overall.overall where nid = %d"

list_all_campaigns = "select  title from users_and_activities.campaign_master where title not in ('hgfdjhvj,bkh.', 'Tag Your Friends', 'XYZ Factor Test', 'A/B Test File Hosting Campaign', 'Birthday Mail (Fake)', 'Chai Impact', 'Bully Text Dummy Campaign') order by title"

list_one_campaign = """select c.nid, title, alias, status, group_concat(m.campaign_id) as mobile_ids,
                        case
                        when m.campaign_id = 0 or m.campaign_id is null
                        then 0
                        else 1
                        end as has_mobile,
                        case
                        when s.campaign_id = 0 or s.campaign_id is null
                        then 0
                        else 1
                        end as is_sms
                        from users_and_activities.campaign_master c left join users_and_activities.mobile_campaign_ids m on c.nid=m.nid left join user_processing.sms_games s on m.campaign_id=s.campaign_id where title = "{0}" group by c.nid"""

new_sign_ups_new = """select date_format(from_unixtime(timestamp), '%Y-%m-%d') as date, ifnull(count(uid),0) as web, ifnull(phones,0) as mobile
                  from dosomething.dosomething_signup w
                  left join
                  (select date_format(activated_at, '%Y-%m-%d') as date, count(phone_number) as phones
                  from users_and_activities.mobile_subscriptions
                  where campaign_id in ( {0}) and been_alpha = 0 and first_seen_campaign = 1 and date_format(activated_at, '%Y-%m-%d') >= "{2}" and date_format(activated_at, '%Y-%m-%d') <= "{3}"
                  group by date_format(activated_at, '%Y-%m-%d')) m
                  on date_format(from_unixtime(timestamp), '%Y-%m-%d')=m.date
                  where nid = {1} and from_unixtime(timestamp, '%Y-%m-%d') >= "{2}" and from_unixtime(timestamp, '%Y-%m-%d') <= "{3}"
                  group by date_format(from_unixtime(timestamp), '%Y-%m-%d')"""

new_members_new = """select date_format(from_unixtime(timestamp), '%Y-%m-%d') as date, ifnull(count(w.uid),0) as web, ifnull(phones,0) as mobile
                    from dosomething.dosomething_signup w
                    join dosomething.users u on w.uid=u.uid
                    left join
                    (select date_format(activated_at, '%Y-%m-%d') as date, count(m.phone_number) as phones
                    from users_and_activities.mobile_subscriptions m
                    join users_and_activities.mobile_users mu
                    on m.phone_number=mu.phone_number
                    where campaign_id in ({0}) and been_alpha = 0 and first_seen_campaign = 1 and date_add(mu.created_at, interval 5 minute) >= m.activated_at and date_format(activated_at, '%Y-%m-%d') >= "{2}" and date_format(activated_at, '%Y-%m-%d') <= "{3}"
                    group by date_format(activated_at, '%Y-%m-%d')) m
                    on date_format(from_unixtime(timestamp), '%Y-%m-%d')=m.date
                    where nid = {1} and date_add(from_unixtime(u.created), interval 5 minute) >= from_unixtime(timestamp) and from_unixtime(timestamp, '%Y-%m-%d') >= "{2}" and from_unixtime(timestamp, '%Y-%m-%d') <= "{3}"
                    group by date_format(from_unixtime(timestamp), '%Y-%m-%d')"""

new_sign_ups_new_mobile = """select date_format(activated_at, '%Y-%m-%d') as date, 0 as web, ifnull(count(phone_number),0) as mobile
                  from users_and_activities.mobile_subscriptions
                  where campaign_id in ({0}) and first_seen_campaign = 1 and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}"
                  group by date_format(activated_at, '%Y-%m-%d')"""

new_members_new_mobile = """select date_format(activated_at, '%Y-%m-%d') as date, 0 as web, ifnull(count(m.phone_number),0) as mobile
                    from users_and_activities.mobile_subscriptions m
                    join users_and_activities.mobile_users mu
                    on m.phone_number=mu.phone_number
                    where campaign_id in ({0}) and first_seen_campaign = 1 and date_add(mu.created_at, interval 5 minute) >= m.activated_at and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}"
                    group by date_format(activated_at, '%Y-%m-%d')"""

sources_new = """select date, e.site as source, ifnull(entrances,0) as unq_visits from users_and_activities.entrances e join
              (select site from users_and_activities.entrances where nid = {0} and date >= "{1}" and date <= "{2}" group by site order by sum(entrances) desc limit 15) s on e.site=s.site
              where nid = {0} and date >= "{1}" and date <= "{2}" """

signups_total = """select
                ifnull(count(uid),0)
                +
                (select  ifnull(count(phone_number),0)
                from users_and_activities.mobile_subscriptions
                where campaign_id in ({0}) and been_alpha = 0 and first_seen_campaign = 1 and date_format(activated_at, '%Y-%m-%d') >= "{2}" and date_format(activated_at, '%Y-%m-%d') <= "{3}")
                as total_signups
                from dosomething.dosomething_signup w
                where nid = {1} and from_unixtime(timestamp, '%Y-%m-%d') >= "{2}" and from_unixtime(timestamp, '%Y-%m-%d') <= "{3}" """

signups_web = """select
                ifnull(count(uid),0) as web_su
                from dosomething.dosomething_signup
                where nid = {0} and from_unixtime(timestamp, '%Y-%m-%d') >= "{1}" and from_unixtime(timestamp, '%Y-%m-%d') <= "{2}" """

new_members_total = """select
                    ifnull(count(w.uid),0)
                    +
                    (select ifnull(count(m.phone_number),0)
                    from users_and_activities.mobile_subscriptions m
                    join users_and_activities.mobile_users mu
                    on m.phone_number=mu.phone_number
                    where campaign_id in  ({0}) and been_alpha = 0 and first_seen_campaign = 1 and date_add(mu.created_at, interval 5 minute) >= m.activated_at and date_format(activated_at, '%Y-%m-%d') >= "{2}" and date_format(activated_at, '%Y-%m-%d') <= "{3}" )
                    as new_members_total
                    from dosomething.dosomething_signup w
                    join dosomething.users u on w.uid=u.uid
                    where nid = {1} and date_add(from_unixtime(u.created), interval 5 minute) >= from_unixtime(timestamp) and from_unixtime(timestamp, '%Y-%m-%d') >= "{2}" and from_unixtime(timestamp, '%Y-%m-%d') <= "{3}" """

report_back_total_web = """select
                        ifnull(count(*),0) as rb
                        from
                        dosomething.dosomething_reportback
                        where nid = {0} and flagged = 0 and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
                        or nid = {0} and flagged is null and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}" """

report_back_total_sms = """select
                        ifnull(count(*),0) as alpha
                        from users_and_activities.mobile_subscriptions
                        where campaign_id in ({0}) and web_alpha = 1 and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}" """

impact_total = """select
                  ifnull(sum(quantity),0) as impact
                  from
                  dosomething.dosomething_reportback
                  where nid = {0} and flagged = 0 and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
                  or nid = {0} and flagged is null and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}" """

traffic_total = """select
               ifnull(sum(visitors),0) as traffic
               from
               users_and_activities.all_traffic
               where nid = {0} and date >= "{1}" and date <= "{2}" """

new_sign_ups_new_mobile_total = """select ifnull(count(phone_number),0) as mobile_signup_total
                                   from users_and_activities.mobile_subscriptions
                                   where campaign_id in ({0}) and first_seen_campaign = 1 and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}" """

new_members_new_mobile_total = """select ifnull(count(m.phone_number),0) as mobile_new_members_total
                                  from users_and_activities.mobile_subscriptions m
                                  join users_and_activities.mobile_users mu
                                  on m.phone_number=mu.phone_number
                                  where campaign_id in ({0}) and first_seen_campaign = 1 and date_add(mu.created_at, interval 5 minute) >= m.activated_at and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}" """

new_sign_ups_new_alphas = """select ifnull(count(phone_number),0) as alphas
                             from users_and_activities.mobile_subscriptions
                             where campaign_id in ({0}) and web_alpha = 1 and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}" """

traffic_daily = """select
               date, ifnull(visitors,0) as visitors
               from
               users_and_activities.all_traffic
               where nid = {0} and date_format(date, '%Y-%m-%d') >= "{1}" and date_format(date, '%Y-%m-%d') <= "{2}" """

reportback_web_daily = """select
               date_format(from_unixtime(updated), '%Y-%m-%d') as date,
               ifnull(count(rbid),0) as reportbacks
               from
               dosomething.dosomething_reportback
               where nid = {0} and flagged = 0 and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
               or
               nid = {0} and flagged is null and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
               group by date_format(from_unixtime(updated), '%Y-%m-%d')"""

reportback_sms_daily = """select
                        date_format(activated_at, '%Y-%m-%d') as date,
                        ifnull(count(phone_number),0) as alphas
                        from users_and_activities.mobile_subscriptions
                        where campaign_id in ({0}) and web_alpha = 1 and date_format(activated_at, '%Y-%m-%d') >= "{1}" and date_format(activated_at, '%Y-%m-%d') <= "{2}"
                        group by date_format(activated_at, '%Y-%m-%d')"""

impact_daily = """select
                  date_format(from_unixtime(updated), '%Y-%m-%d') as date,
                  ifnull(sum(quantity),0) as impact
                  from
                  dosomething.dosomething_reportback
                  where nid = {0} and flagged = 0 and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
                  or
                  nid = {0} and flagged is null and quantity <= {1} and from_unixtime(updated, '%Y-%m-%d') >= "{2}" and from_unixtime(updated, '%Y-%m-%d') <= "{3}"
                  group by date_format(from_unixtime(updated), '%Y-%m-%d')"""

search_campaigns = "select title from dosomething.node where title like '%{0}%' and type = 'campaign' "

demographics_action_gender = "select 'Action_by_Reported_Gender' as header, name, group_concat(gender) as metric, group_concat(count) as count from action_gender group by name"
demographics_action_income = "select 'Action_by_Income' as header, name, group_concat(income_level) as metric, group_concat(count) as count from action_income group by name"
demographics_cause_gender = "select 'Cause_by_Reported_Gender' as header, name,  group_concat(gender) as metric, group_concat(count) as count from cause_gender group by name"
demographics_cause_income = "select 'Cause_by_Income' as header, name, group_concat(income_level) as metric, group_concat(count) as count from cause_income group by name"
demographics_mobile_age = "select 'Mobile_Age' as header, group_concat(age) as metric, group_concat(count) as count from baseline_mobile_age"
demographics_mobile_gender = "select 'Mobile_Assigned_Gender' as header, group_concat(gender) as metric, group_concat(count) as count from baseline_mobile_gender"
demographics_mobile_income = "select 'Mobile_Income' as header, group_concat(income_level) as metric, group_concat(count) as count from baseline_mobile_income"
demographics_mobile_race = "select 'Mobile_Race' as header, group_concat(race) as metric, group_concat(count) as count from baseline_mobile_race"
demographics_web_age = "select 'Web_Age' as header, group_concat(age) as metric, group_concat(count) as count from baseline_web_age"
demographics_web_gender = "select 'Web_Assigned_Gender' as header, group_concat(gender) as metric, group_concat(count) as count from baseline_web_gender"
demographics_web_income = "select 'Web_Income' as header, group_concat(income_level) as metric, group_concat(count) as count from baseline_web_income"
demographics_web_race = "select 'Web_Race' as header, group_concat(race) as metric, group_concat(count) as count from baseline_web_race"

