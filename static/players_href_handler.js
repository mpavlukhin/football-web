function addHrefToPlayersRows() {
    var table = document.getElementById('statistics');

    var body = table.tBodies[0];
    var trs = body.getElementsByTagName("tr");

    for (let i = 0; i < trs.length; i++)
    {
        const playerTr = trs[i];
        const playerNameTd = playerTr.cells[1];

        const playerName = playerNameTd.innerHTML.trim();

        playerTr.onclick = function() {
                window.location.href='playerstats?name=' + playerName
            };

        playerTr.onmouseover= function() {
                playerNameTd.style.textDecoration = "underline";
            };

        playerTr.onmouseout= function() {
                playerNameTd.style.textDecoration = "";
            };
    }
}