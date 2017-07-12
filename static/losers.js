function addBorderBottom(row) {
    var table = document.getElementById('statistics');

    var body = table.tBodies[0];
    var trs = body.getElementsByTagName("tr");

    last_good_football_player = trs[row];
    last_good_football_player.style.borderBottom = "solid #0761ff";
}