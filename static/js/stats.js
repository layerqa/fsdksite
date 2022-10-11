$.ajax({
    url: "/api/stats",
    success: function (result) {
        for (const player of result.top_kill) {
            $(".top-kill").append(
                `
                <tr>
                    <th scope="row"><a href="/player?id=${player.id}" class="text-white">${player.name}</a></th>
                    <td>${player.kills.toLocaleString()}</td>    
                </tr>
                `
            )
        };
        $(".loading-top-kill").remove();
        for (const player of result.top_skill) {
            $(".top-skill").append(
                `
                <tr>
                    <th scope="row"><a href="/player?id=${player.id}" class="text-white">${player.name}</a></th>
                    <td>${player.skill}</td>    
                </tr>
                `
            )
        };
        $(".loading-top-skill").remove();
        for (const player of result.top_damage) {
            $(".top-damage").append(
                `
                <tr>
                    <th scope="row"><a href="/player?id=${player.id}" class="text-white">${player.name}</a></th>
                    <td>${player.dmg.toLocaleString()}</td>    
                </tr>
                `
            )
        };
        $(".loading-top-damage").remove();
        for (const player of result.top_players) {
            $(".top-players").append(
                `
                <tr>
                    <th scope="row"><a href="/player?id=${player.id}" class="text-white">${player.name}</a></th>
                    <td>${player.kills.toLocaleString()}</td>
                    <td>${player.skill_text}</td>
                    <td>${player.deaths.toLocaleString()}</td>
                    <td>${player.dmg.toLocaleString()}</td>
                </tr>
                `
            )
        };
        $(".loading-top-players").remove();
    }
})