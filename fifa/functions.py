from django.db import models, connection


class Queries:
    def get_avg_alternate_player():
        query = """      
        select
            name_team ,count(titular),titular
        from
            fifa_team ft
        inner join fifa_player fp on
            ft.id = fp.team_id 
        group by
            name_team,titular
        """
        return query

    def get_avg_players_by_team():
        query = """
        select 
            equipo,
            cast(((cast(jugadores as real )/cast(total as real)*100))  as real) as porc_jug_team
            from(
            SELECT 
                ft.name_team as equipo,
                count(1) as jugadores,
                (SELECT COUNT(1) FROM fifa_player) AS total
            FROM 
                fifa_player fp,
                fifa_team ft
            where 
                ft.id = fp.team_id
            GROUP BY team_id
            );
        """
        return query
