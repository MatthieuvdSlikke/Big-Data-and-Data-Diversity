create table spatial_join as (
select N.area_name, sum(num_cars)
from "Neighbourhoods_location" N left join "CarSharingPods" C on ((latitude between northeast_lat and southwest_lat) and (longitude between northeast_lng and southwest_lat ) )
group by N.area_name)
