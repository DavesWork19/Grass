USE NBA;

SELECT * FROM nbaStats where date = '03/2/24';
SELECT * FROM nbaStats WHERE date < '03/11/24' or date is NULL;
SELECT * FROM nbaStats WHERE isWin is NULL and spread is not NULL;
SELECT * FROM nbaStats WHERE teamNumber = 5;
SELECT * FROM nbaStats WHERE isWin is NULL and spread is NULL;

SELECT * FROM nbaParlay2;

INSERT INTO nbaStats (id, gameNumber, teamNumber, isHome, oppTeamNumber, isWin, isOT, gameDayNumber, gameStartNumber, teamPoints, oppTeamPoints, teamWins, teamLosses, teamStreakCode, isInSeasonTournament, year, spread, spreadOdds, overUnder, overUnderOdds, moneyLine, gameTimeActual, spreadCalculated, overUnderCalculated, spreadActual, overUnderActual, date) VALUES (700524, 70, 5, 1, 3, NULL, NULL, 4, 16, NULL, NULL, NULL, NULL, NULL, 0, 2024, '-9.5', '-108', 220, '-112', '-450', '8:00p', NULL, NULL, NULL, NULL, '03/22/24');

UPDATE nbaStats
SET spread = null,
spreadOdds = null,
overUnder = null,
overUnderOdds = null,
moneyLine = null
WHERE id = 7001424;

SELECT * FROM nbaStats where teamNumber = 3;
SELECT * FROM nbaStats where id =650324;

