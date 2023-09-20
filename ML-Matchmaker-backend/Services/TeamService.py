class TeamService:
    def calculateTeamAverages(self, playerStatsList):
        averagedTeamStats = []

        for i in range (1, 8):
            statCount = 0
            for j in range (len(playerStatsList)):
                statCount = playerStatsList[j][i]
            
            averagedTeamStatCount = statCount / len(playerStatsList)

            averagedTeamStats.append(averagedTeamStatCount)

        return averagedTeamStats
    
    def calculateELOAverages(self, playerELOList):
        averagedELOStats = []
        totalELOCount = 0

        for i in range(len(playerELOList)):
            totalELOCount += playerELOList[i]

        averagedELO = totalELOCount / len(playerELOList)
        averagedELOStats.append(averagedELO)

        return averagedELOStats
        


