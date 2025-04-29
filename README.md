# ⚽ Liga MX Analytics Dashboard

This project is a web-based analytics dashboard for Liga MX, built with Django and MySQL. It displays various statistical views such as average attendance, player stats, team performance, and more using optimized database views.

## 🚀 Features

- Dynamic dashboard with Bootstrap styling
- Clean team/player statistics with human-readable labels
- MySQL views for fast, optimized analytics queries
- Environment-agnostic setup via virtualenv and `requirements.txt`

## 🏗️ Tech Stack

- Python 3.11
- Django 5.x
- MySQL
- Bootstrap 5
- HTML/CSS
- PyMySQL / mysqlclient
- sqlparse

## 📁 Project Structure
liga_mx_analytics/ 
├── env/ # virtualenv (excluded from Git) 
├── liga_mx_analytics/ # Django project settings 
│ └── stats/ # Main app: views, templates, models 
│ └── base.html
│ └── dashboard.html 
│ └── static/ styles.css
├── manage.py 
├── .gitignore 
├── requirements.txt 
└── README.md

## ⚙️ Setup Instructions
1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/liga-mx-analytics.git
   cd liga-mx-analytics

2. **Create a virtual environment**
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt   

4. **Configure your database**
Update settings.py with your MySQL DB name, user, and password.

## 🚀 List of Views
-- Teams Stadiums by Capacity
        CREATE VIEW Teams_Stadiums_By_Capacity AS
        SELECT t.team_name, s.stadium_name, s.capacity
        FROM Teams t
        JOIN Stadiums s ON t.stadium_id = s.stadium_id
        ORDER BY s.capacity DESC;

-- Teams and their founded year
        CREATE VIEW Teams_By_Founded_Year AS
        SELECT team_name, founded_year
        FROM Teams
		ORDER BY founded_year ASC;

-- Team with the most and least wins
        CREATE VIEW Most_And_Least_Wins AS
        SELECT team_name, wins
        FROM Team_Stats ts
        JOIN Teams t ON ts.team_id = t.team_id
        ORDER BY wins DESC;

-- Team with the most and least losses
        CREATE VIEW Most_And_Least_Losses AS
        SELECT team_name, losses
        FROM Team_Stats ts
        JOIN Teams t ON ts.team_id = t.team_id
        ORDER BY losses DESC;

-- Teams with the most and least goals scored
        CREATE VIEW Most_And_Least_Goals_Scored AS
        SELECT team_name, goals_scored
        FROM Team_Stats ts
        JOIN Teams t ON ts.team_id = t.team_id
		ORDER BY goals_scored DESC;

-- Teams with the best and worse goal difference
        CREATE VIEW Best_And_Worst_Goal_Difference AS
        SELECT team_name, goal_difference
        FROM Team_Stats ts
        JOIN Teams t ON ts.team_id = t.team_id
		ORDER BY goal_difference DESC;

-- Teams and their respective number of mexican players
        CREATE VIEW Mexican_Player_Count_Per_Team AS
        SELECT t.team_name, COUNT(p.player_id) AS mexican_players
        FROM All_Players p
        JOIN Teams t ON p.team_id = t.team_id
        WHERE p.nationality = 'Mexico'
        GROUP BY t.team_name;

-- Team with the most and least mexican players
        CREATE VIEW Most_And_Least_Mexican_Players AS
        SELECT t.team_name, COUNT(p.player_id) AS mexican_players
        FROM All_Players p
        JOIN Teams t ON p.team_id = t.team_id
        WHERE p.nationality = 'Mexico'
        GROUP BY t.team_name
        ORDER BY mexican_players DESC;

-- Player of the season
        CREATE VIEW Season_MVP AS
        SELECT p.player_name, t.team_name, fps.goals, fps.assists, 
               (fps.goals + fps.assists) AS goal_contributions
        FROM Field_Player_Stats fps
        JOIN All_Players p ON fps.player_id = p.player_id
        JOIN Teams t ON p.team_id = t.team_id
        ORDER BY goal_contributions DESC
        LIMIT 1;

-- Best player for each team
        CREATE VIEW Team_MVPs AS
        WITH Player_Contributions AS (
            SELECT fps.player_id, (fps.goals + fps.assists) AS contributions
            FROM Field_Player_Stats fps
        ),
        Ranked_Contributors AS (
            SELECT t.team_name, p.player_name, pc.contributions,
                   RANK() OVER (PARTITION BY t.team_name ORDER BY pc.contributions DESC) AS rnk
            FROM Player_Contributions pc
            JOIN All_Players p ON pc.player_id = p.player_id
            JOIN Teams t ON p.team_id = t.team_id
        )
        SELECT team_name, player_name, contributions
        FROM Ranked_Contributors
        WHERE rnk = 1;

-- View for Apertura 2023 games
			CREATE VIEW Apertura_2023_Games AS
			SELECT 
				f.match_date, 
				ht.team_name AS home_team, 
				at.team_name AS away_team,
				f.attendance, 
				s.stadium_name AS stadium, 
				f.winner, 
				f.score
			FROM Fixtures f
			JOIN Teams ht ON f.home_team_id = ht.team_id
			JOIN Teams at ON f.away_team_id = at.team_id
			JOIN Stadiums s ON f.stadium_id = s.stadium_id
			WHERE f.tournament = 'Apertura 2023 Regular Season'
			ORDER BY f.match_date;

-- View for Clausura 2024 games
			CREATE VIEW Clausura_2024_Games AS
			SELECT 
				f.match_date, 
				ht.team_name AS home_team, 
				at.team_name AS away_team,
				f.attendance, 
				s.stadium_name AS stadium, 
				f.winner, 
				f.score
			FROM Fixtures f
			JOIN Teams ht ON f.home_team_id = ht.team_id
			JOIN Teams at ON f.away_team_id = at.team_id
			JOIN Stadiums s ON f.stadium_id = s.stadium_id
			WHERE f.tournament = 'Clausura 2024 Regular Season'
			ORDER BY f.match_date;

-- Best Home teams
            CREATE VIEW Best_Home_Teams AS
			SELECT 
			    ht.team_name AS team,
			    COUNT(*) AS home_games,
			    SUM(CASE WHEN f.winner = ht.team_name THEN 1 ELSE 0 END) AS home_wins
			FROM Fixtures f
			JOIN Teams ht ON f.home_team_id = ht.team_id
			GROUP BY ht.team_name
			ORDER BY home_wins DESC;

-- Best Away teams
			CREATE VIEW Best_Away_Teams AS
			SELECT 
			    at.team_name AS team,
			    COUNT(*) AS away_games,
			    SUM(CASE WHEN f.winner = at.team_name THEN 1 ELSE 0 END) AS away_wins
			FROM Fixtures f
			JOIN Teams at ON f.away_team_id = at.team_id
			GROUP BY at.team_name
			ORDER BY away_wins DESC;

-- Attendance per team
            CREATE VIEW Team_Attendance_Ranking AS
			SELECT 
			    t.team_name,
			    SUM(f.attendance) AS total_home_attendance
			FROM Fixtures f
			JOIN Teams t ON f.home_team_id = t.team_id
			GROUP BY t.team_name
			ORDER BY total_home_attendance DESC;

-- Most Fouled Player
			CREATE VIEW Most_Fouled_Player AS
			SELECT p.player_name, t.team_name, fps.fouls_drawn
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY fps.fouls_drawn DESC
			LIMIT 1;
            
-- Most Offsides
			CREATE VIEW Most_Offsides_Player AS
			SELECT p.player_name, t.team_name, fps.offsides
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY fps.offsides DESC
			LIMIT 1;

-- Most Cards (Yellow + Red)
			CREATE VIEW Most_Carded_Players AS
			SELECT p.player_name, t.team_name, fps.yellow_cards, fps.red_cards,
				   (fps.yellow_cards + fps.red_cards) AS total_cards
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY total_cards DESC;

-- Most Penalties Scored
			CREATE VIEW Most_Penalties_Scored AS
			SELECT p.player_name, t.team_name, fps.pk_made
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY fps.pk_made DESC
			LIMIT 1;

-- Most Shots on Target
			CREATE VIEW Most_Shots_On_Target AS
			SELECT p.player_name, t.team_name, fps.shots_on_target
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY fps.shots_on_target DESC
			LIMIT 1;

-- Minutes Played by Youngsters per Team
			CREATE VIEW Youngsters_Minutes_By_Team AS
			SELECT t.team_name, SUM(fps.minutes) AS total_minutes_young_players
			FROM Field_Player_Stats fps
			JOIN All_Players p ON fps.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			WHERE p.age < 21
			GROUP BY t.team_name
			ORDER BY total_minutes_young_players DESC;

-- Oldest and Youngest Player per Team
			CREATE VIEW Oldest_Youngest_Per_Team AS
			WITH Ranked_Players AS (
				SELECT 
					p.player_name,
					t.team_name,
					p.field_position,
					p.age,
					RANK() OVER (PARTITION BY p.team_id ORDER BY p.age DESC) AS oldest_rank,
					RANK() OVER (PARTITION BY p.team_id ORDER BY p.age ASC) AS youngest_rank
				FROM All_Players p
				JOIN Teams t ON p.team_id = t.team_id
			)
			SELECT team_name, player_name, field_position, age
			FROM Ranked_Players
			WHERE oldest_rank = 1
			UNION
			SELECT team_name, player_name, field_position, age
			FROM Ranked_Players
			WHERE youngest_rank = 1;

-- Most and Least Minutes Per Team
			CREATE VIEW Most_Least_Minutes_Per_Team AS
			WITH Player_Minutes AS (
				SELECT p.player_name, t.team_name, fps.minutes
				FROM Field_Player_Stats fps
				JOIN All_Players p ON fps.player_id = p.player_id
				JOIN Teams t ON p.team_id = t.team_id
				UNION ALL
				SELECT p.player_name, t.team_name, gs.minutes
				FROM Goalkeepers_Stats gs
				JOIN All_Players p ON gs.player_id = p.player_id
				JOIN Teams t ON p.team_id = t.team_id
			),
			Ranked_Minutes AS (
				SELECT *,
					RANK() OVER (PARTITION BY team_name ORDER BY minutes DESC) AS max_rank,
					RANK() OVER (PARTITION BY team_name ORDER BY minutes ASC) AS min_rank
				FROM Player_Minutes
			)
			SELECT team_name, player_name, minutes, 'Most Minutes' AS status
			FROM Ranked_Minutes
			WHERE max_rank = 1
			UNION
			SELECT team_name, player_name, minutes, 'Least Minutes' AS status
			FROM Ranked_Minutes
			WHERE min_rank = 1;

-- Goalkeepers with Most Clean Sheets
			CREATE VIEW GK_Most_Clean_Sheets AS
			SELECT p.player_name, t.team_name, gs.clean_sheets
			FROM Goalkeepers_Stats gs
			JOIN All_Players p ON gs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY gs.clean_sheets DESC;

-- Goalkeepers with Most Goals Conceded
			CREATE VIEW GK_Most_Goals_Conceded AS
			SELECT p.player_name, t.team_name, gs.goals_against
			FROM Goalkeepers_Stats gs
			JOIN All_Players p ON gs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY gs.goals_against DESC;

-- Number of Games officiated per Referee
			CREATE VIEW Referee_Game_Count AS
			SELECT 
				r.referee_name, 
				COUNT(*) AS games_officiated
			FROM Fixtures f
			JOIN Referees r ON f.referee_id = r.referee_id
			GROUP BY r.referee_name
			ORDER BY games_officiated DESC;

-- Displays the referee that officiated the most times for each team
			CREATE VIEW Team_Referee_Repeats AS
			SELECT 
				t.team_name, 
				r.referee_name, 
				COUNT(*) AS appearances
			FROM Fixtures f
			JOIN Teams t ON f.home_team_id = t.team_id OR f.away_team_id = t.team_id
			JOIN Referees r ON f.referee_id = r.referee_id
			GROUP BY t.team_name, r.referee_name
			HAVING appearances > 1
			ORDER BY appearances DESC;

-- Goal scorers
			CREATE VIEW Top_Goal_Scorers AS
			SELECT 
				p.player_name, 
				t.team_name, 
				fs.goals
			FROM Field_Player_Stats fs
			JOIN All_Players p ON fs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			ORDER BY fs.goals DESC
			LIMIT 10;

-- Best midfielders
			CREATE VIEW Top_Midfielders_By_Assists AS
			SELECT 
				p.player_name, 
				t.team_name, 
				fs.assists
			FROM Field_Player_Stats fs
			JOIN All_Players p ON fs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			WHERE p.field_position = 'MF'
			ORDER BY fs.assists DESC
			LIMIT 10;

-- Best defenders
			CREATE VIEW Top_Defenders_By_Tackles AS
			SELECT 
				p.player_name, 
				t.team_name, 
				fs.tackles_won
			FROM Field_Player_Stats fs
			JOIN All_Players p ON fs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			WHERE p.field_position = 'DF'
			ORDER BY fs.tackles_won DESC
			LIMIT 10;

-- Best player per team
			CREATE VIEW Best_Player_Per_Team AS
			SELECT 
				t.team_name,
				p.player_name,
				fs.goals,
				fs.assists,
				(fs.goals + fs.assists) AS goal_contributions
			FROM Field_Player_Stats fs
			JOIN All_Players p ON fs.player_id = p.player_id
			JOIN Teams t ON p.team_id = t.team_id
			WHERE (fs.goals + fs.assists) = (
				SELECT MAX(fs2.goals + fs2.assists)
				FROM Field_Player_Stats fs2
				JOIN All_Players p2 ON fs2.player_id = p2.player_id
				WHERE p2.team_id = p.team_id
			)
			ORDER BY goal_contributions DESC;

-- Roster per team
			CREATE OR REPLACE VIEW club_america_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Club América'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_chivas_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Guadalajara'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_monterrey_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Monterrey'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_tigres_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'UANL'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_pumas_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'UNAM'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_toluca_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Toluca'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_pachuca_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Pachuca'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_azul_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Cruz Azul'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_leon_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'León'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_queretaro_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Querétaro'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_necaxa_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Necaxa'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_atletico_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Atlético'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_mazatlan_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Mazatlán'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_santos_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Santos'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_tijuana_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Tijuana'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_juarez_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'FC Juárez'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_atlas_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Atlas'
			ORDER BY ap.player_name;

			CREATE OR REPLACE VIEW club_puebla_roster AS
			SELECT
			  ap.player_name,
			  ap.nationality,
			  ap.field_position,
			  ap.age
			FROM Teams AS t
			JOIN All_Players AS ap ON t.team_id = ap.team_id
			WHERE t.team_name = 'Puebla'
			ORDER BY ap.player_name;

-- avg_age_per_team
            CREATE OR REPLACE VIEW avg_age_per_team AS
            SELECT 
                t.team_name,
                IFNULL(AVG(p.age), 0) AS avg_age
            FROM All_Players p
            JOIN Teams t ON p.team_id = t.team_id
            WHERE p.age IS NOT NULL
            GROUP BY t.team_name;

-- avg_attendance_per_team   
            CREATE OR REPLACE VIEW avg_attendance_per_team AS
            SELECT 
                t.team_name,
                AVG(f.attendance) AS avg_attendance
            FROM Fixtures f
            JOIN Teams t ON f.home_team_id = t.team_id OR f.away_team_id = t.team_id
            GROUP BY t.team_name;       

-- avg_goals_scored_per_team
            CREATE OR REPLACE VIEW avg_goals_scored_per_team AS
            SELECT 
                t.team_name,
                AVG(
                    CAST(SUBSTRING_INDEX(f.score, '-', 1) AS UNSIGNED) +
                    CAST(SUBSTRING_INDEX(f.score, '-', -1) AS UNSIGNED)
                ) AS avg_goals
            FROM Fixtures f
            JOIN Teams t ON f.home_team_id = t.team_id OR f.away_team_id = t.team_id
            GROUP BY t.team_name;

-- avg_goals_conceded_per_team
            CREATE OR REPLACE VIEW avg_goals_conceded_per_team AS
            SELECT 
                t.team_name,
                AVG(CAST(SUBSTRING_INDEX(f.score, '-', -1) AS UNSIGNED)) AS avg_goals_conceded
            FROM Fixtures f
            JOIN Teams t ON f.home_team_id = t.team_id OR f.away_team_id = t.team_id
            GROUP BY t.team_name;

-- avg_yellow_red_cards_per_team
            CREATE OR REPLACE VIEW avg_yellow_red_cards_per_team AS
            SELECT 
                t.team_name,
                AVG(fs.yellow_cards + fs.red_cards) AS avg_cards
            FROM Field_Player_Stats fs
            JOIN All_Players p ON fs.player_id = p.player_id
            JOIN Teams t ON p.team_id = t.team_id
            GROUP BY t.team_name;

-- avg_success_penalty_percentage
            CREATE OR REPLACE VIEW avg_success_penalty_percentage AS
            SELECT 
                p.player_name,
                (SUM(fs.pk_made) / SUM(fs.pk_attempted)) * 100 AS success_percentage
            FROM Field_Player_Stats fs
            JOIN All_Players p ON fs.player_id = p.player_id
            GROUP BY p.player_name
            HAVING SUM(fs.pk_attempted) > 0;

-- avg_shots_on_target_percentage
            CREATE OR REPLACE VIEW avg_shots_on_target_percentage AS
            SELECT 
                p.player_name,
                (SUM(fs.shots_on_target) / SUM(fs.total_shots)) * 100 AS shots_on_target_percentage
            FROM Field_Player_Stats fs
            JOIN All_Players p ON fs.player_id = p.player_id
            GROUP BY p.player_name
            HAVING SUM(fs.total_shots) > 0;

avg_goals_saved_per_goalkeeper
            CREATE OR REPLACE VIEW avg_goals_saved_per_goalkeeper AS
            SELECT 
                p.player_name,
                AVG((gs.goals_against / gs.shots_on_target_against) * gs.saves) AS avg_goals_saved
            FROM Goalkeepers_Stats gs
            JOIN All_Players p ON gs.player_id = p.player_id
            GROUP BY p.player_name;

avg_attendance_per_tournament
            CREATE VIEW avg_attendance_per_tournament AS
            SELECT 
                f.tournament,
                AVG(f.attendance) AS avg_attendance
            FROM Fixtures f
            GROUP BY f.tournament;

## 🚀 List of Created indexes
CREATE INDEX idx_team_id ON All_Players (team_id);
CREATE INDEX idx_tournament ON Fixtures (tournament);
CREATE INDEX idx_home_team_id ON Fixtures (home_team_id);
CREATE INDEX idx_away_team_id ON Fixtures (away_team_id);
CREATE INDEX idx_player_id ON Field_Player_Stats (player_id);
CREATE INDEX idx_team_id_teams ON Teams (team_id);
CREATE INDEX idx_referee_id ON Fixtures (referee_id);
CREATE INDEX idx_stadium_id ON Fixtures (stadium_id);
CREATE INDEX idx_player_position ON All_Players (player_id, field_position);
CREATE INDEX idx_match_date ON Fixtures (match_date);
CREATE INDEX idx_attendance ON Fixtures (attendance);
CREATE INDEX idx_score ON Fixtures (score);
CREATE INDEX idx_stadium_team ON Fixtures (stadium_id, home_team_id);
CREATE INDEX idx_stadium_away_team ON Fixtures (stadium_id, away_team_id);
CREATE INDEX idx_referee_name ON Referees (referee_name);
CREATE INDEX idx_player_name ON All_Players (player_name);
CREATE INDEX idx_field_position ON All_Players (field_position);
CREATE INDEX idx_goalkeeper_id ON Goalkeepers_Stats (player_id);