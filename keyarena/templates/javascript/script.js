let teams = [];
let currentRound = 0;
let winners = [];
let losers = [];
let matchHistory = [];

function startTournament() {
    const numParticipants = parseInt(document.getElementById('num-participants').value);

    if (numParticipants < 2 || isNaN(numParticipants)) {
        alert('O número de participantes deve ser pelo menos 2.');
        return;
    }

    teams = [];
    for (let i = 1; i <= numParticipants; i++) {
        teams.push({ name: `Time ${i}`, wins: 0, losses: 0 });
    }

    currentRound = 0;
    winners = [];
    losers = [];
    matchHistory = [];

    document.getElementById('rounds').innerHTML = '';
    document.getElementById('team-results').innerHTML = '';
    document.getElementById('new-round-btn').style.display = 'inline';

    startNewRound();
}

function startNewRound() {
    if (currentRound > 0) {
        getWinnersAndLosers();
    }

    currentRound++;

    let teamsForRound = currentRound === 1
        ? teams.map(t => t.name)
        : [...winners, ...losers];

    // Gerar e exibir as partidas
    let roundMatches = generateRoundMatches(teamsForRound);
    displayRound(roundMatches, currentRound);
    updateTeamResults();
}

function getWinnersAndLosers() {
    winners.length = 0;  // Limpa os arrays globais antes de cada rodada
    losers.length = 0;
    const selects = document.querySelectorAll(`select[data-round="${currentRound}"]`);

    selects.forEach(select => {
        const winner = select.value;
        const team1 = select.getAttribute('data-team1');
        const team2 = select.getAttribute('data-team2');

        if (!team1 || !team2) {
            console.error("Um dos times não está definido.");
            return;
        }

        if (winner === "") {
            alert('Por favor, selecione um vencedor para cada partida antes de prosseguir para a próxima rodada.');
            return;
        }

        if (winner === team1) {
            winners.push(team1);
            losers.push(team2);
            updateTeamRecord(team1, true);
            updateTeamRecord(team2, false);
        } else if (winner === team2) {
            winners.push(team2);
            losers.push(team1);
            updateTeamRecord(team2, true);
            updateTeamRecord(team1, false);
        }

        matchHistory.push([team1, team2]);
    });

    console.log("Vencedores:", winners);
    console.log("Perdedores:", losers);
}

function updateTeamRecord(teamName, won) {
    const team = teams.find(t => t.name === teamName);
    if (team) {
        if (won) {
            team.wins++;
        } else {
            team.losses++;
        }
    }
}

function generateRoundMatches(teams) {
    let matchups = [];
    let availableTeams = [...teams];

    if (availableTeams.length % 2 !== 0) {
        availableTeams.push('BYE');
    }

    while (availableTeams.length >= 2) {
        let team1 = availableTeams.shift();
        let opponentIndex = availableTeams.findIndex(opponent => !hasPlayedBefore(team1, opponent));
        if (opponentIndex === -1) {
            opponentIndex = 0;
        }

        let team2 = availableTeams.splice(opponentIndex, 1)[0];
        if (team2) {
            matchups.push([team1, team2]);
        } else {
            console.error(`Não foi possível encontrar um oponente para: ${team1}`);
        }
    }

    return matchups;
}

function hasPlayedBefore(team1, team2) {
    if (!team1 || !team2) {
        return false;
    }
    return matchHistory.some(match => 
        (match[0] === team1 && match[1] === team2) || 
        (match[0] === team2 && match[1] === team1)
    );
}

function displayRound(matchups, roundNumber) {
    const roundsContainer = document.getElementById('rounds');
    const roundDiv = document.createElement('div');
    roundDiv.classList.add('round');
    roundDiv.innerHTML = `<h3>Rodada ${roundNumber}</h3>`;

    matchups.forEach(matchup => {
        const matchDiv = document.createElement('div');
        matchDiv.classList.add('matchup');

        const team1 = matchup[0];
        const team2 = matchup[1];

        // Criação do dropdown para selecionar o vencedor
        matchDiv.innerHTML = `
            <span>${team1}</span>
            <span>vs</span>
            <span>${team2}</span>
            <select data-round="${roundNumber}" data-team1="${team1}" data-team2="${team2}">
                <option value="">Selecionar vencedor</option>
                <option value="${team1}">${team1}</option>
                <option value="${team2}">${team2}</option>
            </select>
        `;
        roundDiv.appendChild(matchDiv);
    });

    roundsContainer.appendChild(roundDiv);
}

function updateTeamResults() {
    const teamResultsContainer = document.getElementById('team-results');
    teamResultsContainer.innerHTML = '';

    teams.forEach(team => {
        const teamRecord = document.createElement('li');
        teamRecord.textContent = `${team.name}: ${team.wins} Vitórias, ${team.losses} Derrotas`;
        teamResultsContainer.appendChild(teamRecord);
    });
}
