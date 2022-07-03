from django.db import models, connection


class Queries:
    def get_avg_alternate_player():
        query = """      
            select
                name_team ,
                cast(count(*) as real)/cast((
                select
                    count(*)
                from
                    fifa_team ft
                inner join fifa_player fp on
                    ft.id = fp.team_id 
                group by
                    name_team order by name_team asc
            ) as real ) 
            from
                fifa_team ft
            inner join fifa_player fp on
                ft.id = fp.team_id where titular=0
            group by
                name_team order by name_team asc ;
        """
        return query
